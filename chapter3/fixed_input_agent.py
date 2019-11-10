from agent import Agent


class FixedInputAgent(Agent):
    def __init__(self, robot, vel=0.2, omega=0.0):
        super(FixedInputAgent, self).__init__(robot)
        self._vel = vel
        self._omega = omega

    def act(self, delta_t):
        ut = (self._vel, self._omega)
        self._robot.one_step(ut, delta_t)
