from particle import Particle

import sys
sys.path.append("chapter3")
sys.path.append("chapter4")

from drawable import Drawable

class MonteCarloLocalization():
    def __init__(self, init_pose, particle_num):
        self._particles = [Particle(init_pose) for i in range(particle_num)]

    def draw(self, ax):
        drawn_objects = []
        for particle in self._particles:
            drawn_objects.append(particle.draw(ax))
        
        return drawn_objects