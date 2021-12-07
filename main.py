from robot import Robot
import asyncio


if __name__ ==  '__main__':
    loop = asyncio.get_event_loop()
    robot1 = Robot(1, 'ROB-735472934', 1, 13, 100)
    loop.run_until_complete(robot1.main())