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
altprev = bmp280.altitude

writedata = False
timeprev = time.monotonic()

with open("data.txt", "a") as fp:
    fp.write(f"Measurement start \n")

while True:
    buzzer.buzzer_tick()
    states.tick()


    altitude = bmp280.altitude
    pressure = bmp280.pressure
    acceleration = accelerometer.acceleration
    # print(f"Acceleration: {acceleration} \n")
    # print(f"Pressure: {pressure}, Altitude: {altitude} \n")

    # with open("data.txt", "a") as fp:
    #     fp.write(f"Acceleration: {acceleration} \n")


    # print(time.time())

    if(states.state == statemachine.States.LAUNCHED_MODE):
        writedata = True

        timenow = time.monotonic()
        if timenow - timeprev > 0.3:
            timeprev = timenow
            altitude = bmp280.altitude
            pressure = bmp280.pressure
            acceleration = accelerometer.acceleration

            if altitude <= altprev:
                alt_counter += 1
            else:
                alt_counter = 0
            altprev = altitude

            with open("data.txt", "a") as fp:
                fp.write(f"{acceleration} {pressure} {altitude} \n")
                # fp.write(f"Pressure: {pressure}, Altitude: {altitude} \n")
                # fp.write(str(time.time()))

        if alt_counter == 3:
            external.PYRO_DETONATE() # TODO: is this accounted for by line below?
            states.state == statemachine.States.DEPLOYED_MODE
    
    if(states.state == statemachine.States.DEPLOYED_MODE):
        timenow = time.monotonic()
        if timenow - timeprev > 0.3:
            timeprev = timenow
            altitude = bmp280.altitude
            pressure = bmp280.pressure
            acceleration = accelerometer.acceleration

            with open("data.txt", "a") as fp:
                fp.write(f"{acceleration} {pressure} {altitude} \n")
                # fp.write(f"Pressure: {pressure}, Altitude: {altitude} \n")