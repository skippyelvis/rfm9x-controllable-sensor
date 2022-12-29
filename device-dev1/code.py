from rfm9x import RFM9X
import gc
import time

class Device(RFM9X):

    def __init__(self, **kw):
        super().__init__(
            led=True, node=1, destination=2, name="sensor"
        )
        self.radio.receive_timeout = 3
        self.send("STARTUP:sensor")

    def read_sensor(self):
        val = time.monotonic()
        return val

    def parse(self, packet):
        cmd = packet["payload"]
        name, val = cmd.split(":")
        if name == "DSLEEP":
            return name, int(val)
        return None, None

    def handle(self, command, val):
        if command == "DSLEEP":
            self.radio.sleep()
            time.sleep(val)

    def poll(self):
        interval = 3
        now = time.monotonic()
        while True:
            packet = self.receive()
            if packet is not None:
                command, val = self.parse(packet)
                print(command, val)
                self.handle(command, val)
            if time.monotonic() - now > interval:
                now = time.monotonic()
                val = self.read_sensor()
                msg = f"TIME:{val}"
                print(msg)
                self.send(msg)
            print("===")

if __name__ == "__main__":
    dev = Device()
    dev.poll()
