######################## Pyricks library ########################
from pybricks.parameters import Color, Direction, Stop, Icon, Button
from pybricks.tools import wait, StopWatch
from ACL_FLL_v04_Cybertronics import *

################## Shared and local constants ##################

# Adapter configuration: (LeftPower, RightPower, LeftLimit, RightLimit)
ROUTE_ADAPTER_POWER = (-40, 100, 30, 30)

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

def Route11(laura: Laura):

    print("\n--- Starting Route 11 ---")
    routeTimer = StopWatch()
    laura.port_view_battery()
    routeTimer.reset()
    laura.hub_status_light(Color.MAGENTA)

    """ Start your code here """
    laura.wall_square()
    laura.gyro_acc(70, 240)
    laura.encoder_degree(80, -80, 155, False)
    laura.gyro_acc(75, 700, 90, 50, stop=False)
    laura.line_follow_degree(-1, 50, RIGHT_COLOUR, 300)
    laura.gyro_point_turn(0)
    laura.gyro_acc(75, 550)
    laura.gyro_point_turn(90)
    laura.gyro_acc(65, 250, 90)
    laura.gyro_lock_turn(LEFT_DRIVE, 0)
    laura.gyro_time(60, 850)
    laura.adapter_motor_seconds(LEFT_ADAPTER, 1000, 800, wait_complete=False)
    laura.adapter_motor_seconds(RIGHT_ADAPTER, 1000, 2000)



    """ Route end """
    elapsed_time = routeTimer.time() / 1000
    print(f"Total Time: {elapsed_time:.2f} seconds")
    print("--- Route 11 Complete ---")

######################## Route testing ########################

# For individual route testing only.
if __name__ == "__main__":
    test = Laura()

    while not Button.RIGHT in test.hub_button_pressed():
        test.unregulated_adapter(*ROUTE_ADAPTER_POWER)
    
    test.adapter_motor_brake(LEFT_ADAPTER)
    test.adapter_motor_brake(RIGHT_ADAPTER)

    Route11(test)
