import math
import sys
sys.path.append("chapter3")
sys.path.append("chapter4")

from drawable import Drawable
from robot import Robot

class Particle(Drawable):
    def __init__(self, init_pose):
        self._pose = init_pose

    def draw(self, ax):
        xs = self._pose[0]
        ys = self._pose[1]
        vxs = math.cos(self._pose[2])
        vys = math.sin(self._pose[2])
        return ax.quiver(xs, ys, vxs, vys, color="blue", alpha=0.5)

    def motion_update(self, vel, omega, delta_t, motion_noise_rate_pdf):
        noise = motion_noise_rate_pdf.rvs()
        vel_scalar = math.sqrt(abs(vel)/delta_t)
        omega_scalar = math.sqrt(abs(omega)/delta_t)
        noised_vel = vel + noise[0] * vel_scalar + noise[1] * omega_scalar
        noised_omega = omega + noise[2] * vel_scalar + noise[3] * omega_scalar
        self._pose = Robot.transition_function(noised_vel, noised_omega, delta_t, self._pose)

