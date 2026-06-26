####################### Disclaimer #######################

# Filename - ACL_FLL_v04_Pro.py
# Pybricks firmware - v3.6.1 (Pybricks Code v2.6.1)
# Tested on - Laura 4 Air

# 1 - This code library is developed for Assassins Robotics students & coaches usage only.
# 2 - This code library was tested on and to be paired with Laura.
# 3 - Any modifications to the robot base & code library are not encouraged and the results will not be optimsed.
# 4 - Should you found any bugs or ideas for improvement, feel free to consult respective Assassins Robotics coaches.

# Think Like Champion, Work Like Champion, Play Like Champion
# © 2025 Assassins Mecha Sdn Bhd.

################### Pybricks library ###################
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Axis, Button, Color, Direction, Port, Side, Stop, Icon
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

################ Robot configuration ################
AXLE_TRACK = 146   # If robot turn too less, increase axle_track and vice versa
WHEEL_SIZE = 62.7   # If robot drives too far, increase wheel_size and vice versa

LOW = 13  # Default value for the darkest line (0-100)
HIGH = 99  # Default value for the brightest surface (0-100)

# =================================================================
# GLOBAL CONSTANTS FOR STUDENT AUTOCOMPLETE
# =================================================================
LEFT_DRIVE = "left_drive"
RIGHT_DRIVE = "right_drive"
LEFT_ADAPTER = "left_adapter"
RIGHT_ADAPTER = "right_adapter"
LEFT_COLOUR = "left_colour"
RIGHT_COLOUR = "right_colour"

