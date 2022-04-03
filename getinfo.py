import Adafruit_DHT
import board
import time
from prometheus_client import start_http_server, Gauge, Summary

collection_interval = 5

temperature = Gauge("temperature_data", "temperature data gathered by DHT22")
humidity = Gauge("humdity_data", "humidity data gathered by DHT22")

# initialize dht device without pulse
thermometer = Adafruit_DHT.DHT22(board.D4, use_pulseio=False)

def get_temp_data():
    while True:
        try: 
            temp_F = str(thermometer.temperature * (9/5) + 32)
            humidity = str(thermometer.humidity)

            print("Temperature: {:10s}  Humidity: {:10s}".format(temp_F, humidity))

        except Exception:
            raise Exception

        time.sleep(collection_interval)

def main(): 
    start_http_server(9111)
    get_temp_data()

if __name__ == '__main__':
    main()

