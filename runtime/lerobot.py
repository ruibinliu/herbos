import subprocess
import threading

from config import ROBOT_FOLLOWER_PORT, ROBOT_LEADER_PORT
from herbos.core.events import emit_log
from herbos.core.events import emit_status


class LeRobotRuntime:

    def __init__(self, job_name, command):
        self.job_name = job_name
        self.command = command
        self.process = None
        self.running = False

    def start(self):
        if self.process:
            emit_log(f"{self.job_name} already running")
            return

        emit_log(f"Starting {self.job_name}...")
        self.running = True
        self.process = subprocess.Popen(self.command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8"
        )

        threading.Thread(
            target=self._stream_output,
            daemon=True
        ).start()
        emit_status(robot_state=f"{self.job_name}")

    def _stream_output(self):
        while self.running:
            line = self.process.stdout.readline()
            if not line:
                break
            emit_log(line.strip())
        emit_log(f"{self.job_name} output thread exited")

    def stop(self):
        if not self.process:
            return

        emit_log(f"Stopping {self.job_name}...")

        self.running = False
        self.process.terminate()

        try:
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            emit_log(f"Force killing {self.job_name}")
            self.process.kill()

        self.process = None

        emit_status(robot_state="Idle")
        emit_log(f"{self.job_name} stopped")


current_runtime = None

def start_teleop():
    global current_runtime
    if current_runtime:
        emit_log(f"{current_runtime.job_name} already running")
        return

    current_runtime = LeRobotRuntime(
        job_name="teleop",
        command=["lerobot-teleoperate",
                 "--robot.type=so101_follower",
                 f"--robot.port={ROBOT_FOLLOWER_PORT}",
                 "--robot.id=my_awesome_follower_arm",
                 "--teleop.type=so101_leader",
                 f"--teleop.port={ROBOT_LEADER_PORT}",
                 "--teleop.id=my_awesome_leader_arm",
                 ])
    current_runtime.start()

def stop_runtime():
    global current_runtime
    if current_runtime:
        current_runtime.stop()
        current_runtime = None
