######################## Pyricks library ########################
from pybricks.parameters import Color, Direction, Stop, Icon, Button
from pybricks.tools import wait, StopWatch
from ACL_FLL_v04_Cybertronics import *

################## Shared and local constants ##################

# Adapter configuration: (LeftPower, RightPower, LeftLimit, RightLimit)
ROUTE_ADAPTER_POWER = (-40, -40, 30, 30)

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

def Route9(laura: Laura):

    print("\n--- Starting Route 9 ---")
    routeTimer = StopWatch()
    laura.port_view_battery()
    routeTimer.reset()
    laura.hub_status_light(Color.MAGENTA)

    """ Start your code here """
    laura.wall_square()
    laura.encoder_degree(70, 0, 40)
    laura.gyro_acc(80, 420, 24)
    laura.encoder_degree(80, -80, 305)
    laura.gyro_acc(-80, 500, 180, 50, stop=False)
    laura.gyro_time(-50, 350, 180, False)
    laura.gyro_acc(60, 15, 180)
    wait(200)
    laura.adapter_motor_seconds(RIGHT_ADAPTER, 300, 1000, wait_complete=False)
    laura.encoder_degree(-70, 70, 170)
    laura.encoder_acc(45, 50, 200)
    laura.adapter_motor_seconds(LEFT_ADAPTER, 600, 1000)

    laura.encoder_time(45, 50, 600)
    laura.adapter_motor_seconds(RIGHT_ADAPTER, -150, 1500, wait_complete=False)
    laura.adapter_motor_seconds(LEFT_ADAPTER, -300, 1200, wait_complete=False)
    wait(2000)
    laura.encoder_acc(-60, -60, 200, stop=False)
    laura.gyro_point_turn(192, decel_dist=70, stop=False)
    laura.gyro_acc(120, 850, 192)
    wait(350)
    laura.gyro_point_turn(0, True, 100, 0)
    

    """ Route end """
    elapsed_time = routeTimer.time() / 1000
    print(f"Total Time: {elapsed_time:.2f} seconds")
    print("--- Route 9 Complete ---")

######################## Route testing ########################

# For individual route testing only.
if __name__ == "__main__":
    test = Laura()

    while not Button.RIGHT in test.hub_button_pressed():
        test.unregulated_adapter(*ROUTE_ADAPTER_POWER)
    
    test.adapter_motor_brake(LEFT_ADAPTER)
    test.adapter_motor_brake(RIGHT_ADAPTER)

    Route9(test)
