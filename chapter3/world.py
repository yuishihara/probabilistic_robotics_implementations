import matplotlib.animation as anim
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("nbagg")


class World(object):
    def __init__(self, time_span=10, time_interval=0.1):
        self._agents = []
        self._objects = []
        self._animation = None
        self._time_span = time_span
        self._time_interval = time_interval

    def append_agent(self, agent):
        self._agents.append(agent)

    def append_object(self, obj):
        self._objects.append(obj)

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
                                             frames=int(
                                                 self._time_span / self._time_interval) + 1,
                                             interval=int(
                                                 self._time_interval * 100),
                                             repeat=False)
        plt.show()

    def _step(self, step_number, scene_objects, ax):
        self._act_agents()
        self._remove_previous_scene_objects(scene_objects)
        scene_objects.extend(self._draw_step_number(step_number, ax))
        scene_objects.extend(self._draw_time(step_number, ax))
        scene_objects.extend(self._draw_agents(ax))
        scene_objects.extend(self._draw_objects(ax))

    def _act_agents(self):
        for agent in self._agents:
            agent.act(self._time_interval)

    def _remove_previous_scene_objects(self, objects):
        print('total scene objects num: ', len(objects))
        for obj in objects:
            obj.remove()
        objects.clear()

    def _draw_step_number(self, step_number, ax):
        step_str = "step=" + str(step_number)
        drawn_object = ax.text(-4.4, 4.5, step_str, fontsize=10)
        return [drawn_object]

    def _draw_time(self, step_number, ax):
        time_str = "time={:.2f}[s]".format(self._time_interval * step_number)
        drawn_object = ax.text(-4.4, 4.2, time_str, fontsize=10)
        return [drawn_object]

    def _draw_agents(self, ax):
        drawn_objects = []
        for agent in self._agents:
            drawn_objects.extend(agent.draw(ax))
        return drawn_objects

    def _draw_objects(self, ax):
        drawn_objects = []
        for obj in self._objects:
            drawn_objects.extend(obj.draw(ax))
        return drawn_objects


if __name__ == "__main__":
    world = World()
    world.draw()
