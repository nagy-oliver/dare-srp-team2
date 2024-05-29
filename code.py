import board
import external
import time
import measure
import statemachine
import buzzer
import config
import time

delay_pyro_miliseconds = config.get_deployment_timer()
print(f'Read in a delay of {delay_pyro_miliseconds} ms from the config file')

states = statemachine.Statemachine(PYRO_FIRE_DELAY_MS = delay_pyro_miliseconds)

# i2c = busio.I2C(board.SCL, board.SDA)
i2c = board.I2C()

import adafruit_mpu6050
accelerometer = adafruit_mpu6050.MPU6050(i2c)


import adafruit_bmp280
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, 0x76)
bmp280.sea_level_pressure = 1013.25

alt_counter = 0
altmax = bmp280.altitude

writedata = False

while True:
    buzzer.buzzer_tick()
    states.tick()
    altitude = bmp280.altitude
    pressure = bmp280.pressure
    acceleration = accelerometer.acceleration
    # print(f"Acceleration: {acceleration} \n")
    # print(f"Pressure: {pressure}, Altitude: {altitude} \n")


    # print(time.time())

    if(states.state == statemachine.States.LAUNCHED_MODE):
        writedata = True

        if altitude <= altmax:
            alt_counter += 1
        else:
            alt_counter = 0
        altmax = altitude

        if alt_counter == 3:
            external.PYRO_DETONATE()
       
            # print(accelerometer.acceleration)
            # print(bmp280.pressure)
            # print(bmp280.altitude)
        time.sleep(1)

    if writedata:
        with open("data.txt", "w") as fp:
            fp.write(f"Acceleration: {acceleration} \n")
            fp.write(f"Pressure: {pressure}, Altitude: {altitude} \n")
            # fp.write(str(time.time_ns()))