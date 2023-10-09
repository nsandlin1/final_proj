import adafruit_dht
import board
import time

# initialize dht device without pulse
thermometer = adafruit_dht.DHT22(board.D4, use_pulseio=False)

while True:
    try: 
        temp_F = str(thermometer.temperature * (9/5) + 32)
        humidity = str(thermometer.humidity)

        print("Temperature: {:10s}  Humidity: {:10s}".format(temp_F, humidity))

    except Exception:
        raise Exception

    time.sleep(2)
