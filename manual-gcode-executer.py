import serial
import time
import sys
import threading
 
PORT = '/dev/ttyUSB0'
BAUD = 250000
 
ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)
ser.flushInput()
 
abort_flag = threading.Event()
 
 
def shutdown():
    """Send program shutdown by triggering Arduino reset."""
    try:
        ser.dtr = False
        time.sleep(0.1)
        ser.dtr = True
        time.sleep(0.1)
        ser.dtr = False
    finally:
        ser.close()
        sys.exit(0)
 
 
def send_gcode(command):
    """Send a single G-code command and wait for 'ok' response."""
    command = command.strip()
    if not command or command.startswith(';'):
        return  # Skip empty lines and comments
 
    ser.write((command + '\n').encode())
    ser.flush()
    print(f"  >> {command}")
 
    # Wait for 'ok' back from printer
    while True:
        if abort_flag.is_set():
            shutdown()
        line = ser.readline().decode(errors='ignore').strip()
        if line:
            print(f"  << {line}")
        if line.lower().startswith('ok'):
            break
        if line.lower().startswith('error'):
            print(f"  [!] Printer reported error: {line}")
            break
 
 
def main():
    print("G-code Executor Ready")
    print("  Type a G-code command and press Enter to send.")
    print("  Press Ctrl+C at any time to shut down.\n")
 
    try:
        while True:
            try:
                cmd = input("gcode> ").strip()
            except EOFError:
                break
 
            if cmd:
                send_gcode(cmd)
 
    except KeyboardInterrupt:
        abort_flag.set()
        shutdown()
 
 
if __name__ == "__main__":
    main()
 

