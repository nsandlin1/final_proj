from prometheus_client.core import REGISTRY as reg
import time
from prometheus_client import start_http_server, Gauge

class CustomCollector(object):
    def __init__(self):
        pass

    def collect(self):
        g = Gauge('my_inprogress_requests', 'Description')
        i = 1
        while True:
            g.set(i)
            i += 1
            yield g
            time.sleep(1)

if __name__ == '__main__':
    start_http_server(8000)
    reg.register(CustomCollector())
    while True:
        time.sleep(1)
