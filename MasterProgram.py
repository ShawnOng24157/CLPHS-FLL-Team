######################## Pybricks library ########################
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Axis, Button, Color, Direction, Port, Stop, Icon
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

from micropython import const                                                       

######################## Custom program ########################
from ACL_FLL_v04_Cybertronics import *
import Cybertronics_R1 as route1 
import Cybertronics_R2 as route2  
import Cybertronics_R3 as route3 
import Cybertronics_R4 as route4  
import Cybertronics_R5 as route5 
import Cybertronics_R6 as route6 
import Cybertronics_R7 as route7 
import Cybertronics_R8 as route8
import Cybertronics_R9 as route9 
import Cybertronics_R10 as route10
import Cybertronics_R11 as route11

######################## Total route ########################
_MAX_ROUTE = const(11) # Modify accordingly

# List of available route modules
ROUTE_MODULES = {
    1: route1, 2: route2, 3: route3, 4: route4, 5: route5,
    6: route6, 7: route7, 8: route8, 9: route9, 10: route10, 11: route11
}

# Dictionary mapping route number to the execution function
ROUTES = {
    1: route1.Route1, 2: route2.Route2, 3: route3.Route3, 4: route4.Route4, 5: route5.Route5,
    6: route6.Route6, 7: route7.Route7, 8: route8.Route8, 9: route9.Route9, 10: route10.Route10, 11: route11.Route11
}

######################## Main program ########################
def select_route(bot: Laura):
    current_route = 1
    
    while True:
        # 1. Update Hub Display & Status
        bot.hub_display_num(current_route)
        bot.hub_status_light(Color.CYAN)
        
        # 2. Continually Tension Adapters
        route_module = ROUTE_MODULES.get(current_route)
        adapter_powers = getattr(route_module, "ROUTE_ADAPTER_POWER", (0, 0, 60, 60))
        bot.unregulated_adapter(*adapter_powers)
        
        # 3. Check Button Presses
        pressed = bot.hub_button_pressed()
        
        # --- CYCLE LEFT ---
        if Button.LEFT in pressed:
            if current_route > 1:
                current_route -= 1
            while Button.LEFT in bot.hub_button_pressed():
                wait(10)
                
        # --- CYCLE RIGHT ---
        elif Button.BLUETOOTH in pressed:
            if current_route < _MAX_ROUTE:
                current_route += 1
            while Button.BLUETOOTH in bot.hub_button_pressed():
                wait(10)
                
        # --- EXECUTE ROUTE ---
        elif Button.RIGHT in pressed:
            bot.adapter_motor_brake(LEFT_ADAPTER)
            bot.adapter_motor_brake(RIGHT_ADAPTER)
            bot.hub_speaker_beep(150, 100)
            
            try:
                ROUTES[current_route](bot)
            except SystemExit:
                bot.robot_stop()
                continue
                
            # Auto-increment next route upon completion
            if current_route < _MAX_ROUTE:
                current_route += 1
                
            # Wait for button release before returning to loop
            while Button.RIGHT in bot.hub_button_pressed():
                wait(10)
                
        wait(10)

if __name__ == "__main__":
    laura = Laura()
    select_route(laura)