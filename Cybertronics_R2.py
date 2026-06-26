######################## Pyricks library ########################
from pybricks.parameters import Color, Direction, Stop, Icon, Button
from pybricks.tools import wait, StopWatch
from ACL_FLL_v04_Cybertronics import *

################## Shared and local constants ##################

# Adapter configuration: (LeftPower, RightPower, LeftLimit, RightLimit)
ROUTE_ADAPTER_POWER = (-40, 50, 30, 30)

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

def Route2(laura: Laura):

    print("\n--- Starting Route 2 ---")
    routeTimer = StopWatch()
    laura.port_view_battery()
    routeTimer.reset()
    laura.hub_status_light(Color.ORANGE)

    """ Start your code here """
    laura.wall_square()
    laura.gyro_acc(80, 250, stop=False)
    laura.encoder_degree(0, 70, 90, False)
    laura.gyro_acc(80, 400, -43, stop=False)
    laura.gyro_point_turn(43, False)
    laura.gyro_degree(60, 100, 43, False)
    laura.adapter_motor_seconds(RIGHT_ADAPTER, -1000, 700, wait_complete=False)
    laura.gyro_time(50, 950, 43)
    laura.adapter_motor_seconds(LEFT_ADAPTER, 1000, 800)
    laura.adapter_motor_seconds(RIGHT_ADAPTER, 400, 1200)
    laura.adapter_motor_seconds(LEFT_ADAPTER, -1000, 900, Stop.BRAKE, False)
    laura.gyro_acc(-80, 150, 45, stop=False)
    laura.gyro_point_turn(-20, False)
    laura.gyro_degree(-150, 600, -10, stop=False)
    laura.gyro_degree(-150, 500, 0, stop=False)
    laura.gyro_lock_turn(RIGHT_DRIVE, 0)

    """ Route end """
    elapsed_time = routeTimer.time() / 1000
    print(f"Total Time: {elapsed_time:.2f} seconds")
    print("--- Route 2 Complete ---")

######################## Route testing ########################

# For individual route testing only.
if __name__ == "__main__":
    test = Laura()

    while not Button.RIGHT in test.hub_button_pressed():
        test.unregulated_adapter(*ROUTE_ADAPTER_POWER)
    
    test.adapter_motor_brake(LEFT_ADAPTER)
    test.adapter_motor_brake(RIGHT_ADAPTER)

    Route2(test)