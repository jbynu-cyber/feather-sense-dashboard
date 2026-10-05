```python
import board
import time
import displayio
import terminalio

from adafruit_display_text import label
from adafruit_displayio_ssd1306 import SSD1306

import adafruit_lsm6ds.lsm6dsox
import adafruit_lps2x
import adafruit_sht31d


# ---------------------------------------------------------
# Set up sensors
# ---------------------------------------------------------

i2c = board.I2C()

# Accelerometer
accelerometer = adafruit_lsm6ds.lsm6dsox.LSM6DSOX(i2c)

# Pressure
pressure_sensor = adafruit_lps2x.LPS25(i2c)

# Temperature and humidity
humidity_sensor = adafruit_sht31d.SHT31D(i2c)


# ---------------------------------------------------------
# Set up OLED
# ---------------------------------------------------------

displayio.release_displays()

display_bus = displayio.I2CDisplay(
    i2c,
    device_address=0x3C
)

display = SSD1306(
    display_bus,
    width=128,
    height=64
)


# ---------------------------------------------------------
# Function to create the display
# ---------------------------------------------------------

def show_dashboard(landscape, temperature, pressure,
                   humidity, x, y, z):

    splash = displayio.Group()

    # -----------------------------------------------------
    # Landscape layout
    # -----------------------------------------------------
    if landscape:

        title = label.Label(
            terminalio.FONT,
            text="FEATHER SENSE",
            color=0xFFFFFF,
            x=27,
            y=7
        )
        splash.append(title)

        temp_text = label.Label(
            terminalio.FONT,
            text="Temp: {:.1f} C".format(temperature),
            color=0xFFFFFF,
            x=2,
            y=20
        )
        splash.append(temp_text)

        pressure_text = label.Label(
            terminalio.FONT,
            text="Press: {:.1f}".format(pressure),
            color=0xFFFFFF,
            x=2,
            y=32
        )
        splash.append(pressure_text)

        humidity_text = label.Label(
            terminalio.FONT,
            text="Hum: {:.1f}%".format(humidity),
            color=0xFFFFFF,
            x=2,
            y=44
        )
        splash.append(humidity_text)

        accel_text = label.Label(
            terminalio.FONT,
            text="X:{:.1f} Y:{:.1f} Z:{:.1f}".format(x, y, z),
            color=0xFFFFFF,
            x=2,
            y=57
        )
        splash.append(accel_text)

    # -----------------------------------------------------
    # Portrait layout
    # -----------------------------------------------------
    else:

        title = label.Label(
            terminalio.FONT,
            text="SENSE",
            color=0xFFFFFF,
            x=45,
            y=7
        )
        splash.append(title)

        temp_text = label.Label(
            terminalio.FONT,
            text="TEMP",
            color=0xFFFFFF,
            x=5,
            y=19
        )
        splash.append(temp_text)

        temp_value = label.Label(
            terminalio.FONT,
            text="{:.1f} C".format(temperature),
            color=0xFFFFFF,
            x=65,
            y=19
        )
        splash.append(temp_value)

        pressure_text = label.Label(
            terminalio.FONT,
            text="PRESS",
            color=0xFFFFFF,
            x=5,
            y=31
        )
        splash.append(pressure_text)

        pressure_value = label.Label(
            terminalio.FONT,
            text="{:.1f}".format(pressure),
            color=0xFFFFFF,
            x=65,
            y=31
        )
        splash.append(pressure_value)

        humidity_text = label.Label(
            terminalio.FONT,
            text="HUM",
            color=0xFFFFFF,
            x=5,
            y=43
        )
        splash.append(humidity_text)

        humidity_value = label.Label(
            terminalio.FONT,
            text="{:.1f}%".format(humidity),
            color=0xFFFFFF,
            x=65,
            y=43
        )
        splash.append(humidity_value)

        accel_text = label.Label(
            terminalio.FONT,
            text="X {:.1f}".format(x),
            color=0xFFFFFF,
            x=5,
            y=55
        )
        splash.append(accel_text)

        accel_y = label.Label(
            terminalio.FONT,
            text="Y {:.1f}".format(y),
            color=0xFFFFFF,
            x=50,
            y=55
        )
        splash.append(accel_y)

        accel_z = label.Label(
            terminalio.FONT,
            text="Z {:.1f}".format(z),
            color=0xFFFFFF,
            x=95,
            y=55
        )
        splash.append(accel_z)

    display.root_group = splash


# ---------------------------------------------------------
# Main loop
# ---------------------------------------------------------

while True:

    # Get sensor readings
    temperature = humidity_sensor.temperature
    humidity = humidity_sensor.relative_humidity
    pressure = pressure_sensor.pressure

    x, y, z = accelerometer.acceleration

    # Determine orientation using accelerometer.
    #
    # If X is stronger than Y, the board is being held
    # horizontally. Otherwise it is being held vertically.
    #
    # This threshold prevents the display from constantly
    # changing while the board is close to level.

    if abs(x) > abs(y):
        landscape = True
    else:
        landscape = False

    # Update dashboard
    show_dashboard(
        landscape,
        temperature,
        pressure,
        humidity,
        x,
        y,
        z
    )

    time.sleep(0.5)
```
