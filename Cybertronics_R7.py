######################## Pyricks library ########################
from pybricks.parameters import Color, Direction, Stop, Icon, Button
from pybricks.tools import wait, StopWatch
from ACL_FLL_v04_Cybertronics import *

################## Shared and local constants ##################

# Adapter configuration: (LeftPower, RightPower, LeftLimit, RightLimit)
ROUTE_ADAPTER_POWER = (0, 0, 30, 30)

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

def Route7(laura: Laura):

    print("\n--- Starting Route 7 ---")
    routeTimer = StopWatch()
    laura.port_view_battery()
    routeTimer.reset()
    laura.hub_status_light(Color.MAGENTA)

    """ Start your code here """

    laura.wall_square()
    # laura.adapter_motor_seconds(LEFT_ADAPTER,200,500,Stop.BRAKE,True)
    laura.encoder_degree(50,50,1260,True)
    # laura.gyro_lock_turn(RIGHT_DRIVE, -47, 1)
    laura.gyro_point_turn(-45, True,2)
    laura.encoder_degree(50,50,270,True)
    #laura.encoder_degree(-50,-50,40,True)
    #laura.adapter_motor_seconds(RIGHT_ADAPTER,-500,600,Stop.BRAKE,True)
    #laura.encoder_degree(-100,-100,100,True)
    




    """ Route end """
    elapsed_time = routeTimer.time() / 1000
    print(f"Total Time: {elapsed_time:.2f} seconds")
    print("--- Route 7 Complete ---")

######################## Route testing ########################

# For individual route testing only.
if __name__ == "__main__":
    test = Laura()

    while not Button.RIGHT in test.hub_button_pressed():
        test.unregulated_adapter(*ROUTE_ADAPTER_POWER)
    
    test.adapter_motor_brake(LEFT_ADAPTER)
    test.adapter_motor_brake(RIGHT_ADAPTER)

    Route7(test)
