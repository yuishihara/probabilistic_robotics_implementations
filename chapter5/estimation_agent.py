import sys
sys.path.append("chapter3")
sys.path.append("chapter4")

from agent import Agent

class EstimationAgent(Agent):
    def __init__(self, robot, vel, omega, localizer):
        super(EstimationAgent, self).__init__(robot)
        self._vel = vel
        self._omega = omega
        self._localizer = localizer

    def act(self, delta_t):
        ut = (self._vel, self._omega)
        self._robot.one_step(ut, delta_t)

    def draw(self, ax):
        drawn_objects = []
        drawn_objects.extend(super().draw(ax))
        drawn_objects.append(ax.text(0, 0, "hoge", fontsize=10))
        drawn_objects.extend(self._localizer.draw(ax))
        return drawn_objects


if __name__ == "__main__":
    import numpy as np
    import math

    from landmark import Landmark
    from map import Map
    from ideal_camera import IdealCamera
    from real_robot import RealRobot
    from world import World
    from monte_carlo_localization import MonteCarloLocalization

    landmark1 = Landmark(2, -2)
    landmark2 = Landmark(-1, -3)
    landmark3 = Landmark(3, 3)
    world_map = Map()
    world_map.append_landmark(landmark1)
    world_map.append_landmark(landmark2)
    world_map.append_landmark(landmark3)

    world = World(time_span=30, time_interval=0.1)
    init_pose = np.array([-2, -1, math.pi * 5 / 6]).T
    robot = RealRobot(init_pose, camera=IdealCamera(world_map))
    mcl = MonteCarloLocalization(init_pose, 100)
    agent = EstimationAgent(robot, vel=0.2, omega=10.0 /
                            180 * math.pi, localizer=mcl)
    world.append_agent(agent)

    world.append_object(world_map)
    world.draw()
