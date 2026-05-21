import subprocess
import threading

from config import ROBOT_FOLLOWER_PORT, ROBOT_LEADER_PORT
from herbos.core.events import emit_log
from herbos.core.events import emit_status


class TeleopRuntime:

    def __init__(self):
        self.process = None

    def start(self):
        if self.process:
            emit_log("Teleop already running")
            return

        emit_log("Starting teleop...")

        self.process = subprocess.Popen(["lerobot-teleoperate",
            "--robot.type=so101_follower",
            f"--robot.port={ROBOT_FOLLOWER_PORT}",
            "--robot.id=my_awesome_follower_arm",
            "--teleop.type=so101_leader",
            f"--teleop.port={ROBOT_LEADER_PORT}",
            "--teleop.id=my_awesome_leader_arm",
        ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8"
        )

        threading.Thread(
            target=self._stream_output,
            daemon=True
        ).start()

        emit_status(
            robot_state="Teleop"
        )

    def _stream_output(self):

        for line in self.process.stdout:
            emit_log(line.strip())

        retcode = self.process.poll()

        if retcode == 0:

            emit_log("Teleop exited")

            emit_status(
                robot_state="Idle"
            )

        else:
            emit_log(f"Teleop failed with code {retcode}")
            emit_status(robot_state="Error")

        self.process = None

    def stop(self):
        if not self.process:
            return

        emit_log("Stopping teleop...")
        self.process.terminate()

        try:
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            emit_log("Force killing teleop")
            self.process.kill()

        self.process = None
        emit_status(robot_state="Idle")

        emit_log("Teleop stopped")
