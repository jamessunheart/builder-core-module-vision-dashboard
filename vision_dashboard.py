from flask import Flask, render_template_string
from core_memory_hub import CoreMemoryHub
from autopilot_priority_executor import AutopilotPriorityExecutor

app = Flask(__name__)

memory = CoreMemoryHub()
autopilot = AutopilotPriorityExecutor()

dashboard_template = """
<!doctype html>
<html>
<head>
  <title>Builder Core Vision Dashboard</title>
  <style>
    body { font-family: Arial, sans-serif; background: #101010; color: #f0f0f0; padding: 2em; }
    h1 { color: #00ffd0; }
    .section { margin-bottom: 2em; }
    .log-box { background: #1e1e1e; padding: 1em; border-radius: 6px; }
    .tag { background: #333; color: #0ff; padding: 0.2em 0.6em; margin: 0.2em; display: inline-block; border-radius: 4px; }
  </style>
</head>
<body>
  <h1>🧠 Builder Core Vision Dashboard</h1>

  <div class="section">
    <h2>🔢 System Metrics</h2>
    <div class="log-box">
      <p><strong>Reflection Cycles:</strong> {{ metrics.total_cycles }}</p>
      <p><strong>Diagnostics Run:</strong> {{ metrics.diagnostics }}</p>
      <p><strong>Plans Created:</strong> {{ metrics.plans_made }}</p>
      <p><strong>Last Action:</strong> {{ metrics.last_action }}</p>
    </div>
  </div>

  <div class="section">
    <h2>🧠 Memory Highlights</h2>
    <div class="log-box">
      {% for entry in memory_entries %}
        <p>🗒️ {{ entry }}</p>
      {% endfor %}
    </div>
  </div>

  <div class="section">
    <h2>🎯 Strategy Notes</h2>
    <div class="log-box">
      <p>— Optimize clarity and responsiveness</p>
      <p>— Strengthen self-awareness and memory integration</p>
      <p>— Extend Builder Core to support external collaborations</p>
    </div>
  </div>

</body>
</html>
"""

@app.route("/")
def dashboard():
    metrics = autopilot.get_execution_history()
    log = memory.summarize_recent(7)
    summary = {
        "total_cycles": len(metrics),
        "diagnostics": len(memory.recall(["diagnostic"])),
        "plans_made": len(memory.recall(["planning"])),
        "last_action": metrics[-1] if metrics else "—"
    }
    return render_template_string(dashboard_template, metrics=summary, memory_entries=log)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)