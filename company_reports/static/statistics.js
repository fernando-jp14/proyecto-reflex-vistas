// Guardamos referencias a instancias Chart para destruirlas al recargar
let chartIngresos = null;
let chartSesiones = null;
let chartPagos = null;
let chartPacientes = null;

const $ = (sel) => document.querySelector(sel);

function toCurrency(n){
  const num = Number(n ?? 0);
  return new Intl.NumberFormat('es-PE',{style:'currency',currency:'PEN',maximumFractionDigits:2}).format(num);
}

function todayISO(){ return new Date().toISOString().slice(0,10); }

// Carga inicial
window.addEventListener('DOMContentLoaded', () => {
  // Prefill con últimos 7 días
  const end = todayISO();
  const start = new Date(Date.now() - 6*24*60*60*1000).toISOString().slice(0,10);
  $('#start').value = start;
  $('#end').value = end;

  $('#btn-load').addEventListener('click', loadStats);
  loadStats();
});

async function loadStats(){
  const start = $('#start').value;
  const end = $('#end').value;

  if(!start || !end){
    alert('Selecciona ambas fechas.');
    return;
  }

  const url = `/api/company/reports/statistics/?start=${start}&end=${end}`;

  let data;
  try{
    const res = await fetch(url);
    if(!res.ok) throw new Error(`HTTP ${res.status}`);
    data = await res.json();
  }catch(err){
    console.error('Error obteniendo estadísticas:', err);
    setKpis(null);
    setTerapeutas([]);
    renderIngresos({});
    renderSesiones({});
    renderTiposPago({});
    renderTiposPacientes({});
    return;
  }

  // Métricas
  setKpis(data.metricas);

  // Tabla terapeutas
  setTerapeutas(data.terapeutas || []);

  // Charts
  renderIngresos(data.ingresos || {});
  renderSesiones(data.sesiones || {});
  renderTiposPago(data.tipos_pago || {});
  renderTiposPacientes(data.tipos_pacientes || {});
}

/* --------- KPI Cards --------- */
function setKpis(metricas){
  const pac = metricas?.ttlpacientes ?? 0;
  const ses = metricas?.ttlsesiones ?? 0;
  const gan = metricas?.ttlganancias ?? 0;

  $('#kpi-pacientes').textContent = pac;
  $('#kpi-sesiones').textContent = ses;
  $('#kpi-ingresos').textContent = toCurrency(gan);
}

/* --------- Tabla Terapeutas --------- */
function setTerapeutas(list){
  const tbody = $('#tbl-terapeutas tbody');
  const empty = $('#empty-terapeutas');
  tbody.innerHTML = '';

  if(!list || list.length === 0){
    empty.hidden = false;
    return;
  }
  empty.hidden = true;

  list.forEach((t, idx) => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${idx+1}</td>
      <td>${t.terapeuta}</td>
      <td>${t.sesiones}</td>
      <td>${toCurrency(t.ingresos)}</td>
      <td>${Number(t.raiting ?? t.rating ?? 0).toFixed(1)}</td>
    `;
    tbody.appendChild(tr);
  });
}

/* --------- Charts helpers --------- */
function destroyChart(inst){
  if(inst && typeof inst.destroy === 'function') inst.destroy();
}
function hasValues(obj){
  if(!obj) return false;
  return Object.values(obj).some(v => Number(v) !== 0);
}

/* --------- Chart: Ingresos por día --------- */
function renderIngresos(obj){
  const empty = $('#empty-ingresos');
  destroyChart(chartIngresos);

  const labels = Object.keys(obj || {});
  const values = Object.values(obj || {});

  if(labels.length === 0 || !hasValues(obj)){
    empty.hidden = false;
    return;
  }
  empty.hidden = true;

  const ctx = $('#chart-ingresos').getContext('2d');
  chartIngresos = new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [{ label: 'Ingresos (S/.)', data: values }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: true },
        tooltip: {
          callbacks: {
            label: (item) => `${item.dataset.label}: ${toCurrency(item.raw)}`
          }
        }
      },
      scales: {
        y: { beginAtZero: true, ticks: { callback: v => toCurrency(v) } }
      }
    }
  });
}

/* --------- Chart: Sesiones por día --------- */
function renderSesiones(obj){
  const empty = $('#empty-sesiones');
  destroyChart(chartSesiones);

  const labels = Object.keys(obj || {});
  const values = Object.values(obj || {});

  if(labels.length === 0 || !hasValues(obj)){
    empty.hidden = false;
    return;
  }
  empty.hidden = true;

  const ctx = $('#chart-sesiones').getContext('2d');
  chartSesiones = new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [{ label: 'Sesiones', data: values }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: true } },
      scales: { y: { beginAtZero: true, precision: 0 } }
    }
  });
}

/* --------- Chart: Tipos de pago --------- */
function renderTiposPago(obj){
  const empty = $('#empty-pagos');
  destroyChart(chartPagos);

  const labels = Object.keys(obj || {});
  const values = Object.values(obj || {});

  if(labels.length === 0 || !hasValues(obj)){
    empty.hidden = false;
    return;
  }
  empty.hidden = true;

  const ctx = $('#chart-pagos').getContext('2d');
  chartPagos = new Chart(ctx, {
    type: 'pie',
    data: { labels, datasets: [{ data: values }] },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'bottom' },
        tooltip: {
          callbacks: {
            label: (item) => `${item.label}: ${item.raw}`
          }
        }
      }
    }
  });
}

/* --------- Chart: Tipos de pacientes --------- */
function renderTiposPacientes(obj){
  const empty = $('#empty-pacientes');
  destroyChart(chartPacientes);

  const labels = Object.keys(obj || {});
  const values = Object.values(obj || {});

  if(labels.length === 0){ // aquí pueden venir ceros, igual mostramos
    empty.hidden = false;
    return;
  }
  empty.hidden = true;

  const ctx = $('#chart-pacientes').getContext('2d');
  chartPacientes = new Chart(ctx, {
    type: 'doughnut',
    data: { labels, datasets: [{ data: values }] },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'bottom' },
        tooltip: {
          callbacks: {
            label: (item) => `${item.label}: ${item.raw}`
          }
        }
      }
    }
  });
}
