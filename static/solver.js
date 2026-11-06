
document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('solveBtn').addEventListener('click', solve);
  document.getElementById('problemInput').addEventListener('keydown', function(e) {
    if (e.key === 'Enter') solve();
  });
});

function tryExample(btn) {
  document.getElementById('problemInput').value = btn.dataset.expr;
  solve();
}

async function solve() {
  var problem = document.getElementById('problemInput').value.trim();

  document.getElementById('solveBtn').textContent = 'Solving...';
  document.getElementById('resultArea').style.display = 'none';
  document.getElementById('errorArea').style.display = 'none';

  try {
    var res = await fetch('/solve', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({problem: problem, type: 'auto'})
    });
    var data = await res.json();

    if (data.error) {
      document.getElementById('errorArea').style.display = 'block';
      document.getElementById('errorArea').textContent = data.error;
    } else {
      showResult(data);
    }
  } catch(e) {
    document.getElementById('errorArea').style.display = 'block';
    document.getElementById('errorArea').textContent = 'Error: ' + e.message;
  }

  document.getElementById('solveBtn').textContent = 'Solve';
}

function showResult(data) {
  document.getElementById('resultArea').style.display = 'block';
  var latex = document.getElementById('resultLatex');
  latex.innerHTML = '\(' + (data.latex || data.result) + '\)';
  if (window.MathJax) MathJax.typesetPromise([latex]);

  var list = document.getElementById('stepsList');
  list.innerHTML = '';
  (data.steps || []).forEach(function(step, i) {
    var div = document.createElement('div');
    div.className = 'step-item';
    div.innerHTML = '<div class="step-num">' + (i+1) + '</div><div class="step-text">' + step + '</div>';
    list.appendChild(div);
  });

  if (data.graph_data) {
    document.getElementById('graphCard').style.display = 'block';
    renderGraph(data.graph_data);
  }
}

var chartInstance = null;
function renderGraph(graphData) {
  var ctx = document.getElementById('mathChart').getContext('2d');
  if (chartInstance) chartInstance.destroy();
  chartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: graphData.labels,
      datasets: graphData.datasets.map(function(ds, i) {
        return {
          label: ds.label,
          data: ds.data,
          borderColor: i === 0 ? '#6c63ff' : '#ef4444',
          backgroundColor: 'transparent',
          borderWidth: 2,
          pointRadius: 0,
          spanGaps: false
        };
      })
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {ticks: {color: '#888', maxTicksLimit: 10}, grid: {color: 'rgba(255,255,255,0.05)'}},
        y: {ticks: {color: '#888'}, grid: {color: 'rgba(255,255,255,0.05)'}}
      },
      plugins: {legend: {labels: {color: '#888'}}}
    }
  });
}

function toggleSteps() {
  var list = document.getElementById('stepsList');
  var btn = document.getElementById('toggleSteps');
  if (list.style.display === 'none') {
    list.style.display = 'block';
    btn.textContent = 'Hide steps';
  } else {
    list.style.display = 'none';
    btn.textContent = 'Show steps';
  }
}
