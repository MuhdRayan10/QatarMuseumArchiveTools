let rawData = null;

// fetching data once loaded
fetch("/api/data")
  .then(res => res.json())
  .then(data => {
    rawData = data;
    populateMonths(Object.keys(data));
    updateChart();
  });

function populateMonths(months) {
  const sel = document.getElementById("monthSelect");
  sel.innerHTML = months.map(m => `<option>${m}</option>`).join("");
  sel.addEventListener("change", updateChart);
  document.getElementById("viewToggle")
    .addEventListener("change", updateChart);
}

function updateChart() {
  const month = document.getElementById("monthSelect").value;
  const view  = document.getElementById("viewToggle").value;
  if (!rawData || !month) return;

  let labels, series;
  if (view === "weekly") {
    labels = Object.keys(rawData[month]);
    series = labels.map(week => rawData[month][week]);
  } else {
    
    // monthly: sum each type across all weeks
    labels = ["images","videos","audio","documents"];
    const acc = {images:0,videos:0,audio:0,documents:0};
    Object.values(rawData[month]).forEach(week => {
      labels.forEach(type => acc[type] += week[type]);
    });
    series = [acc];
  }

  const ctx = document.getElementById("chartCanvas").getContext("2d");
  if (window._qmChart) window._qmChart.destroy();
  window._qmChart = new Chart(ctx, {
    type: view==="weekly"?"bar":"pie",
    data: {
      labels: view==="weekly"?labels:labels,
      datasets: [{
        label: view==="weekly"?`Weekly breakdown for ${month}`:"Monthly Totals",
        data: view==="weekly"?labels.map(w=>rawData[month][w][labels[0]]):labels.map(t=>series[0][t]),
        backgroundColor: [
          "#4e79a7","#f28e2b","#e15759","#76b7b2"
        ]
      }]
    },
    options: { responsive: true }
  });

  // update total assets
  const total = view==="weekly"
    ? labels.reduce((sum,w)=> sum + Object.values(rawData[month][w]).reduce((a,b)=>a+b,0),0)
    : labels.reduce((sum,t)=> sum + series[0][t],0);
  document.getElementById("totalAssets").innerText = total;
}
