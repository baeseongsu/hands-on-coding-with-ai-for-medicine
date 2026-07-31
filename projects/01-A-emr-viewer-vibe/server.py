#!/usr/bin/env python3
"""Local EMR viewer server for the MIMIC-IV demo dataset."""

import csv
import gzip
import json
import os
import zipfile
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from io import TextIOWrapper
from pathlib import Path
from urllib.parse import unquote, urlparse


PROJECT_ROOT = Path(__file__).parent
DEFAULT_ZIP_PATH = PROJECT_ROOT / "data" / "mimic-iv-clinical-database-demo-2.2.zip"
CORE_ADMISSION_FIELDS = (
    "hadm_id",
    "admittime",
    "dischtime",
    "admission_type",
    "admission_location",
    "discharge_location",
)
CORE_PRESCRIPTION_FIELDS = (
    "pharmacy_id",
    "hadm_id",
    "drug",
    "prod_strength",
    "dose_val_rx",
    "dose_unit_rx",
    "route",
    "starttime",
    "stoptime",
)
CORE_LAB_FIELDS = (
    "labevent_id",
    "hadm_id",
    "charttime",
    "label",
    "fluid",
    "category",
    "value",
    "valuenum",
    "valueuom",
    "ref_range_lower",
    "ref_range_upper",
    "flag",
)


def _read_gz_csv(archive, member_name):
    with archive.open(member_name) as compressed:
        with gzip.GzipFile(fileobj=compressed) as uncompressed:
            with TextIOWrapper(uncompressed, encoding="utf-8", newline="") as text:
                yield from csv.DictReader(text)


def load_dataset(zip_path=DEFAULT_ZIP_PATH):
    """Load the patient and admission tables from the untouched source ZIP."""
    patients = {}
    admissions = {}
    diagnosis_names = {}
    diagnoses = {}
    prescriptions = {}
    lab_items = {}
    labs = {}

    patient_member = "mimic-iv-clinical-database-demo-2.2/hosp/patients.csv.gz"
    admission_member = "mimic-iv-clinical-database-demo-2.2/hosp/admissions.csv.gz"
    diagnosis_member = "mimic-iv-clinical-database-demo-2.2/hosp/diagnoses_icd.csv.gz"
    diagnosis_dictionary_member = "mimic-iv-clinical-database-demo-2.2/hosp/d_icd_diagnoses.csv.gz"
    prescription_member = "mimic-iv-clinical-database-demo-2.2/hosp/prescriptions.csv.gz"
    lab_member = "mimic-iv-clinical-database-demo-2.2/hosp/labevents.csv.gz"
    lab_dictionary_member = "mimic-iv-clinical-database-demo-2.2/hosp/d_labitems.csv.gz"

    with zipfile.ZipFile(zip_path) as archive:
        for row in _read_gz_csv(archive, patient_member):
            row["subject_id"] = str(row["subject_id"])
            row["anchor_age"] = int(row["anchor_age"])
            patients[row["subject_id"]] = row

        for row in _read_gz_csv(archive, admission_member):
            subject_id = str(row["subject_id"])
            admissions.setdefault(subject_id, []).append(row)

        for row in _read_gz_csv(archive, diagnosis_dictionary_member):
            diagnosis_names[(row["icd_code"], row["icd_version"])] = row["long_title"]

        for row in _read_gz_csv(archive, diagnosis_member):
            subject_id = str(row["subject_id"])
            diagnoses.setdefault(subject_id, []).append(row)

        for row in _read_gz_csv(archive, prescription_member):
            subject_id = str(row["subject_id"])
            prescriptions.setdefault(subject_id, []).append(row)

        for row in _read_gz_csv(archive, lab_dictionary_member):
            lab_items[row["itemid"]] = row

        for row in _read_gz_csv(archive, lab_member):
            subject_id = str(row["subject_id"])
            labs.setdefault(subject_id, []).append(row)

    return {
        "patients": patients,
        "admissions": admissions,
        "diagnosis_names": diagnosis_names,
        "diagnoses": diagnoses,
        "prescriptions": prescriptions,
        "lab_items": lab_items,
        "labs": labs,
    }


