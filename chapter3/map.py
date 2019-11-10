from drawable import Drawable


class Map(Drawable):
    def __init__(self):
        self._landmarks = []

    def append_landmark(self, landmark):
        landmark.set_id(len(self._landmarks) + 1)
        self._landmarks.append(landmark)

    def draw(self, ax):
        drawn_objects = []
        for landmark in self._landmarks:
            drawn_objects.extend(landmark.draw(ax))
        return drawn_objects
