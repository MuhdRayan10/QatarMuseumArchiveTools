// static/js/dashboard.js

let assets = {};
let previewIndex = 0;

// Fetch the flat list of assets
fetch("/api/data")
  .then(res => res.json())
  .then(json => {
    assets = json.assets || [];
    initPreview();
    initStats();
  })
  .catch(err => console.error("Failed to load assets:", err));

/* ----------- PREVIEW TAB ------------ 
function initPreview() {
  updatePreview();
  document.getElementById("prevBtn")
    .addEventListener("click", () => {
      previewIndex = Math.max(0, previewIndex - 1);
      updatePreview();
    });
  document.getElementById("nextBtn")
    .addEventListener("click", () => {
      previewIndex = Math.min(assets.length - 1, previewIndex + 1);
      updatePreview();
    });
}

function updatePreview() {
  const ctr = document.getElementById("previewCounter");
  ctr.innerText = `${previewIndex + 1} / ${assets.length}`;

  const slot = document.getElementById("previewArea");
  slot.innerHTML = "";
  const a = assets[previewIndex];
  if (!a) {
    slot.textContent = "No asset data available";
    return;
  }

  slot.innerHTML = `
    <div class="card bg-secondary text-white mx-auto" style="max-width: 400px;">
      <div class="card-body">
        <h5 class="card-title">${a.name}</h5>
        <ul class="list-group list-group-flush text-white">
          <li class="list-group-item bg-secondary">Type: ${a.type}</li>
          <li class="list-group-item bg-secondary">Month: ${a.month}</li>
          <li class="list-group-item bg-secondary">Week: ${a.week}</li>
          <li class="list-group-item bg-secondary">URL: ${a.url}</li>
        </ul>
      </div>
    </div>`;
}
*/
/* ----------- STATISTICS TAB ------------ */
function initStats() {
  // build unique month list
  //const months = Array.from(new Set(assets.map(a => a.month)));
  const months = Object.keys(assets["all_data"])
  const sel = document.getElementById("statMonth");
  sel.innerHTML = months.map(m => `<option>${m}</option>`).join("");
  sel.addEventListener("change", renderStats);
  document.getElementById("statView").addEventListener("change", renderStats);

  // trigger first draw
  renderStats();
}

function renderStats() {
  const month = document.getElementById("statMonth").value;
  const view  = document.getElementById("statView").value;

  // filter to this month
  //const monthAssets = assets.filter(a => a.month === month);
  const monthAssets = assets["all_data"][month] || [];

  // Total assets = count of items in this month
  const total = monthAssets.length;
  
  document.getElementById("totalAssets").innerText = total;

  // Build chart data
  let labels = [], data = [];
  if (view === "weekly") {
    labels = Array.from(new Set(monthAssets.map(a => a.week)));
    data = labels.map(wk =>
      monthAssets.filter(a => a.week === wk).length
    );
  } else {
    labels = Array.from(new Set(monthAssets.map(a => a.type)));
    data = labels.map(tp =>
      monthAssets.filter(a => a.type === tp).length
    );
  }

  // Render Chart.js
  const ctx = document.getElementById("statsChart").getContext("2d");
  if (window._dashChart) window._dashChart.destroy();
  window._dashChart = new Chart(ctx, {
    type: view === "weekly" ? "bar" : "pie",
    data: {
      labels,
      datasets: [{
        label: view === "weekly"
               ? `Items per week in ${month}`
               : `Items per type in ${month}`,
        data,
        backgroundColor: [
          "#3498db", "#e74c3c", "#2ecc71", "#f39c12"
        ]
      }]
    },
    options: { responsive: true, indexAxis: view === "weekly" ? "y" : undefined }
  });
}
