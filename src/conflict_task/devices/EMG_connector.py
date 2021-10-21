from psychopy.clock import StaticPeriod
from psychopy.parallel import ParallelPort

from conflict_task.util import fatal_exit


class EMGConnector:
    PORT_ADDRESS = 0x378
    _connected = False
    ISI = StaticPeriod()

    @classmethod
    def connect(cls, force=False) -> None:
        try:
            cls.port = ParallelPort(address=cls.PORT_ADDRESS)
            cls._set_data(0)
            cls._connected = True
        except TypeError:
            cls._connected = False

        if cls._read_data() != 0:
            cls._connected = False

        if force and not cls._connected:
            fatal_exit("EMGConnector requested but no ParallelPort connection made")

    @classmethod
    def _read_data(cls):
        if cls._connected:
            return cls.port.readData()
        else:
            return None

    @classmethod
    def _read_pin(cls, pin):
        if cls._connected:
            return cls.port.readPin(pin)
        else:
            return None

    @classmethod
    def _print_all_pins(cls):
        print(f"{cls._read_pin(15):b}x", end="")
        for i in range(13, 1, -1):
            print(f"{cls._read_pin(i):b}", end="")
        print()

    @classmethod
    def _set_data(cls, data):
        if cls._connected:
            cls.port.setData(data)

    @classmethod
    def send_marker(cls, marker, t=0.005, t_after=0.0):
        cls.ISI.start(t)
        cls._set_data(marker)
        cls.ISI.complete()
        if t_after > 0.0:
            cls.ISI.start(t_after)
            cls.ISI.complete()

    @classmethod
    def connected(cls):
        return cls._connected
