######################## Pyricks library ########################
from pybricks.parameters import Color, Direction, Stop, Icon, Button
from pybricks.tools import wait, StopWatch
from ACL_FLL_v04_Cybertronics import *

################## Shared and local constants ##################

# Adapter configuration: (LeftPower, RightPower, LeftLimit, RightLimit)
ROUTE_ADAPTER_POWER = (-50, -50, 30, 30)

# Route-Specific PID Gains
STR_KP_CUSTOM = 1.5
STR_KD_CUSTOM = 1

GYRO_KP_CUSTOM = 0.7
GYRO_KD_CUSTOM = 0.2

LF_KP_CUSTOM = 0.4
LF_KD_CUSTOM = 0.1

######################## Route program ########################

# --- Starting position ---
# Blue base - Robot left wheel align 1.0 line from left
# Mission - Mountain rock

def Route6(laura: Laura):

    print("\n--- Starting Route 6 ---")
    routeTimer = StopWatch()
    laura.port_view_battery()
    routeTimer.reset()
    laura.hub_status_light(Color.MAGENTA)

    """ Start your code here """
    laura.wall_square()
    laura.gyro_lock_turn(RIGHT_DRIVE, -25)
    laura.gyro_lock_turn(LEFT_DRIVE, 0)
    laura.gyro_acc(80, 400, stop=False)
    laura.gyro_time(50, 1000)


    laura.adapter_motor_seconds(LEFT_ADAPTER, 600, 1000)
    laura.adapter_motor_seconds(LEFT_ADAPTER, -350, 1300, wait_complete=False)
    laura.adapter_motor_seconds(RIGHT_ADAPTER, 800, 1500)
    laura.adapter_motor_seconds(RIGHT_ADAPTER, -900, 1500)


    laura.gyro_degree(-150, 735, -40, stop=False)
    laura.gyro_lock_turn(RIGHT_DRIVE, 0, True, 100, 0)


    """ Route end """
    elapsed_time = routeTimer.time() / 1000
    print(f"Total Time: {elapsed_time:.2f} seconds")
    print("--- Route 6 Complete ---")

######################## Route testing ########################

# For individual route testing only.
if __name__ == "__main__":
    test = Laura()

    while not Button.RIGHT in test.hub_button_pressed():
        test.unregulated_adapter(*ROUTE_ADAPTER_POWER)
    
    test.adapter_motor_brake(LEFT_ADAPTER)
    test.adapter_motor_brake(RIGHT_ADAPTER)

    Route6(test)
