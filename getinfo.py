import adafruit_dht
import board
import time
from prometheus_client import start_http_server, Gauge, Summary

collection_interval = 1

temperature = Gauge("temperature_data", "temperature data gathered by DHT22")
humidity = Gauge("humdity_data", "humidity data gathered by DHT22")

# initialize dht device without pulse
thermometer = adafruit_dht.DHT22(board.D4, use_pulseio=False)

def truncate(my_float, n):
    new_int = int(my_float*(10**n)) / (10**n)
    return new_int

def get_temp_data():
    while True:
        try: 
            temp_F = thermometer.temperature * (9/5) + 32
            temp_F = str(truncate(temp_F, 2))

            humidity = thermometer.humidity
            humidity = str(truncate(humidity, 2))

            print("Temperature: {:10s}  Humidity: {:10s}".format(temp_F, humidity))

        except RuntimeError:
            pass

        except Exception:
            raise Exception

        time.sleep(collection_interval)

def main(): 
    start_http_server(9111)
    get_temp_data()

if __name__ == '__main__':
    main()

