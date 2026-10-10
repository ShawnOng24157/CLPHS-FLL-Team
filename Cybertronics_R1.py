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
    laura.gyro_acc(70, 240)
    laura.encoder_degree(-80, 80, 150, False)
    laura.gyro_point_turn(-90, False)
    laura.gyro_acc(75, 570, -90, 50, stop=False)
    laura.line_follow_detect_reflected(1, 50, LEFT_COLOUR, RIGHT_COLOUR, 10)
    laura.gyro_degree(60, 25, -90)
    laura.adapter_motor_seconds(LEFT_ADAPTER, -1000, 1200, wait_complete=False)
    laura.gyro_point_turn(-180)
    laura.adapter_motor_degree(LEFT_ADAPTER, 1000, 200, wait_complete=False)
    laura.gyro_acc(-80, 550, -180, stop=False)
    laura.adapter_motor_seconds(LEFT_ADAPTER, -1000, 1000, wait_complete=False)
    laura.gyro_acc(-80, 100, -180, 50, stop=False)
    laura.gyro_time(-45, 650, -180)
    laura.gyro_degree(60, 20, -180)
    laura.encoder_degree(-50, 50, 180)
    laura.adapter_motor_seconds(LEFT_ADAPTER, 1000, 1600, wait_complete=False)
    wait(600)
    laura.encoder_degree(50, 53, 200, stop=False)
    laura.encoder_time(50, 53, 700)
    laura.gyro_degree(-45, 50, -270)
    laura.adapter_motor_seconds(LEFT_ADAPTER, -700, 1400)
    wait(400)
    laura.adapter_motor_seconds(LEFT_ADAPTER, 1000, 500, wait_complete=False)
    laura.gyro_degree(-45, 60, -270)
    laura.adapter_motor_seconds(RIGHT_ADAPTER, 1000, 800)
    laura.gyro_degree(-45, 360, -270)
    laura.adapter_motor_seconds(LEFT_ADAPTER, -1000, 1000, wait_complete=False)
    # laura.gyro_point_turn(-190)
    laura.gyro_lock_turn(LEFT_DRIVE, -188)
    laura.gyro_degree(85, 1100, -188)
    laura.gyro_point_turn(-270)
    laura.encoder_degree(100, 90, 1300)
    wait(500)
    laura.gyro_point_turn(0, True, 100, 0)


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
