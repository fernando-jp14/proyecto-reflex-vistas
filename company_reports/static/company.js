
const API_BASE = "http://127.0.0.1:8000/api/company/company/";

// Función para obtener el CSRF token de la cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

// Mostrar empresas al cargar
document.addEventListener("DOMContentLoaded", loadCompanies);

function loadCompanies() {
    fetch(API_BASE)
        .then(res => res.json())
        .then(data => {
            const list = document.getElementById("companyList");
            list.innerHTML = "";
            data.data.forEach(c => {
                const card = document.createElement("div");
                card.classList.add("company-card");
                card.innerHTML = `
                    <div>
                        <strong>ID:</strong> ${c.id} <br>
                        <strong>Nombre:</strong> ${c.company_name} <br>
                        <small>Creado: ${new Date(c.created_at).toLocaleString()}</small>
                    </div>
                    <div>
                        ${c.has_logo ? `<img src="${c.logo_url}" alt="Logo">` : "Sin logo"}
                    </div>
                `;
                list.appendChild(card);
            });
        });
}

// Crear empresa
document.getElementById("createCompanyForm").addEventListener("submit", e => {
    e.preventDefault();
    const name = document.getElementById("companyName").value;

    fetch(API_BASE, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({ company_name: name })
    })
    .then(res => res.json())
    .then(() => loadCompanies());
});

// Subir logo
document.getElementById("uploadLogoForm").addEventListener("submit", e => {
    e.preventDefault();
    const id = document.getElementById("uploadId").value;
    const logo = document.getElementById("uploadLogo").files[0];

    let formData = new FormData();
    formData.append("logo", logo);

    fetch(`${API_BASE}${id}/upload_logo/`, {
        method: "POST",
        body: formData,
        headers: {
            'X-CSRFToken': csrftoken
        }
    })
    .then(res => res.json())
    .then(() => loadCompanies());
});

// Eliminar logo
document.getElementById("deleteLogoForm").addEventListener("submit", e => {
    e.preventDefault();
    const id = document.getElementById("deleteId").value;

    fetch(`${API_BASE}${id}/delete_logo/`, {
        method: "DELETE",
        headers: {
            'X-CSRFToken': csrftoken
        }
    })
    .then(res => res.json())
    .then(() => loadCompanies());
});

// Actualizar empresa (nombre + logo opcional)
document.getElementById("updateCompanyForm").addEventListener("submit", e => {
    e.preventDefault();
    const id = document.getElementById("updateId").value;
    const name = document.getElementById("updateName").value;
    const logo = document.getElementById("updateLogo").files[0];

    let formData = new FormData();
    if (name) formData.append("company_name", name);
    if (logo) formData.append("company_logo", logo);

    fetch(`${API_BASE}${id}/`, {
        method: "PUT",
        body: formData,
        headers: {
            'X-CSRFToken': csrftoken
        }
    })
    .then(res => res.json())
    .then(() => loadCompanies());
});
