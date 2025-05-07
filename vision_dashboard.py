from flask import Flask, render_template_string
from core_memory_hub import CoreMemoryHub
from autopilot_priority_executor import AutopilotPriorityExecutor
import threading
import time

app = Flask(__name__)

memory = CoreMemoryHub()
autopilot = AutopilotPriorityExecutor()
vision_log = []

# Schedule autopilot + memory sync

def scheduler():
    while True:
        result = autopilot.run_autopilot_cycle()
        vision_log.append(f"🌀 Autopilot @ {result['plan_time']}\n" + "\n".join(result['executed']))
        time.sleep(3600)  # every hour

threading.Thread(target=scheduler, daemon=True).start()

template = """
<!doctype html>
<html>
<head>
  <title>Builder Core Dashboard</title>
  <style>
    body { font-family: Arial, sans-serif; background: #111; color: #eee; padding: 2em; }
    h1, h2 { color: #00ffe0; }
    .log-box { background: #222; padding: 1em; border-radius: 6px; margin-bottom: 2em; }
  </style>
</head>
<body>
  <h1>🧠 Builder Core Vision Dashboard</h1>
  <div class="log-box">
    <h2>System Cycles & Metrics</h2>
    <p><strong>Total Cycles:</strong> {{ metrics.total_cycles }}</p>
    <p><strong>Diagnostics:</strong> {{ metrics.diagnostics }}</p>
    <p><strong>Plans Created:</strong> {{ metrics.plans_made }}</p>
    <p><strong>Last Action:</strong> {{ metrics.last_action }}</p>
  </div>
  <div class="log-box">
    <h2>🧠 Recent Memory Highlights</h2>
    {% for entry in memory_entries %}<p>• {{ entry }}</p>{% endfor %}
  </div>
  <div class="log-box">
    <h2>🌀 Vision Events (Autopilot Sync)</h2>
    {% for log in vision_log[-5:] %}<p>{{ log }}</p>{% endfor %}
  </div>
</body>
</html>
"""

@app.route("/")
def dashboard():
    metrics = autopilot.get_execution_history()
    summary = {
        "total_cycles": len(metrics),
        "diagnostics": len(memory.recall(["diagnostic"])),
        "plans_made": len(memory.recall(["planning"])),
        "last_action": metrics[-1] if metrics else "—"
    }
    return render_template_string(template, metrics=summary, memory_entries=memory.summarize_recent(), vision_log=vision_log)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)