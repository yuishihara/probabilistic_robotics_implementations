from particle import Particle

import sys
sys.path.append("chapter3")
sys.path.append("chapter4")

import numpy as np
from scipy.stats import multivariate_normal

from drawable import Drawable


class MonteCarloLocalization(Drawable):
    def __init__(self, init_pose, particle_num, motion_noise_stds):
        self._particles = [Particle(init_pose) for i in range(particle_num)]

        v = motion_noise_stds
        covariance = np.diag([v["nn"]**2, v["no"]**2, v["on"]**2, v["oo"]**2])
        self._motion_noise_rate_pdf = multivariate_normal(cov=covariance)

    def draw(self, ax):
        drawn_objects = []
        for particle in self._particles:
            drawn_objects.append(particle.draw(ax))

        return drawn_objects

    def motion_update(self, vel, omega, delta_t):
        for particle in self._particles:
            particle.motion_update(vel, omega, delta_t, self._motion_noise_rate_pdf)


if __name__ == "__main__":
    import math
    from estimation_agent import EstimationAgent
    initial_pose = np.array([0, 0, 0]).T
    particle_num = 100
    stds = {"nn": 0.01, "no": 0.02, "on": 0.03, "oo": 0.04}
    localizer = MonteCarloLocalization(
        initial_pose, particle_num, motion_noise_stds=stds)
    localizer.motion_update(0.2, 10.0 / 180 * math.pi, 0.1)
    for p in localizer._particles:
        print(p._pose)