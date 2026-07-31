import json
import unittest
from pathlib import Path

from server import domain_payload, load_dataset, patient_payload, timeline_payload


PROJECT_ROOT = Path(__file__).parent
ZIP_PATH = PROJECT_ROOT / "data" / "mimic-iv-clinical-database-demo-2.2.zip"


class DatasetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dataset = load_dataset(ZIP_PATH)

    def test_patient_10000032_contains_deidentified_profile(self):
        result = patient_payload(self.dataset, "10000032")

        self.assertIsNotNone(result)
        self.assertEqual(result["patient"]["subject_id"], "10000032")
        self.assertEqual(result["patient"]["gender"], "F")
        self.assertEqual(result["patient"]["anchor_age"], 52)
        self.assertEqual(len(result["admissions"]), 4)

    def test_patient_10000032_admissions_are_sorted_and_use_core_fields(self):
        result = patient_payload(self.dataset, "10000032")

        admissions = result["admissions"]
        self.assertEqual(
            [row["admittime"] for row in admissions],
            [
                "2180-05-06 22:23:00",
                "2180-06-26 18:27:00",
                "2180-07-23 12:35:00",
                "2180-08-05 23:44:00",
            ],
        )
        self.assertEqual(
            set(admissions[0]),
            {
                "hadm_id",
                "admittime",
                "dischtime",
                "admission_type",
                "admission_location",
                "discharge_location",
            },
        )

    def test_unknown_patient_returns_none(self):
        self.assertIsNone(patient_payload(self.dataset, "99999999"))

    def test_patient_domain_payload_resolves_diagnosis_names(self):
        result = domain_payload(self.dataset, "10000032")

        self.assertEqual(result["counts"], {"diagnoses": 39, "prescriptions": 81, "labs": 623})
        diagnosis = result["diagnoses"][0]
        self.assertEqual(diagnosis["icd_code"], "2761")
        self.assertEqual(diagnosis["icd_name"], "Hyposmolality and/or hyponatremia")
        self.assertEqual(diagnosis["hadm_id"], "22841357")

    def test_patient_domain_payload_includes_prescription_and_lab_labels(self):
        result = domain_payload(self.dataset, "10000032")

        prescription = result["prescriptions"][0]
        self.assertEqual(prescription["drug"], "Tiotropium Bromide")
        self.assertIn("route", prescription)
        self.assertIn("starttime", prescription)

        lab = result["labs"][0]
        self.assertEqual(lab["label"], "Sodium")
        self.assertEqual(lab["value"], "124")
        self.assertEqual(lab["flag"], "abnormal")

    def test_unknown_patient_has_no_domain_payload(self):
        self.assertIsNone(domain_payload(self.dataset, "99999999"))

    def test_patient_timeline_merges_and_sorts_all_event_domains(self):
        result = timeline_payload(self.dataset, "10000032")

        self.assertEqual(result["counts"], {"admissions": 8, "diagnoses": 39, "prescriptions": 81, "labs": 623})
        self.assertEqual(len(result["events"]), 751)
        timestamps = [event["occurred_at"] for event in result["events"]]
        self.assertEqual(timestamps, sorted(timestamps))
        self.assertEqual(result["events"][0]["event_type"], "lab")
        self.assertEqual(result["events"][0]["occurred_at"], "2180-03-23 11:51:00")

    def test_timeline_places_diagnosis_at_admission_time_with_source_note(self):
        result = timeline_payload(self.dataset, "10000032")
        diagnosis = next(
            event
            for event in result["events"]
            if event["event_type"] == "diagnosis"
            and event["title"] == "Hyposmolality and/or hyponatremia"
        )

        self.assertEqual(diagnosis["occurred_at"], "2180-06-26 18:27:00")
        self.assertEqual(diagnosis["date_source"], "admission")
        self.assertEqual(diagnosis["title"], "Hyposmolality and/or hyponatremia")

    def test_unknown_patient_has_no_timeline(self):
        self.assertIsNone(timeline_payload(self.dataset, "99999999"))


if __name__ == "__main__":
    unittest.main()
