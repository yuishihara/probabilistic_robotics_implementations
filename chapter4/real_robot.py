import sys
sys.path.append('chapter3')
import math

from scipy.stats import expon, norm, uniform
from robot import Robot


class RealRobot(Robot):
    def __init__(self, initial_pose, camera=None, color='black',
                 noise_per_meter=5, noise_std=math.pi / 60,
                 bias_rate_stds=(0.1, 0.1),
                 expected_stuck_time=1e100, expected_escape_time=1e-100,
                 expected_kidnap_time=1e100,
                 kidnap_x_range=(-5.0, 5.0),
                 kidnap_y_range=(-5.0, 5.0)):
        super(RealRobot, self).__init__(initial_pose, camera, 0.2, color)
        self._noise_pdf = expon(scale=1.0 / (1e-100 + noise_per_meter))
        self._distance_until_noise = self._noise_pdf.rvs()
        self._theta_noise = norm(scale=noise_std)
        self._vel_bias_rate = norm.rvs(loc=1.0, scale=bias_rate_stds[0])
        self._omega_bias_rate = norm.rvs(loc=1.0, scale=bias_rate_stds[1])

        self._stuck_pdf = expon(scale=expected_stuck_time)
        self._time_until_stuck = self._stuck_pdf.rvs()
        self._escape_pdf = expon(scale=expected_escape_time)
        self._time_until_escape = self._escape_pdf.rvs()
        self._is_stuck = False

        self._kidnap_pdf = expon(scale=expected_kidnap_time)
        self._time_until_kidnap = self._kidnap_pdf.rvs()
        range_x = kidnap_x_range
        range_y = kidnap_y_range
        self._kidnap_distribution = uniform(loc=(range_x[0], range_y[0], 0.0),
                                            scale=(range_x[1] - range_x[0], range_y[1] - range_y[0], 2 * math.pi))

    def one_step(self, ut, delta_t):
        self._pose = self._compute_pose(ut, delta_t)
        self._trajectory.append(self._pose)
        return self._camera.observe(self._pose) if self._camera else None

    def _compute_pose(self, ut, delta_t):
        vel, omega = self._add_bias(ut)
        vel, omega = self._check_stuck(vel, omega, delta_t)
        next_pose = self.transition_function(vel, omega, delta_t, self._pose)
        next_pose = self._add_noise(next_pose, vel, omega, delta_t)
        next_pose = self._kidnap(next_pose, delta_t)
        return next_pose

    def _add_bias(self, ut):
        vel, omega = ut
        return vel * self._vel_bias_rate, omega * self._omega_bias_rate

    def _add_noise(self, pose, vel, omega, delta_t):
        self._distance_until_noise -= abs(vel) * \
            delta_t + self._radius * abs(omega) * delta_t
        if self._distance_until_noise <= 0.0:
            self._distance_until_noise += self._noise_pdf.rvs()
            pose[2] += self._theta_noise.rvs()
        return pose

    def _check_stuck(self, vel, omega, delta_t):
        if self._is_stuck:
            self._time_until_escape -= delta_t
            if self._time_until_escape <= 0.0:
                self._time_until_escape += self._escape_pdf.rvs()
                self._is_stuck = False
        else:
            self._time_until_stuck -= delta_t
            if self._time_until_stuck <= 0.0:
                self._time_until_stuck += self._stuck_pdf.rvs()
                self._is_stuck = True
        return vel * (not self._is_stuck), omega * (not self._is_stuck)

    def _kidnap(self, pose, delta_t):
        self._time_until_kidnap -= delta_t
        if self._time_until_kidnap <= 0.0:
            self._time_until_kidnap += self._kidnap_pdf.rvs()
            return np.array(self._kidnap_distribution.rvs()).T
        else:
            return pose


if __name__ == "__main__":
    from world import World
    from fixed_input_agent import FixedInputAgent
    from ideal_robot import IdealRobot
    import numpy as np
    world = World(time_span=30, time_interval=0.1)

    unbiased_robot = IdealRobot(np.array([0.0, 0.0, 0.0]).T, color='gray')
    unbiased_agent = FixedInputAgent(
        unbiased_robot, vel=0.2, omega=10.0 / 180 * math.pi)
    world.append_agent(unbiased_agent)

    biased_robot = RealRobot(np.array([0.0, 0.0, 0.0]).T,
                             noise_per_meter=0.0, bias_rate_stds=(0.2, 0.2),
                             expected_stuck_time=1e1000000,
                             expected_escape_time=0.0,
                             color='red')
    biased_agent = FixedInputAgent(
        biased_robot, vel=0.2, omega=10.0 / 180 * math.pi)
    world.append_agent(biased_agent)

    stucked_robot = RealRobot(np.array([0.0, 0.0, 0.0]).T,
                              noise_per_meter=0.0, bias_rate_stds=(0.0, 0.0),
                              expected_stuck_time=10,
                              expected_escape_time=10,
                              color='blue')
    stucked_agent = FixedInputAgent(
        stucked_robot, vel=0.2, omega=10.0 / 180 * math.pi)
    world.append_agent(stucked_agent)

    kidnap_robot = RealRobot(np.array([0.0, 0.0, 0.0]).T,
                             noise_per_meter=0.0, bias_rate_stds=(0.0, 0.0),
                             expected_stuck_time=1e100,
                             expected_escape_time=1e-100,
                             expected_kidnap_time=5,
                             color='black')
    kidnap_agent = FixedInputAgent(
        kidnap_robot, vel=0.2, omega=10.0 / 180 * math.pi)
    world.append_agent(kidnap_agent)

    world.draw()
