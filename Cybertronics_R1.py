######################## Pyricks library ########################
from pybricks.parameters import Color, Direction, Stop, Icon, Button
from pybricks.tools import wait, StopWatch
from ACL_FLL_v04_Cybertronics import *

################## Shared and local constants ##################

# Adapter configuration: (LeftPower, RightPower, LeftLimit, RightLimit)
ROUTE_ADAPTER_POWER = (0, 40, 30, 30)

# Route-Specific PID Gains
STR_KP_CUSTOM = 1.5
STR_KD_CUSTOM = 1

GYRO_KP_CUSTOM = 0.7
GYRO_KD_CUSTOM = 0.2

LF_KP_CUSTOM = 0.4
LF_KD_CUSTOM = 0.1

######################## Route program ########################

# --- Starting position ---
# Blue base - Robot right wheel align 1st line from right
# Mission - Mountain rock

def Route1(laura: Laura):

    print("\n--- Starting Route 1 ---")
    routeTimer = StopWatch()
    laura.port_view_battery()
    routeTimer.reset()
    laura.hub_status_light(Color.MAGENTA)

    """ Start your code here """
    laura.wall_square()
    laura.adapter_motor_seconds(RIGHT_ADAPTER, -600, 900, Stop.BRAKE, False)
    laura.gyro_acc(75, 247)
    laura.encoder_degree(-70, 70, 165)
    laura.gyro_acc(75, 630, -90, 50, decel_dist=150, stop=False)
    laura.line_follow_detect_reflected(1, 50, LEFT_COLOUR, RIGHT_COLOUR, 10, stop=False)
    laura.gyro_acc(80, 80, -90, stop=False)
    laura.adapter_motor_seconds(LEFT_ADAPTER, -1000, 1400, Stop.BRAKE, False)
    laura.encoder_degree(-80, 0, 205)
    laura.adapter_motor_degree(LEFT_ADAPTER, 1000, 200, wait_complete=False)
    laura.gyro_degree(-80, 1000, -180, False)
    laura.adapter_motor_degree(LEFT_ADAPTER, -1000, 350, wait_complete=False)
    laura.gyro_time(-50, 500, -180)
    laura.gyro_acc(70, 12, -180)
    laura.encoder_degree(-70, 70, 165)
    laura.adapter_motor_seconds(LEFT_ADAPTER, 1000, 1700, wait_complete=False)
    wait(500)
    laura.encoder_time(45, 49, 1700)
    laura.gyro_degree(-40, 15, -270)
    laura.adapter_motor_seconds(LEFT_ADAPTER, -600, 1450)
    wait(200)
    laura.adapter_motor_seconds(LEFT_ADAPTER, 800, 600, Stop.COAST, False)
    wait(900)
    laura.encoder_degree(-60, -60, 65)
    laura.adapter_motor_seconds(RIGHT_ADAPTER, 1000, 800)
    laura.encoder_degree(-60, -60, 35, False)
    laura.adapter_motor_seconds(LEFT_ADAPTER, -1000, 1900, Stop.COAST, False)
    laura.encoder_degree(-70, -70, 440, False)
    laura.gyro_lock_turn(LEFT_DRIVE, -192)
    laura.adapter_motor_degree(LEFT_ADAPTER, 1000, 120, True, Stop.BRAKE, False)
    wait(300)
    laura.gyro_acc(80, 645, -192)
    laura.gyro_point_turn(-270)
    laura.gyro_degree(100, 600, -270, False)
    laura.adapter_motor_seconds(LEFT_ADAPTER, -1000, 700, wait_complete=False)
    laura.gyro_degree(120, 700, -240, True)
    wait(400)
    laura.gyro_point_turn(0, True, 100, 360)

    """ Route end """
    elapsed_time = routeTimer.time() / 1000
    print(f"Total Time: {elapsed_time:.2f} seconds")
    print("--- Route 1 Complete ---")

######################## Route testing ########################

# For individual route testing only.
if __name__ == "__main__":
    test = Laura()
    
    while not Button.RIGHT in test.hub_button_pressed():
        test.unregulated_adapter(*ROUTE_ADAPTER_POWER)
    
    test.adapter_motor_brake(LEFT_ADAPTER)
    test.adapter_motor_brake(RIGHT_ADAPTER)

    Route1(test)
