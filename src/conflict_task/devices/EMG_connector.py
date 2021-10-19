from psychopy.parallel import ParallelPort

from conflict_task.util import fatal_exit

class EMGConnector:
    PORT_ADDRESS = 0x378

    def __init__(self, force = False) -> None:
        self._connected = True
        try:
            self.port = ParallelPort(address=self.PORT_ADDRESS)
            self.set_data(0)
        except TypeError:
            self._connected = False
        
        if self.read_data() != 0:
            self._connected = False
        
        if force and not self._connected:
            fatal_exit("EMGConnector requested but no ParallelPort connection made")

    def read_data(self):
        if self._connected:
            return self.port.readData()
        else:
            return None
    
    def read_pin(self, pin):
        if self._connected:
            return self.port.readPin(pin)
        else:
            return None
    
    def _print_all_pins(self):
        print(f"{self.read_pin(15):b}x", end="")
        for i in range(13, 1, -1):
            print(f"{self.read_pin(i):b}", end="")
        print()

    def set_data(self, data):
        if self._connected:
            self.port.setData(data)

    def connected(self):
        return self._connected
