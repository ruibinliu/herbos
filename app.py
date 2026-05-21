from flask import Flask, render_template
from flask_socketio import SocketIO
from queue import Queue

from herbos.core.events import init_events, emit_log
from herbos.robot.worker import RuntimeWorker
from runtime.teleop import TeleopRuntime

from config import HOST, PORT

app = Flask(__name__)

socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")
init_events(socketio)
teleop = TeleopRuntime()

task_queue = Queue()
worker = RuntimeWorker(task_queue)
worker.start()


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("run_skill")
def run_skill(data):
    skill = data["skill"]

    task_queue.put({"type": "skill", "name": skill})

    socketio.emit("status", {
        "message": f"{skill} queued"
    })


@socketio.on("start_teleop")
def start():
    print("start teleop")
    teleop.start()
    emit_log("teleoperation started")


@socketio.on("stop_teleop")
def stop():
    print("stop teleop")
    teleop.stop()
    socketio.emit("status", {
        "message": f"teleoperation stopped"
    })


if __name__ == "__main__":
    socketio.run(app, host=HOST, port=PORT, allow_unsafe_werkzeug=True)
