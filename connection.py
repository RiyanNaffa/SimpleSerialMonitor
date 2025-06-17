import serial

class Connection:
    def __init__(self, port: str = '/dev/ttyUSB0', baudrate: int = 115200, timeout: float = 1.0):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_connection = None

    def connect(self):
        """Establish a serial connection."""
        try:
            self.serial_connection = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout
            )
            print(
                f"Connected to "
                f"\x1b[4;92;40m{self.port}\x1b[0m "
                f"at "
                f"\x1b[4;92;40m{self.baudrate}\x1b[0m baud rate."
            )
        except serial.SerialException as e:
            print(
                f"\x1b[1;97;41mFailed to connect: {e}\x1b[0m"
            )

    def disconnect(self):
        """Close the serial connection."""
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            print(
                f"\x1b[22;97;103mConnection closed.\x1b[0m"
            )