// static/js/dashboard.js

let assets = {};
let previewIndex = 0;

// Fetch the flat list of assets
fetch("/api/data")
  .then(res => res.json())
  .then(json => {
    assets = json || {};
    //initPreview();
  })
  .catch(err => console.error("Failed to load assets!!!:", err));

/* ----------- PREVIEW TAB ------------ 
TO DO
*/
/* ----------- STATISTICS TAB ------------ */
function initStats() {
  // set the view to monthly by default
  document.getElementById("statView").value = "monthly";

  // build unique month list
  const months = Object.keys(assets["all_data"]);
  const lastMonth = months[0]; // get the last month

  renderTimeSelector("monthly", months, lastMonth); // pass lastMonth as selected
  document.getElementById("statView").addEventListener("change", function() {
    const view = this.value;
    if (view === "weekly") {
      // Get weeks for the last month by default
      const month = document.getElementById("statMonth")?.value || lastMonth;
      const weeks = Object.keys(assets["all_data"][month] || {});
      renderTimeSelector("weekly", weeks, month, months);
    } else {
      renderTimeSelector("monthly", months, lastMonth);
    }
    renderStats();
  });
  // trigger first draw
  renderStats();
}

function renderTimeSelector(view, options, selectedMonth, months) {
  const container = document.getElementById("statTimeSelector");
  if (view == "monthly") {
    container.innerHTML = `
      <label for="statMonth" class="form-label fw-semibold">Month</label>
      <select id="statMonth" class="form-select">
        ${options.map(m => `<option${m === selectedMonth ? " selected" : ""}>${m}</option>`).join("")}
      </select>`;
    document.getElementById("statMonth").addEventListener("change", renderStats);   
  }
  else {
    container.innerHTML = `
      <label for="statMonth" class="form-label fw-semibold">Month</label>
      <select id="statMonth" class="form-select mb-2">
        ${months.map(m => `<option${m === selectedMonth ? " selected" : ""}>${m}</option>`).join("")}
      </select>
      <label for="statWeek" class="form-label fw-semibold mt-2">Week</label>
      <select id="statWeek" class="form-select">
        ${options.map(w => `<option>${w}</option>`).join("")}
      </select>`;
    document.getElementById("statMonth").addEventListener("change", function () {
      const month = this.value;
      const weeks = Object.keys(assets["all_data"][month] || {});
      renderTimeSelector("weekly", weeks, month, months);
      renderStats();
    });
    document.getElementById("statWeek").addEventListener("change", renderStats);
  }
}

function renderStats() {
  const view  = document.getElementById("statView").value;
  let month, week;
  if (view === "weekly") {
    month = document.getElementById("statMonth").value;
    week = document.getElementById("statWeek").value;
  } else {
    month = document.getElementById("statMonth").value;
  }

  const monthAssets = assets["all_data"][month] || {};
  const month_data = {images:0, videos:0, audio:0, documents:0};
  let sum = 0;
  let data = [];
  let labels = ["Images", "Videos", "Audio", "Documents"];

  if (view === "monthly") {
    for (let w in monthAssets) {
      month_data.images += monthAssets[w].images;
      month_data.videos += monthAssets[w].videos;
      month_data.audio += monthAssets[w].audio;
      month_data.documents += monthAssets[w].documents;
    }
    for (let n in month_data) sum += month_data[n];
    data = [
      month_data.images,
      month_data.videos,
      month_data.audio,
      month_data.documents
    ];
  } else {
    const week_data = monthAssets[week] || {images:0, videos:0, audio:0, documents:0};
    sum = week_data.images + week_data.videos + week_data.audio + week_data.documents;
    data = [
      week_data.images,
      week_data.videos,
      week_data.audio,
      week_data.documents  
    ];
  }
  document.getElementById("totalAssets").innerText = sum;

  // Render Bar Chart
  const ctx = document.getElementById("statsChart").getContext("2d");
  if (window._dashChart) window._dashChart.destroy();
  window._dashChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [{
        label: view === "weekly"
               ? `Items in ${week} of ${month}`
               : `Items in ${month}`,
        data,
        backgroundColor: [
          "#3498db", "#e74c3c", "#2ecc71", "#f39c12"
        ]
      }]
    },
    options: { 
      responsive: true,
      maintainAspectRatio: false
    }
  });

  // Render Pie Chart
  const pieCtx = document.getElementById("pieChart").getContext("2d");
  if (window._pieChart) window._pieChart.destroy();
  window._pieChart = new Chart(pieCtx, {
    type: "pie",
    data: {
      labels,
      datasets: [{
        data,
        backgroundColor: [
          "#3498db", "#e74c3c", "#2ecc71", "#f39c12"
        ]
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'right'
        },
        datalabels: {
          color: '#222',
          font: { weight: 'bold' },
          formatter: (value, context) => {
            const total = context.chart.data.datasets[0].data.reduce((a, b) => a + b, 0);
            if (!total) return '0%';
            const pct = (value / total) * 100;
            return pct.toFixed(1) + '%';
          }
        }
      }
    },
    plugins: [ChartDataLabels]
  });
}

document.addEventListener("DOMContentLoaded", function() {
  // Listen for statistics tab activation
  const statsTab = document.querySelector('button[data-bs-target="#stats"]');
  if (statsTab) {
    statsTab.addEventListener('shown.bs.tab', function () {
      initStats();
    });
  }
});