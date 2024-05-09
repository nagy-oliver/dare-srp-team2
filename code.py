import board
import external
import time
import measure
import statemachine
import buzzer
import config

delay_pyro_miliseconds = config.get_deployment_timer()
print(f'Read in a delay of {delay_pyro_miliseconds} ms from the config file')

states = statemachine.Statemachine(PYRO_FIRE_DELAY_MS = delay_pyro_miliseconds)

i2c = board.I2C()

import adafruit_adxl34x
accelerometer = adafruit_adxl34x.ADXL343(i2c)
# accelerometer.acceleration

import adafruit_bmp280
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
bmp280.sea_level_pressure = 1013.25
# bmp280.pressure
# bmp280.altitude

with open("data.txt", "w") as fp:
   while True:
      buzzer.buzzer_tick()
      states.tick()

      fp.write(f"{accelerometer.acceleration} \n")
      fp.write(f"Pressure: {bmp280.pressure}, Altitude: {bmp280.altitude} \n")
      # print(accelerometer.acceleration)
      # print(bmp280.pressure)
      # print(bmp280.altitude)


# external.PYRO_DETONATE()