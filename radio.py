import time
import board
import busio
import digitalio
import adafruit_rfm69
import adafruit_adxl34x
import adafruit_bmp280

# Define radio parameters.
RADIO_FREQ_MHZ = 915.0  # Frequency of the radio in Mhz. Must match your module!
CS = digitalio.DigitalInOut(board.D5)
RESET = digitalio.DigitalInOut(board.D6)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm69 = adafruit_rfm69.RFM69(spi, CS, RESET, RADIO_FREQ_MHZ)

# Initialize the BMP280 sensor
i2c = busio.I2C(board.SCL, board.SDA)
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

# Initialize the ADXL345 accelerometer
accelerometer = adafruit_adxl34x.ADXL345(i2c)

# Optionally set an encryption key (16 byte AES key).
rfm69.encryption_key = (
    b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08"
)

# Main loop
while True:
    # Read altitude and pressure from BMP280 sensor
    altitude = bmp280.altitude
    pressure = bmp280.pressure

    # Read acceleration from ADXL345 accelerometer
    acceleration = accelerometer.acceleration

    # Calculate velocity using the trapezoidal rule
    velocity_x = acceleration[0] * 9.80665  # Convert from g to m/s^2
    velocity_y = acceleration[1] * 9.80665
    velocity_z = acceleration[2] * 9.80665

    # Prepare data to send
    data = bytearray()
    data.extend(bytearray(struct.pack("<f", altitude)))  # Pack altitude as float
    data.extend(bytearray(struct.pack("<f", pressure)))  # Pack pressure as float
    data.extend(bytearray(struct.pack("<f", velocity_x)))  # Pack velocity_x as float
    data.extend(bytearray(struct.pack("<f", velocity_y)))  # Pack velocity_y as float
    data.extend(bytearray(struct.pack("<f", velocity_z)))  # Pack velocity_z as float

    # Send data over RFM69 radio
    rfm69.send(data)

    # Print transmitted data for debugging
    print("Altitude:", altitude, "m")
    print("Pressure:", pressure, "hPa")
    print("Velocity X:", velocity_x, "m/s")
    print("Velocity Y:", velocity_y, "m/s")
    print("Velocity Z:", velocity_z, "m/s")

    # Wait for a short interval before sending the next data
    time.sleep(1)
