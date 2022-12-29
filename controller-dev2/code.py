from rfm9x import RFM9X
import gc
import time

class Controller(RFM9X):
    
    def __init__(self, **kw):
        super().__init__(
            led=False, node=2, destination=1, name="sensor"
        )
        self.send("STARTUP:receiver")
        self.tmpval = None

    def parse(self, packet):
        data = packet["payload"]
        name, val = data.split(":")
        if name == "TIME":
            return name, float(val)
        return None, None

    def handle(self, name, val):
        if self.tmpval is None:
            self.tmpval = val
        elif name == "TIME":
            if val - self.tmpval > 10:
                self.tmpval = None
                self.send("DSLEEP:10")

    def poll(self):
        while True:
            packet = self.receive()
            if packet is None:
                continue
            print(packet)
            name, val = self.parse(packet)
            self.handle(name, val)
            print("===")

if __name__ == "__main__":
    controller = Controller()
    controller.poll()
