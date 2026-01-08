#!/usr/bin/env python3

import os
import time

# Battery paths
batt_life = "/sys/class/power_supply/battery/capacity"
batt_status = "/sys/class/power_supply/battery/status"

# GPIO paths from your debug
RED_GPIO12 = "/sys/class/gpio/gpio12/value"   # red_led_1
RED_GPIO17 = "/sys/class/gpio/gpio17/value"   # red_led
BLUE_GPIO0 = "/sys/class/gpio/gpio0/value"    # blue_led
BLUE_GPIO11 = "/sys/class/gpio/gpio11/value"  # blue_led_1

# Export GPIOs if needed
for gpio in ["0", "11", "12", "17"]:
    gpio_path = f"/sys/class/gpio/gpio{gpio}"
    if not os.path.exists(gpio_path):
        try:
            with open("/sys/class/gpio/export", "w") as f:
                f.write(gpio)
        except:
            pass
    direction_path = f"{gpio_path}/direction"
    if os.path.exists(direction_path):
        with open(direction_path, "w") as f:
            f.write("out")

while True:
    try:
        cap = int(open(batt_life, "r").read().strip())
        status = open(batt_status, "r").read().strip()
    except:
        cap = 50
        status = "Unknown"
        time.sleep(10)
        continue

    # Reset all LEDs first
    for gpio in [RED_GPIO12, RED_GPIO17, BLUE_GPIO0, BLUE_GPIO11]:
        with open(gpio, "w") as f:
            f.write("0")

    if status == "Charging":
        # Charging: Pink (red + blue on)
        with open(RED_GPIO12, "w") as f: f.write("1")
        with open(RED_GPIO17, "w") as f: f.write("1")
        with open(BLUE_GPIO0, "w") as f: f.write("1")
        with open(BLUE_GPIO11, "w") as f: f.write("1")
    else:
        if cap > 20:
            # Blue on (>20%)
            with open(BLUE_GPIO0, "w") as f: f.write("1")
            with open(BLUE_GPIO11, "w") as f: f.write("1")
        elif cap > 10:
            # Solid red (11% to 20%)
            with open(RED_GPIO12, "w") as f: f.write("1")
            with open(RED_GPIO17, "w") as f: f.write("1")
        else:
            # Blinking red (≤10%)
            with open(RED_GPIO12, "w") as f: f.write("1")
            with open(RED_GPIO17, "w") as f: f.write("1")
            time.sleep(0.5)
            with open(RED_GPIO12, "w") as f: f.write("0")
            with open(RED_GPIO17, "w") as f: f.write("0")
            time.sleep(0.5)

    time.sleep(5)  # Check every 5 seconds