def patient_payload(dataset, subject_id):
    """Return the public viewer payload for one subject ID, or None if absent."""
    subject_id = str(subject_id).strip()
    patient = dataset["patients"].get(subject_id)
    if patient is None:
        return None

    patient_fields = {
        "subject_id": patient["subject_id"],
        "gender": patient["gender"],
        "anchor_age": patient["anchor_age"],
        "anchor_year_group": patient["anchor_year_group"],
        "dod": patient["dod"] or None,
    }
    patient_admissions = [
        {field: row.get(field) or None for field in CORE_ADMISSION_FIELDS}
        for row in dataset["admissions"].get(subject_id, [])
    ]
    patient_admissions.sort(key=lambda row: row["admittime"] or "")
    return {"patient": patient_fields, "admissions": patient_admissions}


def domain_payload(dataset, subject_id):
    """Return diagnosis, prescription, and lab data for one subject ID."""
    subject_id = str(subject_id).strip()
    if subject_id not in dataset["patients"]:
        return None

    diagnosis_rows = []
    for row in dataset["diagnoses"].get(subject_id, []):
        diagnosis_rows.append(
            {
                "hadm_id": row["hadm_id"],
                "seq_num": row["seq_num"],
                "icd_code": row["icd_code"],
                "icd_version": row["icd_version"],
                "icd_name": dataset["diagnosis_names"].get(
                    (row["icd_code"], row["icd_version"]), "Unknown diagnosis"
                ),
            }
        )

    prescription_rows = []
    for row in dataset["prescriptions"].get(subject_id, []):
        prescription_rows.append({field: row.get(field) or None for field in CORE_PRESCRIPTION_FIELDS})

    lab_rows = []
    for row in dataset["labs"].get(subject_id, []):
        item = dataset["lab_items"].get(row["itemid"], {})
        display_value = row["value"]
        if display_value in (None, "", "___"):
            display_value = row["valuenum"] or None
        lab_rows.append(
            {
                "labevent_id": row["labevent_id"],
                "hadm_id": row["hadm_id"] or None,
                "charttime": row["charttime"],
                "label": item.get("label", "Unknown lab test"),
                "fluid": item.get("fluid"),
                "category": item.get("category"),
                "value": display_value,
                "valuenum": row["valuenum"] or None,
                "valueuom": row["valueuom"] or None,
                "ref_range_lower": row["ref_range_lower"] or None,
                "ref_range_upper": row["ref_range_upper"] or None,
                "flag": row["flag"] or None,
            }
        )

    return {
        "counts": {
            "diagnoses": len(diagnosis_rows),
            "prescriptions": len(prescription_rows),
            "labs": len(lab_rows),
        },
        "diagnoses": diagnosis_rows,
        "prescriptions": prescription_rows,
        "labs": lab_rows,
    }


