from robot import Robot
import asyncio


if __name__ ==  '__main__':
    loop = asyncio.get_event_loop()
    robot = Robot()
    loop.run_until_complete(robot.main())