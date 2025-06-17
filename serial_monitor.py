import argparse
import threading
import queue
from plot import TimeSeriesPlot as tsp
import connection

def error(msg):
    print(f"\x1b[1;97;101mError: {msg}\x1b[0m")

def serial_reader(conn, num_channels, data_queue, stop_event):
    while not stop_event.is_set():
        if conn.serial_connection and conn.serial_connection.in_waiting:
            try:
                raw_bytes = conn.serial_connection.readline()
                try:
                    raw = raw_bytes.decode(errors='replace').strip()
                except Exception:
                    continue  # Skip this line if decoding fails
                values = [float(v) for v in raw.split(',')]
                if any(v > 4100 for v in values):
                    continue
                if len(values) == num_channels:
                    data_queue.put(values)
            except Exception:
                continue

def main():
    parser = argparse.ArgumentParser(description="Real-time Serial Data Plotter")
    parser.add_argument('--port', '-P', type=str, default='/dev/ttyUSB0', help='Serial port')
    parser.add_argument('--baudrate', '-B', type=int, default=115200, help='Baud rate')
    parser.add_argument('--timeout', '-TO', type=float, default=1.0, help='Timeout (seconds, float)')
    parser.add_argument('--channels', '-C', type=int, default=1, help='Number of channels (int)')
    args = parser.parse_args()

    if args.channels < 1:
        error("Number of channels must be at least 1.")
        return
    if args.timeout <= 0:
        error("Timeout must be a positive number.")
        return
    if args.baudrate <= 0:
        error("Baud rate must be a positive integer.")
        return
    if not args.port:
        error("Port must be specified.")
        return

    c = connection.Connection(port=args.port, baudrate=args.baudrate, timeout=args.timeout)
    c.connect()

    data_queue = queue.Queue()
    stop_event = threading.Event()
    reader_thread = threading.Thread(target=serial_reader, args=(c, args.channels, data_queue, stop_event))
    reader_thread.daemon = True
    reader_thread.start()

    plotter = tsp(data_queue, num_channels=args.channels, max_points=10000, y_label='ADC Value (DMA Averaging)')
    try:
        plotter.run()
    finally:
        stop_event.set()
        reader_thread.join()
        c.disconnect()

if __name__ == "__main__":
    main()