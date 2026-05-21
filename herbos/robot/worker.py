import threading

from herbos.core.events import emit_log
from herbos.core.events import emit_status
from herbos.skills.pick_cup import run_pick_cup
from herbos.skills.pick_capsule import run_pick_capsule


class RuntimeWorker:

    def __init__(self, task_queue):
        self.task_queue = task_queue

    def start(self):
        thread = threading.Thread(target=self.loop, daemon=True)
        thread.start()

    def loop(self):
        emit_log("Worker started")

        while True:
            skill = self.task_queue.get()
            emit_log(f"Dequeued skill: {skill}")
            emit_status(queue_size=self.task_queue.qsize())

            try:
                self.run_skill(skill)
            except Exception as e:
                emit_log(f"Worker error: {e}")

            self.task_queue.task_done()

    def run_skill(self, skill):
        emit_log(f"Starting skill: {skill}")
        emit_status(
            current_skill=skill,
            robot_state="Running"
        )

        try:
            if skill == "pick_cup":
                run_pick_cup()
            elif skill == "pick_capsule":
                run_pick_capsule()
            emit_log(f"Skill completed: {skill}")
            emit_status(robot_state="Idle")

        except Exception as e:
            emit_log(f"Skill failed: {e}")
            emit_status(robot_state="Error")
