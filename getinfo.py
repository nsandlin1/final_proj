import adafruit_dht
import board
import time
from prometheus_client import start_http_server, Gauge, Summary

# Humidity is non-implemented feature. Collected and stored in prometheus
# but not yet graphed.

# data collection interval in seconds
collection_interval = 5

# Guage is a custom class that is part of the prometheus_client package. It is
# used to advertise custom metrics to prometheus service. Guage custom object
# can be incremented, decremented, or set to a specified value
temperature = Gauge("temperature_data", "temperature data gathered by DHT22")
humidity = Gauge("humdity_data", "humidity data gathered by DHT22")

# initialize dht device without pulse
thermometer = adafruit_dht.DHT22(board.D4, use_pulseio=False)

def truncate(my_float, n):
    '''
    truncate floating point to n digits past decimal    
    '''
    new_int = int(my_float*(10**n)) / (10**n) # division returns float by default
    return new_int

def get_temp_data():
    '''
    Pulls data continually from prometheus in intervals defined by 
    collection_interval.
    '''
    # while true allows the unterminated collection of data until closure 
    # of program
    while True:
        try: 
            # thermometer.temperature is a method of adafruit_dht.DHT22 that returns
            # current temperature reading of thermometer in C
            # converted to F because we're american
            temp_F = thermometer.temperature * (9/5) + 32
            # truncate value to 2 values behind decimal
            temp_F = str(truncate(temp_F, 2))
            
            # likewise, thermometer.humidity returns the current humidity reading
            # as a percentage
            hmty = thermometer.humidity
            hmty = str(truncate(hmty, 2))
            
            # FOR DEBUGGING: 
            # print("Temperature: {:10s}  Humidity: {:10s}".format(temp_F, humidity))
            
            # set Guage objects to current value of temperature and humidity 
            temperature.set(temp_F)
            humidity.set(hmty)
        
        # RuntimeError is set to pass because occasional error is thrown from
        # DHT22 thermometer. These errors are to be ignored and the program is to 
        # continue collecting metrics.
        except RuntimeError:
            pass
        
        # raise exeption for any other error
        except Exception as e:
            raise e

        time.sleep(collection_interval)

def main():
    '''
    basic formatting of run structure
    '''
    # start http server for prometheus scrape
    # custom Guage classes automagically accessible to prometheus scrape through
    # socket localhost:9111
    start_http_server(9111)
    # begin collection of metrics
    get_temp_data()

# The below insures that this file only runs when explicitly called to run
# and not when imported to another file.
if __name__ == '__main__':
    main()

