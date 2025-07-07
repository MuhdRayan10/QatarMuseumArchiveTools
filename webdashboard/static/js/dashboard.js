let rawData = {};

// on load, fetch the JSON
fetch("/api/data")
  .then(res => res.json())
  .then(data => {
    rawData = data;
    initControls(Object.keys(data));
    updateChart();
  });

function initControls(months) {
  const monthSel = document.getElementById("monthSelect");
  monthSel.innerHTML = months.map(m => `<option>${m}</option>`).join("");
  monthSel.addEventListener("change", updateChart);
  document.getElementById("viewToggle")
    .addEventListener("change", updateChart);
}

function updateChart() {
  const month = document.getElementById("monthSelect").value;
  const view  = document.getElementById("viewToggle").value;
  if (!rawData[month]) return;

  const monthData = rawData[month];
  const assetTypes = ["images","videos","audio","documents"];
  let labels = [], data = [];

  if (view === "weekly") {
    // one bar per week, sum all asset-types for that week
    labels = Object.keys(monthData);
    data = labels.map(week => {
      const wk = monthData[week];
      return Object.values(assetTypes).reduce((sum, type) =>
        sum + Number(wk[type] || 0), 0
      , 0);
    });
  } else {
    // pie: one slice per asset-type, sum that type across all weeks
    labels = assetTypes;
    data = assetTypes.map(type =>
      Object.values(monthData).reduce((sum, wk) =>
        sum + Number(wk[type] || 0)
      , 0)
    );
  }

  // compute total
  const total = data.reduce((s, v) => s + v, 0);

  // render chart
  const ctx = document.getElementById("chartCanvas").getContext("2d");
  if (window._qmChart) window._qmChart.destroy();
  window._qmChart = new Chart(ctx, {
    type: view === "weekly" ? "bar" : "pie",
    data: {
      labels,
      datasets: [{
        label: view === "weekly"
          ? `Total per week in ${month}`
          : `Total per asset type in ${month}`,
        data,
        backgroundColor: [
          "#4e79a7","#f28e2b","#e15759","#76b7b2"
        ]
      }]
    },
    options: { responsive: true }
  });

  // update totals panel
  document.getElementById("totalAssets").innerText = total;
}
