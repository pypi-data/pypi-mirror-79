#!/usr/bin/env python

###############################################################################
# Copyright 2020 ScPA StarLine Ltd. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###############################################################################

import threading
import time

from oscar_protocol import OscarProtocol
from loops import Spinner
from slp import print_raw
from oscar_control import *
from oscar_vehicle_interfaces import create_interface_by_name


OSCAR_DEFAULT_CONTROL_RATE = 0.5
OSCAR_DEFAULT_ODOMETRY_CALC_RATE = 1

class OscarVehicle():

    def __init__(self, interface          = None,
                       protocol_config    = None,
                       controller         = None,
                       controller_params  = None,
                       control_loop_rate  = OSCAR_DEFAULT_CONTROL_RATE,
                       odometry_loop_rate = OSCAR_DEFAULT_ODOMETRY_CALC_RATE):

        self._control_spinner = Spinner(rate=control_loop_rate)
        self._controller = create_controller_by_name(controller, controller_params)

        if self._controller:
            self._control_spinner.set_target(self._calc_control)

        self._vehicle_protocol  = OscarProtocol(protocol_config)
        self._vehicle_interface = create_interface_by_name(interface, self._vehicle_protocol)

        if self._vehicle_interface:
            self._vehicle_interface.start_communication()

        self._odometry = Odometry(self._vehicle_protocol)
        self._odometry_spinner = Spinner(target = self._odometry.calc_odometry,
                                           rate = odometry_loop_rate)

        self._start_odometry_calculation()


    def set_interface(self, interface):

        if self._vehicle_interface:
            self._stop_interface_communication()

        self._vehicle_interface = interface.create(interface)
        self._start_interface_communication()


    def _start_controller(self):
        if self._controller:
            self._controller.reset()
        self._control_spinner.start()


    def _stop_controller(self):
        self._control_spinner.stop()


    def set_controller(self, controller, params = None):

        active_controller = self._control_spinner.is_active()

        if active_controller:
            self._stop_controller()

        self._controller = create_controller_by_name(controller, params)

        if self._controller:
            self._control_spinner.set_target(self._calc_control)
            if active_controller:
                self._start_controller()


    def set_controller_params(self, params):
        if self._controller:
            self._controller.update_params(params)


    def set_controller_rate(self, rate):
        self._control_spinner.set_rate(rate)


    def get_actual_controller_rate(self):
        return self._control_spinner.get_real_rate()


    def _calc_control(self):
        sw_angle, sw_velocity = self._vehicle_protocol.get_steering_wheel_angle_and_velocity()

        self._vehicle_protocol.set_vehicle_acceleration(throttle)
        self._vehicle_protocol.set_steering_wheel_torque(sw_torque)


    def set_speed(self, speed = None, acceleration = None, jerk = None):
        if self._controller.is_not_active():
            self._start_controller()
        if self._controller:
            self._controller.set_target_speed(speed = speed,
                                              acceleration = acceleration,
                                              jerk = jerk)


    def set_steering(self, steering_angle = None, steering_angle_velocity = None):
        if self._controller.is_not_active():
            self._start_controller()
        if self._controller:
            self._controller.set_target_steering(steering_angle = steering_angle,
                                                 steering_angle_velocity = steering_angle_velocity)


    def set_vehicle_throttle(self, throttle):
        self._stop_controller()
        self._vehicle_protocol.set_vehicle_acceleration(throttle)


    def set_steering_wheel_torque(self, steering_wheel_torque):
        self._stop_controller()
        self._vehicle_protocol.set_steering_wheel_torque(steering_wheel_torque)


    def _start_odometry_calculation(self):
        if self._odometry_spinner.is_active():
            self._odometry_spinner.stop()
            self._odometry.reset()
        self._odometry_spinner.start()


    def _stop_odometry_calculation(self):
        self._odometry_spinner.stop()


    def get_odometry(self):
        return self._odometry.get()


    def reset_odometry(self):
        self._odometry.reset()


    def set_odometry_calc_rate(self, rate):
        self._odometry_spinner.set_rate(rate)


    def get_actual_odometry_rate(self):
        return self._odometry_spinner.get_real_rate()


    def auto_mode(self):

        # check cur vehicle state
        # if needs send cmd to change mode and wait for interception
        self._vehicle_protocol.auto_mode()
        self._vehicle_protocol.vehicle_acceleration_cmd.start_sending()
        self._vehicle_protocol.steering_wheel_torque_cmd.start_sending()
        return True


    def manual_mode(self):

        # check cur vehicle state
        # if needs send cmd to change mode and wait for interception
        self._vehicle_protocol.manual_mode()
        self._vehicle_protocol.vehicle_acceleration_cmd.stop_sending()
        self._vehicle_protocol.steering_wheel_torque_cmd.stop_sending()
        return True


    def get_mode(self):
        mode, source = self._vehicle_protocol.get_mode()
        return mode


    def emergency_stop(self):
        return self._vehicle_protocol.emergency_stop_on()


    def recover(self):
        return (self._vehicle_protocol.hand_brake_off() and
                self._vehicle_protocol.emergency_stop_off())


    def hand_brake(self):
        return self._vehicle_protocol.hand_brake_on()


    def led_blink(self):
        self._vehicle_protocol.led_reverse()
        for i in range(3):
            time.sleep(0.5)
            self._vehicle_protocol.led_reverse()
        return True


    def led_on(self):
        return self._vehicle_protocol.led_on()


    def led_off(self):
        return self._vehicle_protocol.led_off()


    def get_led(self):
        return self._vehicle_protocol.get_led()


    def get_emergency_stop(self):
        return self._vehicle_protocol.get_emergency_stop()


    def get_hand_brake(self):
        return self._vehicle_protocol.get_hand_brake()


    def print_all_raw(self):

        vehicle_speed_raw, rec_time_1 = self._vehicle_protocol.get_vehicle_speed_raw()
        vehicle_wheels_speed, rec_time_2 = self._vehicle_protocol.get_vehicle_wheels_speed_raw()
        vehicle_wheels_acc_and_yaw_rate, rec_time_3 = self._vehicle_protocol.get_vehicle_acceleration_and_yaw_rate_raw()
        steering_wheel_pose_and_velocity, rec_time_4 = self._vehicle_protocol.get_steering_wheel_pose_and_velocity_raw()
        steering_wheel_and_eps_torque, rec_time_5 = self._vehicle_protocol.get_steering_wheel_and_eps_torques_raw()

        # print("\nVehicle speed " + str(rec_time_1))
        # print " ".join(hex(byte) for byte in vehicle_speed_raw)
        #
        # vehicle_speed = (vehicle_speed_raw[5] << 8) + vehicle_speed_raw[6]
        # print("vehicle_speed km/h, m/s: " + format(vehicle_speed / 100., '.2f') + " | " + str(vehicle_speed / 3.6 / 100.))

        # print("encoder: " + str(vehicle_speed_raw[4])) # 6-8 wheels turns for 256 ticks
        #                                                # works from some speed
        #

        # TODO CHECK ADD 552
        # print("\nWheels speed " + str(rec_time_2))
        # print " ".join(hex(byte) for byte in vehicle_wheels_speed)

        # print("\nSteering wheel pos vel " + str(rec_time_3))
        # # print " ".join(format(byte, '#010b') for byte in steering_wheel_pose_and_velocity)
        #
        # wtf_2 = steering_wheel_pose_and_velocity[7]
        #
        # print("wtf: " + format(wtf_2 >> 4, '#010b') + " " + format(wtf_2 & 0x0F, '#010b'))
        #
        # steer_fraction = steering_wheel_pose_and_velocity[4] >> 4
        # bits = 4
        # if steer_fraction & (1 << (bits-1)):
        #     steer_fraction -= 1 << bits
        # steer_fraction *= 0.1
        # print("steer_fraction: " + str(steer_fraction))
        #
        # vel = (steering_wheel_pose_and_velocity[4] << 8) + steering_wheel_pose_and_velocity[5]
        # bits = 12
        # vel = vel & 0x0FFF
        # if vel & (1 << (bits-1)):
        #     vel -= 1 << bits
        # # pose *= 1.5
        # print("vel: " + str(vel))
        #
        # pose = (steering_wheel_pose_and_velocity[0] << 8) + steering_wheel_pose_and_velocity[1]
        # bits = 12
        # if pose & (1 << (bits-1)):
        #     pose -= 1 << bits
        # pose *= 1.5
        # print("pose: " + str(pose))

        print("\nSteering wheel torques " + str(rec_time_4))
        print " ".join(hex(byte) for byte in steering_wheel_and_eps_torque)

        swt = (steering_wheel_and_eps_torque[1] << 8) + steering_wheel_and_eps_torque[2]
        bits = 16
        if swt & (1 << (bits-1)):
            swt -= 1 << bits
        # pose *= 1.5
        print("swt: " + str(swt)) # [-32768 | 32767]

        epst = (steering_wheel_and_eps_torque[5] << 8) + steering_wheel_and_eps_torque[6]
        bits = 16
        if epst & (1 << (bits-1)):
            epst -= 1 << bits
        epst *= 0.73
        print("epst: " + str(epst)) # [-20000 | 20000]


    def get_vehicle_speed(self):
        return 0.0


    def get_vehicle_wheels_speed(self):
        return 0.0, 0.0, 0.0, 0.0


    def get_steering_wheel_angle_and_velocity(self):
        return self._vehicle_protocol.get_steering_wheel_angle_and_velocity()


    def get_steering_wheel_and_eps_torques(self):
        return 0.0, 0.0


    def vehicle_acceleration_interception_on(self):
        return self._vehicle_protocol.vehicle_acceleration_interception_on()


    def vehicle_acceleration_interception_off(self):
        return self._vehicle_protocol.vehicle_acceleration_interception_off()


    def start_sending_vehicle_acceleration(self):
        return self._vehicle_protocol.start_sending_vehicle_acceleration()


    def stop_sending_vehicle_acceleration(self):
        return self._vehicle_protocol.stop_sending_vehicle_acceleration()


    def steering_wheel_interception_on(self):
        return self._vehicle_protocol.steering_wheel_interception_on()


    def steering_wheel_interception_off(self):
        return self._vehicle_protocol.steering_wheel_interception_off()


    def start_sending_steering_wheel_torque(self):
        return self._vehicle_protocol.start_sending_steering_wheel_torque()


    def stop_sending_steering_wheel_torque(self):
        return self._vehicle_protocol.stop_sending_steering_wheel_torque()


    def error_report(self):
        return 'NO_ERROR'


