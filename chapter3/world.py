import matplotlib.animation as anim
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("nbagg")


class World(object):
    def __init__(self):
        self._objects = []
        self._animation = None

    def append(self, obj):
        self._objects.append(obj)

    def draw(self):
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(1, 1, 1)
        ax.set_aspect('equal')
        ax.set_xlim(-5, 5)
        ax.set_ylim(-5, 5)
        ax.set_xlabel("X", fontsize=20)
        ax.set_ylabel("Y", fontsize=20)

        scene_objects = []
        self._animation = anim.FuncAnimation(fig, self._step,
                                             fargs=(scene_objects, ax), frames=10, interval=1000, repeat=False)
        plt.show()

    def _step(self, step_number, scene_objects, ax):
        self._remove_previous_scene_objects(scene_objects)
        scene_objects.extend(self._draw_step_number(step_number, ax))
        scene_objects.extend(self._draw_objects(ax))

    def _remove_previous_scene_objects(self, objects):
        print('total scene objects num: ', len(objects))
        for obj in objects:
            obj.remove()
        objects.clear()

    def _draw_step_number(self, step_number, ax):
        drawn_object = ax.text(-4.4, 4.5, "t="+str(step_number), fontsize=10)
        return [drawn_object]

    def _draw_objects(self, ax):
        drawn_objects = []
        for obj in self._objects:
            drawn_objects.extend(obj.draw(ax))
        return drawn_objects


if __name__ == "__main__":
    world = World()
    world.draw()
