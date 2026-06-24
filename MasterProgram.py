######################## Pyricks library ########################
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Axis, Button, Color, Direction, Port, Stop, Icon
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

# --- Import Core Library & Constants ---
from ACL_FLL_v04_Cybertronics import *

######################## Route Program Setup ########################

# Explicitly import route modules and assign them simple aliases.
import Cybertronics_R1 as route1 
import Cybertronics_R2 as route2  
import Cybertronics_R3 as route3 
import Cybertronics_R4 as route4  
import Cybertronics_R5 as route5 
import Cybertronics_R6 as route6 
import Cybertronics_R7 as route7 
import Cybertronics_R8 as route8
import Cybertronics_R9 as route9 

# List of available route modules
ROUTE_MODULES = {
    0: route0,
    1: route1,
    2: route2,
    3: route3,
    4: route4,
    5: route5,
    6: route6,
    7: route7,
    8: route8,
    9: route9
}

# Dictionary mapping route number to the execution function
ROUTES = {
    0: route0.Route0,
    1: route1.Route1,
    2: route2.Route2,
    3: route3.Route3,
    4: route4.Route4,
    5: route5.Route5,
    6: route6.Route6,
    7: route7.Route7,
    8: route8.Route8,
    9: route9.Route9
}

def run_adapters(bot: Laura, current_route: int):
    route_module = ROUTE_MODULES.get(current_route)
    
    adapter_powers = getattr(route_module, "ROUTE_ADAPTER_POWER", (0, 0, 0, 0)) if route_module else (0, 0, 0, 0)
    
    bot.unregulated_adapter(*adapter_powers)

# Main route selection and execution loop
def select_route(bot: Laura):    
    current_route = 1
    max_route = max(ROUTES.keys()) if ROUTES else 0

    if current_route not in ROUTES:
        current_route = min(ROUTES.keys()) if ROUTES else 0
        
    if max_route == 0:
        bot.hub_display_num(0)
        print("FATAL: No routes were loaded successfully.")
        return
    
    while True:
        bot.hub_display_num(current_route)
        
        # Continuously tension the arms for the selected route
        run_adapters(bot, current_route)

        pressed = bot.hub_button_pressed()

        # --- LAUNCH MISSION ---
        if Button.RIGHT in pressed:
            # Execute the chosen mission route
            mission_function = ROUTES.get(current_route)
            if mission_function:
                mission_function(bot)
            
            # After mission completes, move to the next route number
            if current_route < max_route:
                current_route += 1
            
            # Reset hub state after mission
            bot.hub_status_light(Color.CYAN)
            bot.hub_display_num(current_route)
            
            # Wait for them to release the center button before returning to menu
            while Button.RIGHT in bot.hub_button_pressed():
                wait(10)

        # --- CYCLE LEFT ---
        elif Button.LEFT in pressed:
            if current_route > 0:
                current_route -= 1
            while Button.LEFT in bot.hub_button_pressed():
                wait(10) 
            
        # --- CYCLE RIGHT ---
        elif Button.BLUETOOTH in pressed:
            if current_route < max_route:
                current_route += 1
            while Button.BLUETOOTH in bot.hub_button_pressed():
                wait(10)

        wait(10)

# --- Main Program Entry Point ---
if __name__ == "__main__":
    main_bot = Laura()
    select_route(main_bot)