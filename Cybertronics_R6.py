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
    laura.gyro_acc(75, 450, -2.5, stop=False)
    laura.gyro_time(45, 400)
    laura.adapter_motor_seconds(LEFT_ADAPTER, 1000, 800)
    laura.adapter_motor_seconds(LEFT_ADAPTER, -400, 1500, wait_complete=False)
    wait(800)
    laura.adapter_motor_seconds(RIGHT_ADAPTER, 500, 2000)
    laura.adapter_motor_seconds(RIGHT_ADAPTER, -1000, 1000, wait_complete=False)
    wait(900)
    laura.gyro_degree(-80, 100, 0, False)
    laura.gyro_degree(-120, 750, -30, False)
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
