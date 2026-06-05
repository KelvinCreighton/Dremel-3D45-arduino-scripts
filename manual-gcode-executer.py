import serial
import time
import sys
import threading
 
PORT = '/dev/ttyUSB0'
BAUD = 250000
 
ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)
 
abort_flag = threading.Event()
 
 
def emergency_abort():
    """Send emergency stop and kill the program immediately."""
    print("\n!!! EMERGENCY ABORT !!!")
    try:
        ser.write(b"M112\n")       # Emergency stop — halts all motion immediately
        ser.flush()
        ser.write(b"M84\n")        # Disable all steppers
        ser.flush()
    except Exception:
        pass
    finally:
        ser.close()
        sys.exit(1)
 
 
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
            emergency_abort()
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
    print("  Type 'exit' or 'quit' to close normally.")
    print("  Press Ctrl+C at any time for EMERGENCY ABORT.\n")
 
    try:
        while True:
            try:
                cmd = input("gcode> ").strip()
            except EOFError:
                break
 
            if cmd.lower() in ('exit', 'quit'):
                print("Closing connection.")
                ser.close()
                sys.exit(0)
 
            if cmd:
                send_gcode(cmd)
 
    except KeyboardInterrupt:
        abort_flag.set()
        emergency_abort()
 
 
if __name__ == "__main__":
    main()

