import time
import board

# import digitalio # For use with SPI
import adafruit_bmp280

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)


bmp280.sea_level_pressure = 1013.25

while True:
    print("\nTemperature: %0.1f C" % bmp280.temperature)
    print("Pressure: %0.1f hPa" % bmp280.pressure)
    print("Altitude = %0.2f meters" % bmp280.altitude)
    time.sleep(2)

# Print current altitude
initial_altitude = bmp280.altitude
print("Initial altitude: %.2f meters" % initial_altitude)

# Continuously check altitude every 0.1 seconds until it stops increasing
previous_altitude = initial_altitude
while True:
    altitude = bmp280.altitude
    print("Current altitude: %.2f meters" % altitude)

    # Check if altitude has stopped increasing
    if altitude <= previous_altitude:
        break

    previous_altitude = altitude

    time.sleep(0.1)
