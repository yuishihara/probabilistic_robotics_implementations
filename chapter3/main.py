import numpy as np
import math
from world import World
from ideal_robot import IdealRobot


def main():
    world = World()
    robot1 = IdealRobot(np.array([2, 3, math.pi/6]).T)
    robot2 = IdealRobot(np.array([-2, -1, math.pi*5/6]).T, "red")
    world.append(robot1)
    world.append(robot2)

    world.draw()


if __name__ == "__main__":
    main()
