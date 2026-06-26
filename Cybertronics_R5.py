######################## Pyricks library ########################
from pybricks.parameters import Color, Direction, Stop, Icon, Button
from pybricks.tools import wait, StopWatch
from ACL_FLL_v04_Cybertronics import *

################## Shared and local constants ##################

# Adapter configuration: (LeftPower, RightPower, LeftLimit, RightLimit)
ROUTE_ADAPTER_POWER = (40, 40, 30, 30)

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

def Route5(laura: Laura):

    print("\n--- Starting Route 5 ---")
    routeTimer = StopWatch()
    laura.port_view_battery()
    routeTimer.reset()
    laura.hub_status_light(Color.MAGENTA)

    """ Start your code here """
    laura.wall_square()
    laura.gyro_acc(75, 170)
    laura.encoder_degree(-70, 70, 165)
    laura.gyro_acc(75, 600, -90, 50, decel_dist=150) #580
    laura.gyro_point_turn(0, False)
    laura.gyro_time(-50, 700)
    laura.adapter_motor_seconds(LEFT_ADAPTER, -1000, 1500)
    laura.adapter_motor_seconds(LEFT_ADAPTER, 1000, 800, Stop.COAST, False)
    laura.adapter_motor_seconds(RIGHT_ADAPTER, -300, 650, wait_complete=False)
    wait(150)
    laura.gyro_acc(120, 100, stop=False)
    laura.encoder_degree(-80, 80, 95)
    # laura.encoder_acc(70, 70, 600)

    laura.gyro_acc(60, 260, -55)

    laura.adapter_motor_seconds(RIGHT_ADAPTER, 400, 1200, wait_complete=False)
    wait(250)
    laura.encoder_time(60, 0, 700)
    laura.gyro_lock_turn(LEFT_DRIVE, -110, stop=False)
    laura.gyro_acc(120, 800, -110)

    
    """ Route end """
    elapsed_time = routeTimer.time() / 1000
    print(f"Total Time: {elapsed_time:.2f} seconds")
    print("--- Route 5 Complete ---")

######################## Route testing ########################

# For individual route testing only.
if __name__ == "__main__":
    test = Laura()

    while not Button.RIGHT in test.hub_button_pressed():
        test.unregulated_adapter(*ROUTE_ADAPTER_POWER)
    
    test.adapter_motor_brake(LEFT_ADAPTER)
    test.adapter_motor_brake(RIGHT_ADAPTER)

    Route5(test)