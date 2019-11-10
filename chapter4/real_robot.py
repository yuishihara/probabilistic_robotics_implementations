import sys
sys.path.append('chapter3')
import math

from scipy.stats import expon, norm
from robot import Robot


class RealRobot(Robot):
    def __init__(self, initial_pose, camera=None, color='black',
                 noise_per_meter=5, noise_std=math.pi / 60):
        super(RealRobot, self).__init__(initial_pose, camera, 0.2, color)
        self._noise_pdf = expon(scale=1.0 / (1e-100 + noise_per_meter))
        self._distance_until_noise = self._noise_pdf.rvs()
        self._theta_noise = norm(scale=noise_std)

    def one_step(self, ut, delta_t):
        self._pose = self._compute_pose(ut, delta_t)
        self._trajectory.append(self._pose)
        return self._camera.observe(self._pose) if self._camera else None

    def _add_noise(self, pose, vel, omega, delta_t):
        self._distance_until_noise -= abs(vel) * \
            delta_t + self._radius * abs(omega) * delta_t
        if self._distance_until_noise <= 0.0:
            self._distance_until_noise += self._noise_pdf.rvs()
            pose[2] += self._theta_noise.rvs()
        return pose

    def _compute_pose(self, ut, delta_t):
        vel, omega = ut
        next_pose = self.transition_function(vel, omega, delta_t, self._pose)
        next_pose = self._add_noise(next_pose, vel, omega, delta_t)
        return next_pose
