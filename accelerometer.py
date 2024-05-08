import time
import board
import adafruit_adxl34x

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

# For ADXL343
accelerometer = adafruit_adxl34x.ADXL343(i2c)
# For ADXL345
# accelerometer = adafruit_adxl34x.ADXL345(i2c)

while True:
    print("%f %f %f" % accelerometer.acceleration)
    time.sleep(0.2)


# motion detection
accelerometer.enable_motion_detection()

while True:
    print("%f %f %f" % accelerometer.acceleration)

    print("Motion detected: %s" % accelerometer.events["motion"])
    time.sleep(0.5)

SAMPLE_INTERVAL = 1  # seconds
GRAVITY = 9.80665
initial_time = time.monotonic()

# Initial velocity
velocity_x = 0.0
velocity_y = 0.0
velocity_z = 0.0

while True:
    # Read acceleration data
    acceleration = accelerometer.acceleration

    # Calculate velocity using the trapezoidal rule
    current_time = time.monotonic()
    delta_time = current_time - initial_time

    velocity_x += (acceleration[0] * GRAVITY) * delta_time
    velocity_y += (acceleration[1] * GRAVITY) * delta_time
    velocity_z += (acceleration[2] * GRAVITY) * delta_time

    print("Velocity X: %.2f m/s, Velocity Y: %.2f m/s, Velocity Z: %.2f m/s" % (velocity_x, velocity_y, velocity_z))

    # Update initial time
    initial_time = current_time

    # Wait for the next sample interval
    time.sleep(SAMPLE_INTERVAL)
