from drawable import Drawable


class Agent(Drawable):
    def __init__(self, robot):
        self._robot = robot

    def act(self, delta_t):
        raise NotImplementedError("Agent must implement act()")

    def draw(self, ax):
        return self._robot.draw(ax)
