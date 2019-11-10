import numpy as np
import math
from world import World
from ideal_robot import IdealRobot
from fixed_input_agent import FixedInputAgent


def main():
    world = World()
    robot1 = IdealRobot(np.array([2, 3, math.pi/6]).T)
    agent1 = FixedInputAgent(robot1, vel=0.2, omega=0.0)

    robot2 = IdealRobot(np.array([-2, -1, math.pi*5/6]).T, "red")
    agent2 = FixedInputAgent(robot2, vel=0.2, omega=10.0/180*math.pi)

    world.append(agent1)
    world.append(agent2)

    world.draw()


if __name__ == "__main__":
    main()
