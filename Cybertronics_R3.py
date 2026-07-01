######################## Pyricks library ########################
from pybricks.parameters import Color, Direction, Stop, Icon, Button
from pybricks.tools import wait, StopWatch
from ACL_FLL_v04_Cybertronics import *

################## Shared and local constants ##################

# Adapter configuration: (LeftPower, RightPower, LeftLimit, RightLimit)
ROUTE_ADAPTER_POWER = (-30, 30, 30, 30)

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

def Route3(laura: Laura):

    print("\n--- Starting Route 3 ---")
    routeTimer = StopWatch()
    laura.port_view_battery()
    routeTimer.reset()
    laura.hub_status_light(Color.MAGENTA)

    """ Start your code here """
    laura.wall_square()
    laura.adapter_motor_seconds(RIGHT_ADAPTER, -200, 400, wait_complete=False)
    laura.gyro_lock_turn(RIGHT_DRIVE, -45)
    laura.gyro_acc(70, 300, -43, 45, stop=False)
    laura.gyro_time(45, 1000, -43)
    laura.adapter_motor_seconds(RIGHT_ADAPTER, -600, 1000)
    laura.adapter_motor_seconds(LEFT_ADAPTER, 300, 1000, wait_complete=False)
    laura.encoder_time(-60, -60, 800)
    laura.encoder_degree(65, 65, 40)
    laura.adapter_motor_seconds(RIGHT_ADAPTER, 600, 800)
    # laura.encoder_acc(-120, -120, 720, stop=False)
    # laura.gyro_lock_turn(RIGHT_DRIVE, 0)
    


    """ Route end """
    elapsed_time = routeTimer.time() / 1000
    print(f"Total Time: {elapsed_time:.2f} seconds")
    print("--- Route 3 Complete ---")

######################## Route testing ########################

# For individual route testing only.
if __name__ == "__main__":
    test = Laura()

    while not Button.RIGHT in test.hub_button_pressed():
        test.unregulated_adapter(*ROUTE_ADAPTER_POWER)
    
    test.adapter_motor_brake(LEFT_ADAPTER)
    test.adapter_motor_brake(RIGHT_ADAPTER)

    Route3(test)