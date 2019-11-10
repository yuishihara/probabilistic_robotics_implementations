import matplotlib.animation as anim
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("nbagg")


class World(object):
    def __init__(self):
        self._agents = []
        self._animation = None

    def append(self, agent):
        self._agents.append(agent)

    def draw(self):
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(1, 1, 1)
        ax.set_aspect('equal')
        ax.set_xlim(-5, 5)
        ax.set_ylim(-5, 5)
        ax.set_xlabel('X', fontsize=20)
        ax.set_ylabel('Y', fontsize=20)

        scene_objects = []
        self._animation = anim.FuncAnimation(fig, self._step,
                                             fargs=(scene_objects, ax),
                                             frames=1000,
                                             interval=100,
                                             repeat=False)
        plt.show()

    def _step(self, step_number, scene_objects, ax):
        self._act_agents()
        self._remove_previous_scene_objects(scene_objects)
        scene_objects.extend(self._draw_step_number(step_number, ax))
        scene_objects.extend(self._draw_agents(ax))

    def _act_agents(self):
        for agent in self._agents:
            agent.act(0.1)

    def _remove_previous_scene_objects(self, objects):
        print('total scene objects num: ', len(objects))
        for obj in objects:
            obj.remove()
        objects.clear()

    def _draw_step_number(self, step_number, ax):
        drawn_object = ax.text(-4.4, 4.5, "t="+str(step_number), fontsize=10)
        return [drawn_object]

    def _draw_agents(self, ax):
        drawn_objects = []
        for agent in self._agents:
            drawn_objects.extend(agent.draw(ax))
        return drawn_objects


if __name__ == "__main__":
    world = World()
    world.draw()