class Odometry():

    def __init__(self, protocol):
        self._protocol = protocol

        self.wheel_radius   = self._protocol.vehicle_params["wheel_radius"]
        self.wheel_width    = self._protocol.vehicle_params["wheel_width"]
        self.wheelbase      = self._protocol.vehicle_params["wheelbase"]
        self.axle_track     = self._protocol.vehicle_params["axle_track"]
        self.steering_ratio = self._protocol.vehicle_params["steering_ratio"]

        self._pose_data_lock = threading.Lock()
        self.x    = 0.0
        self.y    = 0.0
        self.yaw  = 0.0
        self.dx   = 0.0
        self.dy   = 0.0
        self.dyaw = 0.0
        self.time = 0.0


    def get(self):
        return self.x, self.y, self.yaw, self.dx, self.dy, self.dyaw, self.time


    def reset(self):
        with self._pose_data_lock:
            self.x    = 0.0
            self.y    = 0.0
            self.yaw  = 0.0
            self.time = 0.0


    def calc_odometry(self):
        pass

        # u_1 = acc
        # u_2 = sw_angle
        #
        # dx = cos(self.yaw) * self.v
        # dy = sin(self.yaw) * self.v
        # dv = u_1
        # dyaw = self.v / self.wheelbase * np.tan(u_2)
        #
        # self.x += dt * dx
        # self.y += dt * dy
        # self.yaw += dt * dyaw
        # self.v += dt * dv
        # self.a = dv