class Laura():
    def __init__(self):
        
        self._hub = PrimeHub(top_side=Axis.Z, front_side=Axis.Y)
        self._colour_A = ColorSensor(Port.A)
        self._colour_B = ColorSensor(Port.B)
        self._left_adapter = Motor(port=Port.C, positive_direction=Direction.CLOCKWISE, gears=[20,20]) 
        self._right_adapter = Motor(port=Port.D, positive_direction=Direction.CLOCKWISE, gears=[20,20]) 
        self._left_drive = Motor(port=Port.E, positive_direction=Direction.COUNTERCLOCKWISE)
        self._right_drive = Motor(port=Port.F, positive_direction=Direction.CLOCKWISE)
        # self._left_adapter = Motor(port=Port.E, positive_direction=Direction.CLOCKWISE, gears=[20,20]) 
        # self._right_adapter = Motor(port=Port.F, positive_direction=Direction.CLOCKWISE, gears=[20,20]) 
        # self._left_drive = Motor(port=Port.C, positive_direction=Direction.COUNTERCLOCKWISE)
        # self._right_drive = Motor(port=Port.D, positive_direction=Direction.CLOCKWISE)
        self._drive_base = DriveBase(self._left_drive, self._right_drive, WHEEL_SIZE, AXLE_TRACK)

        # STRING-TO-HARDWARE MAPPINGS
        self._sensor_map = {
            LEFT_COLOUR: self._colour_A,
            RIGHT_COLOUR: self._colour_B
        }

        self._adapter_motor_map = {
            LEFT_ADAPTER: self._left_adapter, 
            RIGHT_ADAPTER: self._right_adapter
        }

        self._drive_motor_map = {
            LEFT_DRIVE: self._left_drive, 
            RIGHT_DRIVE: self._right_drive
        }

        # WRO PID Constants 
        self._pid = {
            "KP_GYRO": 3.0,
            "KD_GYRO": 0.18,
            "KI_GYRO": 0.0002,
            "KP_GYROPT": 4.0,
            "KD_GYROPT": 0.55,
            "KP_GYROLT": 5.0,
            "KD_GYROLT": 0.9,
            "KP_FAST": 0.4,
            "KD_FAST": 2.0,
            "KP_SLOW": 0.2,
            "KD_SLOW": 2.0
        }

        # ## Blue robot
        # self._pid = {
        #     "KP_GYRO": 1.8,
        #     "KD_GYRO": 0.35,
        #     "KI_GYRO": 0.0002,
        #     "KP_GYROPT": 4.0,
        #     "KD_GYROPT": 0.4,
        #     "KP_GYROLT": 5.0,
        #     "KD_GYROLT": 0.9,
        #     "KP_FAST": 0.4,
        #     "KD_FAST": 2.0,
        #     "KP_SLOW": 0.2,
        #     "KD_SLOW": 2.0
        # }

        self._hub.system.set_stop_button([Button.BLUETOOTH, Button.RIGHT])

        # WRO State Variables
        self._gyro_offset = 0
        self._total_angle_error = 0
        
        # Timers
        self._stopWatch = StopWatch()
        self._internalClock = StopWatch()

    # ==========================================
    # UTILITY FUNCTIONS
    # ==========================================

    def _get_gyro_angle(self):
        return self._hub.imu.rotation(Axis.Z) - self._gyro_offset

    def _get_sensor(self, port):
        if port in self._sensor_map:
            return ((self._sensor_map[port].reflection() - LOW) / (HIGH - LOW)) * 100
        else:
            self.hub_speaker_beep(200, 1000)
            raise ValueError(f"Invalid port: {port}")
    
    def _get_encoders(self):
        return (abs(self._left_drive.angle()) + abs(self._right_drive.angle())) / 2

    def _reset_encoders(self):
        self._left_drive.reset_angle(0)
        self._right_drive.reset_angle(0)
    
    def reset_gyro(self, angle=0):
        self._gyro_offset = self._hub.imu.rotation(Axis.Z) - angle
    
    def calibrate_sensor(self, port):
        print("\n--- Starting calibration ---")
        if port in self._sensor_map:
            low = self._sensor_map[port].reflection()
            high = self._sensor_map[port].reflection()

            while not Button.BLUETOOTH in self._hub.buttons.pressed():
                if self._sensor_map[port].reflection() < low:
                    low = self._sensor_map[port].reflection()
                    self.hub_speaker_beep(200, 50)
                elif self._sensor_map[port].reflection() > high:
                    high = self._sensor_map[port].reflection()
                    self.hub_speaker_beep(200, 50)
        else:
            print(f"ERROR: Invalid Port : '{port}'")
            return

        self.hub_speaker_beep(1000, 50)
        self.hub_speaker_beep(1500, 50)
        self.hub_speaker_beep(1000, 50)
        print("\n--- Colour Sensor Calibration Results ---")
        print("Low = ", low, "High = ", high)
        print("ACTION REQUIRED: Manually update these values in code library for persistence.")

    def motor_pairing(self, power=100, duration=5000):
        self._reset_encoders()
        left_speed_readings = []
        right_speed_readings = []

        print(f"\n--- Starting calibration: {power}% Power for {duration}ms ---")
        self._wro_drive(-power, power) 
        self._stopWatch.reset()

        while self._stopWatch.time() < duration:
            left_speed_readings.append(abs(self._left_drive.speed()))
            right_speed_readings.append(abs(self._right_drive.speed()))
            wait(10)
            
        self.robot_stop(0)

        final_left_angle = abs(self._left_drive.angle())
        final_right_angle = abs(self._right_drive.angle())
        avg_left_speed = sum(left_speed_readings) / len(left_speed_readings)
        avg_right_speed = sum(right_speed_readings) / len(right_speed_readings)
        
        self.hub_speaker_beep(1000, 50)
        self.hub_speaker_beep(1500, 50)
        self.hub_speaker_beep(1000, 50)

        print("\n--- Motor Pair Calibration Results ---")
        print(f"Final Left Angle:    {final_left_angle}°")
        print(f"Final Right Angle:   {final_right_angle}°")
        print(f"Average Left Speed:  {avg_left_speed:.1f} °/s")
        print(f"Average Right Speed: {avg_right_speed:.1f} °/s")

    def robot_stop(self, settling_time=200):
        self._left_drive.brake()
        self._right_drive.brake()
        wait(100)
        self._left_drive.hold()
        self._right_drive.hold()
        wait(50)
        if settling_time > 0:
            self._hub.speaker.beep(500, settling_time)

    def wall_square(self, power=-35, duration=300, angle=0):
        self._wro_drive(-power, power)
        wait(duration)
        self._stopWatch.reset() 
        
        while (abs(self._left_drive.speed()) > 10 or abs(self._right_drive.speed()) > 10) and self._stopWatch.time() < 1500:
            wait(10)
        
        wait(200)
        self.reset_gyro(angle)
        self.robot_stop()

    def _wro_drive(self, left_power, right_power):
        """ The Interceptor: Converts WRO negative logic to FLL positive logic. """
        self._left_drive.dc(-left_power)
        self._right_drive.dc(right_power)

    def unregulated_adapter(self, left_power, right_power, left_limit, right_limit):

        # --- Left Motor Logic ---
        if left_power != 0:
            if abs(self._left_adapter.load()) > abs(left_limit):
                self._left_adapter.hold() # Stall detected, lock it!
            else:
                self._left_adapter.dc(left_power) # Safe to keep pushing
        else:
            self._left_adapter.brake() # Don't move if power is 0

        # --- Right Motor Logic ---
        if right_power != 0:
            if abs(self._right_adapter.load()) > abs(right_limit):
                self._right_adapter.hold()
            else:
                self._right_adapter.dc(right_power)
        else:
            self._right_adapter.brake()
            
        wait(5) # Tiny delay to prevent the hub from freezing in a tight loop

    # ==========================================
    # PORT VIEW
    # ==========================================

    def port_view_colour(self, interval=100):
        """
        Measure Color value.
        - [interval:int] Duration between each reading updates (ms)
        """
        print("\n---- Color Value ----")
        while True:
            print("Colour (left): ", self._colour_A.color(), "Colour (right): ", self._colour_B.color())
            wait(interval)

    def port_view_hsv(self, interval=100):
        """
        Measure HSV value.
        - [interval:int] Duration between each reading updates (ms)
        """
        print("\n---- HSV Value ----")
        while True:
            print("HSV (right): ", self._colour_B.hsv())
            wait(interval)

    def port_view_reflected_light(self, interval=100):
        """
        Measure reflected light value.
        - [interval:int] Duration between each reading updates (ms)
        """
        print("\n---- Reflected Value ----")
        while True:
            right_colour_normalised = (((self._colour_B.reflection() - LOW) / (HIGH - LOW))) * 100
            print("Reflected (right): ", self._colour_B.reflection(), "| Normalised (right): ", right_colour_normalised)
            wait(interval)

    def port_view_motor_angle(self, interval=100, reset_angle=True):
        """
        Measure motor degree.
        - [interval:int] Duration between each reading updates (ms)
        """
        wait(200)
        if resetDegree:
            self._left_drive.reset_angle(0)
            self._right_drive.reset_angle(0)
            self._left_adapter.reset_angle(0)
            self._right_adapter.reset_angle(0)

        print("\n---- Motor angle ----")
        while True:
            print("LeftDrive: ", self._left_drive.angle(), "| RightDrive: ", self._right_drive.angle(), "| LeftAdapter: ", self._left_adapter.angle(), "| RightAdapter: ", self._right_adapter.angle())
            wait(interval)

    def port_view_motor_load(self, power, interval=100):
        """
        Measure motor load.
        - [motorPower:int] Set the testing motor power (-100 to 100)
        - [interval:int] Duration between each reading updates (ms)
        """
        print("\n---- Motor load ----")
        while True:
            self._left_drive.dc(power)
            self._right_drive.dc(power)
            self._left_adapter.dc(power)
            self._right_adapter.dc(power)
            print("LeftDrive: ", self._left_drive.load(), "| RightDrive: ", self._right_drive.load(), "| LeftAdapter: ", self._left_adapter.load(), "| RightAdapter: ", self._right_adapter.load())
            wait(interval)

    def port_view_motor_speed(self, speed, interval=100):
        """
        Measure motor speed.
        - [motorSpeed:int] Set the testing motor speed (-1000 to 1000)
        - [interval:int] Duration between each reading updates (ms)
        """
        print("\n---- Motor speed ----")
        while True:
            self._left_drive.run(speed)
            self._right_drive.run(speed)
            self._left_adapter.run(speed)
            self._right_adapter.run(speed)
            print("LeftDrive: ", self._left_drive.speed(), "| RightDrive: ", self._right_drive.speed(), "| LeftAdapter: ", self._left_adapter.speed(), "| RightAttach: ", self._right_adapter.speed())
            wait(interval)   

    def port_view_battery(self):
        """
        Measure battery level on hub.
        """
        print("Battery voltage: ", self._hub.battery.voltage(), "mV", "| Battery current: ", self._hub.battery.current(), "mA")

    # ==========================================
    # HUB DISPLAY
    # ==========================================

    def hub_status_light(self, colour):
        self._hub.light.on(colour)

    def hub_display_num(self, number):
        self._hub.display.number(number)

    def hub_speaker_beep(self, frequency, duration):
        self._hub.speaker.beep(frequency, duration)

    def hub_button_pressed(self):
        return self._hub.buttons.pressed()

    # ==========================================
    # ADAPTER MOTOR
    # ==========================================
    
    def adapter_motor_brake(self, port):
        if port in self._adapter_motor_map:
            self._adapter_motor_map[port].brake()
        else:
            self.hub_speaker_beep(200, 1000)
            raise ValueError(f"Invalid adapter: {port}")

    def adapter_motor_on_power(self, port, power):
        if port in self._adapter_motor_map:
            self._adapter_motor_map[port].dc(power)
        else:
            self.hub_speaker_beep(200, 1000)
            raise ValueError(f"Invalid adapter: {port}")
    
    def adapter_motor_on_speed(self, port, speed):
        if port in self._adapter_motor_map:
            self._adapter_motor_map[port].run(speed)
        else:
            self.hub_speaker_beep(200, 1000)
            raise ValueError(f"Invalid adapter: {port}")

    def adapter_motor_seconds(self, port, speed, duration, stop_method=Stop.BRAKE, wait_complete=True):
        if port in self._adapter_motor_map:
            self._adapter_motor_map[port].run_time(speed, duration, stop_method, wait_complete)
        else:
            self.hub_speaker_beep(200, 1000)
            raise ValueError(f"Invalid adapter: {port}")
        
    def adapter_motor_degree(self, port, speed, degree, reset_degree=True, stop_method=Stop.BRAKE, wait_complete=True):
        if port in self._adapter_motor_map:
            if reset_degree is True:
                self._adapter_motor_map[port].reset_angle(0)
            self._adapter_motor_map[port].run_angle(speed, degree, stop_method, wait_complete)
        else:
            self.hub_speaker_beep(200, 1000)
            raise ValueError(f"Invalid adapter: {port}")

    # ==========================================
    # ENCODER MOVEMENTS
    # ==========================================

    def _encoder_move(self, mode, target, left_power, right_power, stop, kp, kd, compare, port=None):
        """ WRO CORE MATH: Unified Universal Cross-Multiplication Odometry """
        last_error = 0  
        self._internalClock.reset()
        self._reset_encoders()
        
        if mode == 'time':
            self._stopWatch.reset()

        dir_l = 1 if left_power >= 0 else -1
        dir_r = 1 if right_power >= 0 else -1
        
        avg_power = (abs(left_power) + abs(right_power)) / 2
        if avg_power == 0: 
            avg_power = 1

        while True:
            # Exit Conditions
            if mode == 'time' and self._stopWatch.time() >= target: break
            if mode == 'degree' and self._get_encoders() >= target: break
            if mode == 'sensor' and ((self._get_sensor(port) < target) == compare): break
            if mode == 'curve' and max(abs(self._left_drive.angle()), abs(self._right_drive.angle())) >= target: break
            
            # Cross-Multiplication Math
            l_pos = abs(self._left_drive.angle())
            r_pos = abs(self._right_drive.angle())
            
            raw_error = (l_pos * abs(right_power)) - (r_pos * abs(left_power))
            error = raw_error / avg_power
            
            # PD Correction
            correction = (error * kp) + ((error - last_error) * kd)
            last_error = error
            
            # Actuation Mapping
            l_mag = abs(left_power) - correction
            r_mag = abs(right_power) + correction
            
            l_duty = l_mag * dir_l
            r_duty = r_mag * dir_r
            
            # WRO Actuator wrapper natively handles the FLL negative conversions
            self._wro_drive(max(-100, min(100, -l_duty)), max(-100, min(100, r_duty)))
            wait(10)
            
        if stop: self.robot_stop()

    def encoder_time(self, left_power, right_power, duration, stop=True):
        self._encoder_move('time', duration, left_power, right_power, stop, 1.0, 1.2, None)

    def encoder_degree(self, left_power, right_power, degree, stop=True):
        self._encoder_move('degree', degree, left_power, right_power, stop, 1.0, 1.2, None)

    def encoder_sensor(self, left_power, right_power, port, threshold=15, compare=True, stop=True):
        self._encoder_move('sensor', threshold, left_power, right_power, stop, 1.0, 1.2, compare, port)

    def encoder_curve(self, left_power, right_power, degree, stop=True):
        self._encoder_move('curve', degree, left_power, right_power, stop, 1.0, 1.2, None)

    def encoder_acc(self, left_power, right_power, total_degree, steps=3, stop=True, accel_deg=30, decel_deg=60, min_power=30):
        total_ramp = accel_deg + decel_deg
        if total_ramp > total_degree:
            ratio = total_degree / total_ramp
            accel_deg *= ratio
            decel_deg *= ratio
            
        accel_step_deg = accel_deg / steps
        decel_step_deg = decel_deg / steps
        
        dir_l = 1 if left_power >= 0 else -1
        dir_r = 1 if right_power >= 0 else -1
        max_l = abs(left_power)
        max_r = abs(right_power)

        # 1. Accelerate
        for i in range(1, steps + 1):
            fraction = i / steps 
            cur_l = (min_power + (max_l - min_power) * fraction) * dir_l
            cur_r = (min_power + (max_r - min_power) * fraction) * dir_r
            self.encoder_degree(cur_l, cur_r, accel_step_deg, stop=False)

        # 2. Cruise
        cruise_deg = total_degree - accel_deg - decel_deg
        if cruise_deg > 0:
            self.encoder_degree(left_power, right_power, cruise_deg, stop=False)

        # 3. Decelerate
        for i in range(steps - 1, -1, -1):
            fraction = i / steps
            if i == 0:
                cur_l = min_power * dir_l
                cur_r = min_power * dir_r
                step_stop = stop
            else:
                cur_l = (min_power + (max_l - min_power) * fraction) * dir_l
                cur_r = (min_power + (max_r - min_power) * fraction) * dir_r
                step_stop = False
            self.encoder_degree(cur_l, cur_r, decel_step_deg, stop=step_stop)

    # ==========================================
    # GYRO MOVEMENTS
    # ==========================================

    def _gyro_move(self, mode, target, power, angle, stop, k_angle, k_rate, ki, min_power, accel_dist, decel_dist, compare, port=None):
        self._total_angle_error = 0  
        target_angle = -angle 
        direction = 1 if power >= 0 else -1
        max_power = abs(power)

        if mode == 'time':
            self._stopWatch.reset()
        elif mode in ('degree', 'acc'):
            self._reset_encoders()
            if mode == 'acc':
                distance = abs(target)
                target_counts = (distance * 360) / (WHEEL_SIZE * 3.14159)
                if (accel_dist + decel_dist) > distance:
                    ratio = distance / (accel_dist + decel_dist)
                    accel_dist *= ratio
                    decel_dist *= ratio
            else:
                target_counts = abs(target)

        while True:
            if mode == 'time' and self._stopWatch.time() >= target: break
            elif mode == 'degree' and self._get_encoders() >= target_counts: break
            elif mode == 'sensor':
                if ((self._get_sensor(port) < target) == compare): break
            elif mode == 'acc':
                current_counts = self._get_encoders()
                current_dist = (current_counts / 360) * (WHEEL_SIZE * 3.14159)
                if current_counts >= target_counts: break

            current_power = max_power
            if mode == 'acc':
                dist_remaining = distance - current_dist
                if current_dist < accel_dist:
                    current_power = min_power + (max_power - min_power) * (current_dist / accel_dist)
                elif dist_remaining < decel_dist:
                    current_power = min_power + (max_power - min_power) * (dist_remaining / decel_dist)

            active_power = current_power * direction

            current_angle = self._get_gyro_angle() 
            current_rate = self._hub.imu.angular_velocity(Axis.Z)
            
            angle_error = target_angle - current_angle
            self._total_angle_error += angle_error
            self._total_angle_error = max(-30, min(30, self._total_angle_error)) 
            
            correction = (k_angle * angle_error) - (k_rate * current_rate) + (ki * self._total_angle_error)

            left_duty = max(-100, min(100, -active_power + correction))
            right_duty = max(-100, min(100, active_power + correction))
            
            self._wro_drive(left_duty, right_duty)
            wait(10)

        if stop: self.robot_stop()

    def _gyro_turn(self, angle, move_wheel, stop, k_angle, k_rate, min_power, max_power, accel_angle, decel_angle):
        angle = -angle 
        start_angle = self._get_gyro_angle()
        total_deg = abs(angle - start_angle)
        timeout_ms = max(1000, total_deg * 20)

        if (accel_angle + decel_angle) > total_deg:
            ratio = total_deg / (accel_angle + decel_angle)
            accel_angle *= ratio
            decel_angle *= ratio

        self._stopWatch.reset()
        
        while True:
            current_angle = self._get_gyro_angle()
            current_rate = self._hub.imu.angular_velocity(Axis.Z)
            error = angle - current_angle
            deg_traveled = abs(current_angle - start_angle)
            
            if abs(error) <= 1: break       
            if self._stopWatch.time() > timeout_ms: break
                
            turn_power = (k_angle * error) - (k_rate * current_rate)
            limit = max_power
            if deg_traveled < accel_angle:
                limit = min_power + (max_power - min_power) * (deg_traveled / accel_angle)
            elif abs(error) < decel_angle:
                limit = min_power + (max_power - min_power) * (abs(error) / decel_angle)

            turn_power = max(-limit, min(limit, turn_power))
            if abs(turn_power) < min_power:
                turn_power = min_power if error > 0 else -min_power

            # Use the global constant checks!
            if move_wheel == RIGHT_DRIVE:
                self._left_drive.hold()
                self._right_drive.dc(turn_power)
            elif move_wheel == LEFT_DRIVE:
                self._right_drive.hold()
                self._left_drive.dc(-turn_power) 
            else:
                self._wro_drive(turn_power, turn_power) 
            
            wait(10)

        if stop: self.robot_stop()

    def gyro_time(self, power, duration, angle=0, stop=True):
        self._gyro_move('time', duration, power, angle, stop, self._pid["KP_GYRO"], self._pid["KD_GYRO"], self._pid["KI_GYRO"], 0, 0, 0, None)

    def gyro_degree(self, power, degree, angle=0, stop=True):
        self._gyro_move('degree', degree, power, angle, stop, self._pid["KP_GYRO"], self._pid["KD_GYRO"], self._pid["KI_GYRO"], 0, 0, 0, None)

    def gyro_sensor(self, power, port, threshold, compare=True, angle=0, stop=True):
        self._gyro_move('sensor', threshold, power, angle, stop, self._pid["KP_GYRO"], self._pid["KD_GYRO"], self._pid["KI_GYRO"], 0, 0, 0, compare, port)
        print(self._get_sensor(port))

    def gyro_acc(self, power, distance, angle=0, min_power=40, accel_dist=80, decel_dist=80, stop=True):
        self._gyro_move('acc', distance, power, angle, stop, self._pid["KP_GYRO"], self._pid["KD_GYRO"], self._pid["KI_GYRO"], min_power, accel_dist, decel_dist, None)

    def gyro_point_turn(self, angle, stop=True, accel_dist=10, decel_dist=20):
        self._gyro_turn(angle, None, stop, self._pid["KP_GYROPT"], self._pid["KD_GYROPT"], 45, 90, accel_dist, decel_dist)
        print(self._get_gyro_angle())

    def gyro_lock_turn(self, port, angle, stop=True, accel_dist=2, decel_dist=2):
        self._gyro_turn(angle, port, stop, self._pid["KP_GYROLT"], self._pid["KD_GYROLT"], 50, 90, decel_dist, decel_dist)
        print(self._get_gyro_angle())

    # ==========================================
    # LINE FOLLOW
    # ==========================================

    def _line_follow(self, mode, target, port, detect_port, direction, power, stop, kp, kd, compare):
        last_error = 0 
        if mode == 'time': self._stopWatch.reset()
        elif mode == 'degree': self._reset_encoders()

        while True:
            if mode == 'time' and self._stopWatch.time() >= target: break
            if mode == 'degree' and self._get_encoders() >= target: break
            if mode == 'sensor' and ((self._get_sensor(detect_port) < target) == compare): break
                
            error = (self._get_sensor(port) - 50) * direction
            correction = (error * kp) + ((error - last_error) * kd)
            last_error = error
            
            active_power = power - abs(error * 0.3)
            active_power = max(20, active_power) 
            
            left_duty = max(-100, min(100, -active_power - correction))
            right_duty = max(-100, min(100, active_power - correction))
            
            self._wro_drive(left_duty, right_duty)
            wait(10)

        if stop: self.robot_stop()

    def line_follow_time(self, direction, power, port, duration, stop=True):
        self._line_follow('time', duration, port, None, direction, power, stop, self._pid["KP_FAST"], self._pid["KD_FAST"], None)

    def line_follow_degree(self, direction, power, port, degree, stop=True):
        self._line_follow('degree', degree, port, None, direction, power, stop, self._pid["KP_FAST"], self._pid["KD_SLOW"], None)

    def line_follow_detect_reflected(self, direction, power, port, detect_port, threshold, compare=True, stop=True):
        self._line_follow('sensor', threshold, port, detect_port, direction, power, stop, self._pid["KP_SLOW"], self._pid["KD_FAST"], compare)

    def line_follow_acc(self, direction, max_power, port, total_degree, steps=3, accel_deg=100, decel_deg=100, min_power=50, stop=True, settling_time=0):
        total_ramp = accel_deg + decel_deg
        if total_ramp > total_degree:
            ratio = total_degree / total_ramp
            accel_deg *= ratio
            decel_deg *= ratio
            
        accel_step_deg = accel_deg / steps
        decel_step_deg = decel_deg / steps
        dir_p = 1 if max_power >= 0 else -1
        max_p = abs(max_power)

        # 1. Accelerate
        for i in range(1, steps + 1):
            fraction = i / steps 
            cur_p = (min_power + (max_p - min_power) * fraction) * dir_p
            self.line_follow_degree(direction, cur_p, port, None, accel_step_deg, stop=False)

        # 2. Cruise
        cruise_deg = total_degree - accel_deg - decel_deg
        if cruise_deg > 0:
            self.line_follow_degree(direction, max_power, port, None, cruise_deg, stop=False)

        # 3. Decelerate
        for i in range(steps - 1, -1, -1):
            fraction = i / steps
            step_stop = False
            if i == 0:
                cur_p = min_power * dir_p
                step_stop = stop
            else:
                cur_p = (min_power + (max_p - min_power) * fraction) * dir_p
            
            self.line_follow_degree(direction, cur_p, port, None, decel_step_deg, stop=step_stop)

    # ==========================================
    # PYBRICKS
    # ==========================================

    def move_curve_angle(self, radius, angle, speed, accel, stop_method, wait_complete):
        """
        Max speed = 1000 mm/s\n
        Max turn rate = 540 deg/s\n
        Max accel = 750 mm/s/s
        """
        self._drive_base.use_gyro(True)
        self._drive_base.reset()
        self._drive_base.settings(speed, accel, 500, accel)
        self._drive_base.curve(radius, angle, stop_method, wait_complete)

    def wait_for_adapter_free(self, left_power, right_power, left_limit, right_limit,
                            retract_left_speed=0, retract_right_speed=0,
                            retract_duration=500, timeout=5000):

        self._stopWatch.reset()

        while self._stopWatch.time() < timeout:
            # Drive both motors first, THEN read load
            self._left_adapter.dc(left_power)
            self._right_adapter.dc(right_power)
            wait(50)  # Let motors settle so load reading is meaningful

            left_load  = abs(self._left_adapter.load())
            right_load = abs(self._right_adapter.load())

            left_free  = left_load  < abs(left_limit)
            right_free = right_load < abs(right_limit)

            if left_free and right_free:
                break

            wait(10)

        self._left_adapter.brake()
        self._right_adapter.brake()

        # Retract
        if retract_left_speed != 0:
            self.adapter_motor_seconds(LEFT_ADAPTER,  speed=retract_left_speed,  duration=retract_duration, wait_complete=False)
        if retract_right_speed != 0:
            self.adapter_motor_seconds(RIGHT_ADAPTER, speed=retract_right_speed, duration=retract_duration, wait_complete=True)