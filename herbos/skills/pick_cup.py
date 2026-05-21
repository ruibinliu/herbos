from time import sleep

from herbos.core.log import logger
from herbos.robot.controller import SO101Controller

robot = SO101Controller()


def run_pick_cup():
    logger.info("Running pick cup")
    robot.move_home()
    sleep(1)
    robot.open_gripper()
    sleep(1)
    robot.close_gripper()
    sleep(1)
