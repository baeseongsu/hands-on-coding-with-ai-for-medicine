const form = document.querySelector("#search-form");
const subjectInput = document.querySelector("#subject-id");
const searchButton = document.querySelector("#search-button");
const message = document.querySelector("#message");
const recordView = document.querySelector("#record-view");
const domainFilter = document.querySelector("#domain-hadm-filter");
const abnormalOnly = document.querySelector("#abnormal-only");
const timelineHadmFilter = document.querySelector("#timeline-hadm-filter");
let domainPayload = null;
let timelinePayload = null;
let activeDomain = "diagnoses";
let activeTimelineFilter = "all";

const byId = (id) => document.querySelector(`#${id}`);

function setMessage(text, kind = "") {
  message.textContent = text;
  message.className = `message ${kind}`.trim();
}

function escapeHtml(value) {
  return String(value ?? "—")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function formatDate(value) {
  if (!value) return "—";
  const [date, time] = value.split(" ");
  return time ? `${escapeHtml(date)}<span class="date-time">${escapeHtml(time)}</span>` : escapeHtml(date);
}

function formatValue(value) {
  return escapeHtml(value || "—");
}

function renderRecord(payload) {
  const { patient, admissions } = payload;
  byId("patient-id-badge").textContent = `ID ${patient.subject_id}`;
  byId("patient-label").textContent = `Patient ${patient.subject_id}`;
  byId("patient-demographics").textContent = `${patient.gender} · Anchor age ${patient.anchor_age} · ${patient.anchor_year_group}`;
  byId("patient-gender").textContent = patient.gender || "—";
  byId("patient-age").textContent = patient.anchor_age ?? "—";
  byId("patient-year-group").textContent = patient.anchor_year_group || "—";
  byId("patient-dod").textContent = patient.dod || "—";
  byId("admission-count").textContent = `${admissions.length} record${admissions.length === 1 ? "" : "s"}`;

  const body = byId("admissions-body");
  body.replaceChildren();
  admissions.forEach((admission) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td><span class="admission-id">${formatValue(admission.hadm_id)}</span></td>
      <td>${formatDate(admission.admittime)}</td>
      <td>${formatDate(admission.dischtime)}</td>
      <td><span class="type-chip">${formatValue(admission.admission_type)}</span></td>
      <td>${formatValue(admission.admission_location)}</td>
      <td>${formatValue(admission.discharge_location)}</td>`;
    body.appendChild(row);
  });

  byId("no-admissions").hidden = admissions.length !== 0;
  domainFilter.replaceChildren(new Option("All admissions", "all"));
  admissions.forEach((admission) => {
    domainFilter.appendChild(new Option(admission.hadm_id, admission.hadm_id));
  });
  recordView.hidden = false;
}

function renderDomainCards(counts) {
  byId("diagnosis-count").textContent = counts.diagnoses;
  byId("prescription-count").textContent = counts.prescriptions;
  byId("lab-count").textContent = counts.labs;
}

function filteredRows(kind) {
  if (!domainPayload) return [];
  const selectedAdmission = domainFilter.value;
  const rows = domainPayload[kind].filter((row) => selectedAdmission === "all" || row.hadm_id === selectedAdmission);
  if (kind !== "labs" || !abnormalOnly.checked) return rows;
  return rows.filter((row) => row.flag && row.flag.toLowerCase() === "abnormal");
}

function renderDiagnoses() {
  const body = byId("diagnoses-body");
  body.replaceChildren();
  filteredRows("diagnoses").forEach((diagnosis) => {
    const row = document.createElement("tr");
    row.innerHTML = `<td><strong class="domain-primary">${formatValue(diagnosis.icd_name)}</strong></td>
      <td><span class="code-chip">${formatValue(diagnosis.icd_code)}</span></td>
      <td>${formatValue(diagnosis.icd_version)}</td>
      <td>${formatValue(diagnosis.hadm_id)}</td>`;
    body.appendChild(row);
  });
}

function renderPrescriptions() {
  const body = byId("prescriptions-body");
  body.replaceChildren();
  filteredRows("prescriptions").forEach((prescription) => {
    const dose = [prescription.dose_val_rx, prescription.dose_unit_rx].filter(Boolean).join(" ");
    const row = document.createElement("tr");
    row.innerHTML = `<td><strong class="domain-primary">${formatValue(prescription.drug)}</strong></td>
      <td>${formatValue(prescription.prod_strength)}</td>
      <td>${formatValue(dose)}</td>
      <td><span class="type-chip">${formatValue(prescription.route)}</span></td>
      <td>${formatDate(prescription.starttime)}</td>
      <td>${formatDate(prescription.stoptime)}</td>
      <td>${formatValue(prescription.hadm_id)}</td>`;
    body.appendChild(row);
  });
}

function renderLabs() {
  const body = byId("labs-body");
  body.replaceChildren();
  filteredRows("labs").forEach((lab) => {
    const range = [lab.ref_range_lower, lab.ref_range_upper].filter(Boolean).join(" – ");
    const result = [lab.value, lab.valueuom].filter(Boolean).join(" ");
    const flag = lab.flag ? `<span class="flag-chip abnormal">${formatValue(lab.flag)}</span>` : '<span class="flag-chip">Normal</span>';
    const row = document.createElement("tr");
    row.innerHTML = `<td><strong class="domain-primary">${formatValue(lab.label)}</strong><span class="secondary-text">${formatValue(lab.fluid)}</span></td>
      <td>${formatValue(result)}</td>
      <td>${formatValue(range)}</td>
      <td>${flag}</td>
      <td>${formatDate(lab.charttime)}</td>
      <td>${formatValue(lab.hadm_id)}</td>`;
    body.appendChild(row);
  });
}

function renderActiveDomain() {
  document.querySelectorAll("[data-domain-panel]").forEach((panel) => {
    panel.hidden = panel.dataset.domainPanel !== activeDomain;
  });
  document.querySelectorAll("[data-domain-tab]").forEach((tab) => {
    tab.classList.toggle("active", tab.dataset.domainTab === activeDomain);
  });
  if (activeDomain === "diagnoses") renderDiagnoses();
  if (activeDomain === "prescriptions") renderPrescriptions();
  if (activeDomain === "labs") renderLabs();
  const visibleRows = filteredRows(activeDomain).length;
  byId("domain-result-count").textContent = `${visibleRows} displayed`;
}

function renderDomains(payload) {
  domainPayload = payload;
  renderDomainCards(payload.counts);
  renderActiveDomain();
}

function timelineFilteredEvents() {
  if (!timelinePayload) return [];
  return timelinePayload.events.filter((event) => {
    const typeMatches = activeTimelineFilter === "all" || event.event_type === activeTimelineFilter;
    const admissionMatches = timelineHadmFilter.value === "all" || event.hadm_id === timelineHadmFilter.value;
    return typeMatches && admissionMatches;
  });
}

function renderTimeline() {
  if (!timelinePayload) return;
  const events = timelineFilteredEvents();
  const list = byId("timeline-list");
  list.replaceChildren();
  byId("timeline-empty").hidden = events.length !== 0;
  byId("timeline-count").textContent = `${events.length} displayed · ${timelinePayload.events.length} total`;
  byId("timeline-range").textContent = `${timelinePayload.date_range.start || "—"} → ${timelinePayload.date_range.end || "—"}`;

  const groups = new Map();
  events.forEach((event) => {
    const date = event.occurred_at ? event.occurred_at.slice(0, 10) : "Unknown date";
    if (!groups.has(date)) groups.set(date, []);
    groups.get(date).push(event);
  });

  groups.forEach((groupEvents, date) => {
    const group = document.createElement("section");
    group.className = "timeline-day";
    group.innerHTML = `<div class="timeline-date"><strong>${escapeHtml(date)}</strong><span>${groupEvents.length} event${groupEvents.length === 1 ? "" : "s"}</span></div>`;
    const eventList = document.createElement("div");
    eventList.className = "timeline-events";
    groupEvents.forEach((event) => {
      const item = document.createElement("article");
      item.className = `timeline-event event-${event.event_type}`;
      const flag = event.flag ? `<span class="flag-chip abnormal">${formatValue(event.flag)}</span>` : "";
      const sourceNote = event.date_source === "admission" && event.event_type === "diagnosis" ? '<span class="date-source">Admission time</span>' : "";
      item.innerHTML = `<div class="timeline-marker"></div><div class="timeline-event-content"><div class="timeline-event-top"><time>${formatDate(event.occurred_at)}</time><span class="event-type-label">${escapeHtml(event.event_type)}</span></div><h3>${formatValue(event.title)}</h3><p>${formatValue(event.subtitle)} ${flag}</p><div class="timeline-detail">${formatValue(event.detail)} ${sourceNote} ${event.hadm_id ? `<span class="encounter-chip">${formatValue(event.hadm_id)}</span>` : ""}</div></div>`;
      eventList.appendChild(item);
    });
    group.appendChild(eventList);
    list.appendChild(group);
  });
}

function renderTimelineAdmissions(admissions) {
  timelineHadmFilter.replaceChildren(new Option("All admissions", "all"));
  admissions.forEach((admission) => timelineHadmFilter.appendChild(new Option(admission.hadm_id, admission.hadm_id)));
}

async function searchPatient(subjectId) {
  const normalizedId = subjectId.trim();
  if (!normalizedId) {
    recordView.hidden = true;
    setMessage("환자 ID를 입력해 주세요.", "error");
    subjectInput.focus();
    return;
  }

  searchButton.disabled = true;
  searchButton.querySelector("span").textContent = "Loading…";
  setMessage("환자 기록을 불러오는 중입니다.", "loading");

  try {
    const [patientResponse, domainResponse, timelineResponse] = await Promise.all([
      fetch(`/api/patients/${encodeURIComponent(normalizedId)}`),
      fetch(`/api/patients/${encodeURIComponent(normalizedId)}/domains`),
      fetch(`/api/patients/${encodeURIComponent(normalizedId)}/timeline`),
    ]);
    const payload = await patientResponse.json();
    if (!patientResponse.ok || !domainResponse.ok || !timelineResponse.ok) {
      recordView.hidden = true;
      setMessage("해당 환자를 찾을 수 없습니다. ID를 확인해 주세요.", "error");
      return;
    }
    renderRecord(payload);
    renderDomains(await domainResponse.json());
    timelinePayload = await timelineResponse.json();
    renderTimelineAdmissions(payload.admissions);
    renderTimeline();
    setMessage(`환자 ${normalizedId}의 기록을 불러왔습니다.`, "success");
  } catch (error) {
    recordView.hidden = true;
    setMessage("서버에 연결할 수 없습니다. 로컬 서버 상태를 확인해 주세요.", "error");
  } finally {
    searchButton.disabled = false;
    searchButton.querySelector("span").textContent = "Search patient";
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  searchPatient(subjectInput.value);
});

document.querySelectorAll("[data-domain-tab]").forEach((tab) => {
  tab.addEventListener("click", () => {
    activeDomain = tab.dataset.domainTab;
    renderActiveDomain();
  });
});

domainFilter.addEventListener("change", renderActiveDomain);
abnormalOnly.addEventListener("change", renderActiveDomain);
timelineHadmFilter.addEventListener("change", renderTimeline);
document.querySelectorAll("[data-timeline-filter]").forEach((filter) => {
  filter.addEventListener("click", () => {
    activeTimelineFilter = filter.dataset.timelineFilter;
    document.querySelectorAll("[data-timeline-filter]").forEach((button) => button.classList.toggle("active", button === filter));
    renderTimeline();
  });
});
searchPatient(subjectInput.value);