def timeline_payload(dataset, subject_id):
    """Merge the patient's encounters and clinical domains into a sorted event stream."""
    subject_id = str(subject_id).strip()
    if subject_id not in dataset["patients"]:
        return None

    events = []
    admissions = dataset["admissions"].get(subject_id, [])
    admission_by_id = {row["hadm_id"]: row for row in admissions}

    for admission in admissions:
        events.append(
            {
                "event_type": "admission",
                "event_kind": "admitted",
                "occurred_at": admission["admittime"],
                "hadm_id": admission["hadm_id"],
                "title": "Admitted",
                "subtitle": admission["admission_type"],
                "detail": admission["admission_location"],
                "date_source": "admission",
            }
        )
        events.append(
            {
                "event_type": "admission",
                "event_kind": "discharged",
                "occurred_at": admission["dischtime"],
                "hadm_id": admission["hadm_id"],
                "title": "Discharged",
                "subtitle": admission["discharge_location"],
                "detail": admission["admission_type"],
                "date_source": "admission",
            }
        )

    for row in dataset["diagnoses"].get(subject_id, []):
        encounter = admission_by_id.get(row["hadm_id"], {})
        events.append(
            {
                "event_type": "diagnosis",
                "event_kind": "diagnosis",
                "occurred_at": encounter.get("admittime"),
                "hadm_id": row["hadm_id"],
                "title": dataset["diagnosis_names"].get(
                    (row["icd_code"], row["icd_version"]), "Unknown diagnosis"
                ),
                "subtitle": f"ICD-{row['icd_version']} · {row['icd_code']}",
                "detail": "Date inherited from admission",
                "date_source": "admission",
            }
        )

    for row in dataset["prescriptions"].get(subject_id, []):
        dose = " ".join(value for value in (row["dose_val_rx"], row["dose_unit_rx"]) if value)
        events.append(
            {
                "event_type": "prescription",
                "event_kind": "medication_order",
                "occurred_at": row["starttime"],
                "hadm_id": row["hadm_id"],
                "title": row["drug"],
                "subtitle": row["prod_strength"] or dose or row["route"],
                "detail": f"Route: {row['route'] or '—'} · Stop: {row['stoptime'] or '—'}",
                "date_source": "starttime",
            }
        )

    for row in dataset["labs"].get(subject_id, []):
        item = dataset["lab_items"].get(row["itemid"], {})
        display_value = row["value"]
        if display_value in (None, "", "___"):
            display_value = row["valuenum"] or None
        value_with_unit = " ".join(value for value in (display_value, row["valueuom"]) if value)
        reference = " – ".join(value for value in (row["ref_range_lower"], row["ref_range_upper"]) if value)
        events.append(
            {
                "event_type": "lab",
                "event_kind": "lab_result",
                "occurred_at": row["charttime"],
                "hadm_id": row["hadm_id"] or None,
                "title": item.get("label", "Unknown lab test"),
                "subtitle": value_with_unit or "—",
                "detail": f"Reference: {reference or '—'}",
                "flag": row["flag"] or None,
                "date_source": "charttime",
            }
        )

    priority = {"admission": 0, "diagnosis": 1, "prescription": 2, "lab": 3}
    events.sort(key=lambda event: (event["occurred_at"] or "9999", priority[event["event_type"]]))
    timestamps = [event["occurred_at"] for event in events if event["occurred_at"]]
    return {
        "counts": {
            "admissions": sum(1 for event in events if event["event_type"] == "admission"),
            "diagnoses": sum(1 for event in events if event["event_type"] == "diagnosis"),
            "prescriptions": sum(1 for event in events if event["event_type"] == "prescription"),
            "labs": sum(1 for event in events if event["event_type"] == "lab"),
        },
        "date_range": {"start": min(timestamps) if timestamps else None, "end": max(timestamps) if timestamps else None},
        "events": events,
    }


class ViewerHandler(SimpleHTTPRequestHandler):
    """Serve the viewer and its patient lookup endpoint."""

    def do_GET(self):  # noqa: N802 - required by BaseHTTPRequestHandler
        parsed = urlparse(self.path)
        path = unquote(parsed.path)

        if path.startswith("/api/patients/") and path.endswith("/timeline"):
            subject_id = path.removeprefix("/api/patients/").removesuffix("/timeline").strip("/")
            result = timeline_payload(self.server.dataset, subject_id)
            if result is None:
                self._send_json({"error": "Patient not found."}, 404)
                return
            self._send_json(result, 200)
            return

        if path.startswith("/api/patients/") and path.endswith("/domains"):
            subject_id = path.removeprefix("/api/patients/").removesuffix("/domains").strip("/")
            result = domain_payload(self.server.dataset, subject_id)
            if result is None:
                self._send_json({"error": "Patient not found."}, 404)
                return
            self._send_json(result, 200)
            return

        if path.startswith("/api/patients/"):
            subject_id = path.removeprefix("/api/patients/").strip("/")
            if not subject_id:
                self._send_json({"error": "Patient ID is required."}, 400)
                return
            result = patient_payload(self.server.dataset, subject_id)
            if result is None:
                self._send_json({"error": "Patient not found."}, 404)
                return
            self._send_json(result, 200)
            return

        if path == "/":
            self.path = "/index.html"
        return super().do_GET()

    def _send_json(self, payload, status):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        print(f"{self.address_string()} - {format % args}")


def create_server(host="127.0.0.1", port=8000, zip_path=DEFAULT_ZIP_PATH):
    dataset = load_dataset(zip_path)
    handler = partial(ViewerHandler, directory=str(PROJECT_ROOT))
    server = ThreadingHTTPServer((host, port), handler)
    server.dataset = dataset
    return server


def main():
    host = os.environ.get("EMR_HOST", "127.0.0.1")
    port = int(os.environ.get("EMR_PORT", "8000"))
    server = create_server(host=host, port=port)
    print(f"EMR Viewer running at http://{host}:{port}")
    print("Educational/research prototype only; not for clinical decision-making.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping EMR Viewer.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
