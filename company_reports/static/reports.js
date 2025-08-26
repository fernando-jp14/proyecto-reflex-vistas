function downloadCashPDF() {
    const date = document.getElementById("date").value || new Date().toISOString().split("T")[0];
    window.open(`/api/company/exports/pdf/resumen-caja/?date=${date}`, '_blank');
}
async function loadReports() {
    const date = document.getElementById("date").value || new Date().toISOString().split("T")[0];

    // 1️⃣ Citas por terapeuta
    const res1 = await fetch(`/api/company/reports/appointments-per-therapist/?date=${date}`);
    const data1 = await res1.json();

    const appointmentsTable = document.querySelector("#appointmentsTable tbody");
    appointmentsTable.innerHTML = "";
    if (data1.therapists_appointments.length === 0) {
        appointmentsTable.innerHTML = `<tr><td colspan="3">Sin datos</td></tr>`;
    } else {
        data1.therapists_appointments.forEach(t => {
            appointmentsTable.innerHTML += `
                <tr>
                    <td>${t.first_name} ${t.last_name_paternal} ${t.last_name_maternal}</td>
                    <td>${t.appointments_count}</td>
                    <td>${t.percentage}%</td>
                </tr>
            `;
        });
    }

    // 2️⃣ Caja diaria
    const res2 = await fetch(`/api/company/reports/daily-cash/?date=${date}`);
    const data2 = await res2.json();

    const cashTable = document.querySelector("#cashTable tbody");
    cashTable.innerHTML = "";
    if (data2.length === 0) {
        cashTable.innerHTML = `<tr><td colspan="3">Sin datos</td></tr>`;
    } else {
        data2.forEach(c => {
            cashTable.innerHTML += `
                <tr>
                    <td>${c.id_cita}</td>
                    <td>S/. ${c.payment}</td>
                    <td>${c.payment_type_name}</td>
                </tr>
            `;
        });
    }

    // 3️⃣ Pacientes por terapeuta
    const res3 = await fetch(`/api/company/reports/patients-by-therapist/?date=${date}`);
    const data3 = await res3.json();

    const patientsDiv = document.getElementById("patientsByTherapist");
    patientsDiv.innerHTML = "";
    if (data3.length === 0) {
        patientsDiv.innerHTML = "<p>Sin datos</p>";
    } else {
        data3.forEach(t => {
            let patientsList = "";
            t.patients.forEach(p => {
                patientsList += `<li>${p.patient} (citas: ${p.appointments})</li>`;
            });

            patientsDiv.innerHTML += `
                <div class="therapist-card">
                    <h3>${t.therapist}</h3>
                    <ul>${patientsList}</ul>
                </div>
            `;
        });
    }
}

// 4️⃣ Citas entre fechas
async function loadAppointmentsBetweenDates() {
    const startDate = document.getElementById("start_date").value;
    const endDate = document.getElementById("end_date").value;

    if (!startDate || !endDate) {
        alert("Por favor selecciona ambas fechas");
        return;
    }

    const res = await fetch(`/api/company/reports/appointments-between-dates/?start_date=${startDate}&end_date=${endDate}`);
    const data = await res.json();

    const appointmentsBetweenTable = document.querySelector("#appointmentsBetweenTable tbody");
    appointmentsBetweenTable.innerHTML = "";
    if (data.length === 0) {
        appointmentsBetweenTable.innerHTML = `<tr><td colspan="6">Sin datos</td></tr>`;
    } else {
        data.forEach(a => {
            appointmentsBetweenTable.innerHTML += `
                <tr>
                    <td>${a.appointment_id}</td>
                    <td>${a.patient}</td>
                    <td>${a.document_number_patient}</td>
                    <td>${a.primary_phone_patient}</td>
                    <td>${a.appointment_date}</td>
                    <td>${a.appointment_hour}</td>
                </tr>
            `;
        });
    }
}

// Exportar citas a Excel
function exportAppointmentsExcel() {
    const startDate = document.getElementById("start_date").value;
    const endDate = document.getElementById("end_date").value;

    if (!startDate || !endDate) {
        alert("Por favor selecciona ambas fechas antes de exportar");
        return;
    }

    // Abrir el enlace en el navegador para descargar el archivo
    window.location.href = `/api/company/exports/excel/citas-rango/?start_date=${startDate}&end_date=${endDate}`;
}

function downloadAppointmentsPDF() {
        const date = document.getElementById("date").value || new Date().toISOString().split("T")[0];
        window.open(`/api/company/exports/pdf/citas-terapeuta/?date=${date}`, '_blank');
    }

function downloadPatientsByTherapistPDF() {
    const date = document.getElementById("date").value || new Date().toISOString().split("T")[0];
    window.open(`/api/company/exports/pdf/pacientes-terapeuta/?date=${date}`, '_blank');
}

// Cargar por defecto con la fecha de hoy
window.onload = loadReports;


