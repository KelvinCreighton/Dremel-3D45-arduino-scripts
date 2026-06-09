import serial
import time
 
PORT = '/dev/ttyUSB0'
BAUD = 250000
 
BED_X = 220
BED_Y = 220
MARGIN = 20
TRAVEL_Z = 10
PROBE_SPEED = 500
TRAVEL_SPEED = 3000
 
SERVO_DEPLOY = 95
SERVO_STOW = 65
SERVO_PIN = 11
PROBE_PIN = 18
 
POINTS = [
    (MARGIN,         MARGIN),
    (BED_X - MARGIN, MARGIN),
    (BED_X - MARGIN, BED_Y - MARGIN),
    (MARGIN,         BED_Y - MARGIN),
]
 
ser = serial.Serial(PORT, BAUD, timeout=5)
time.sleep(2)
 
def send(cmd):
    ser.write(f"{cmd}\n".encode())
    time.sleep(0.05)
 
def wait_ok():
    while True:
        line = ser.readline().decode(errors='ignore').strip()
        if line == 'ok':
            return
 
def deploy():
    send(f"M280 P0 S{SERVO_DEPLOY}")
    time.sleep(0.5)
 
def stow():
    send(f"M280 P0 S{SERVO_STOW}")
    time.sleep(0.5)
 
def probe_point(x, y):
    send(f"G1 X{x} Y{y} F{TRAVEL_SPEED}")
    wait_ok()
    send(f"G1 Z2 F{PROBE_SPEED}")
    wait_ok()
    send("G30")
    while True:
        line = ser.readline().decode(errors='ignore').strip()
        if line.startswith("Bed X:") or line.startswith("Z:"):
            parts = line.split()
            for i, p in enumerate(parts):
                if p in ("Z:", "Z") and i + 1 < len(parts):
                    return float(parts[i + 1])
        if line == 'ok':
            break
    return None
 
def home():
    send("G28")
    while True:
        line = ser.readline().decode(errors='ignore').strip()
        if line == 'ok':
            break
 
def main():
    print("Homing...")
    home()
 
    send(f"G1 Z{TRAVEL_Z} F{TRAVEL_SPEED}")
    wait_ok()
 
    deploy()
    print("Probe deployed. Starting calibration...\n")
 
    results = []
    labels = ["Front-left", "Front-right", "Back-right", "Back-left"]
 
    for (x, y), label in zip(POINTS, labels):
        print(f"Probing {label} ({x}, {y})...")
        z = probe_point(x, y)
        results.append((label, x, y, z))
        send(f"G1 Z{TRAVEL_Z} F{TRAVEL_SPEED}")
        wait_ok()
 
    stow()
    print("Probe stowed.\n")
 
    send("G28 XY")
    wait_ok()
    ser.close()
 
    ref = results[0][3]
    print("=== Z Calibration Results ===")
    for label, x, y, z in results:
        offset = round(z - ref, 3) if z is not None else "ERR"
        print(f"  {label:15} ({x:3}, {y:3})  Z={z}  offset={offset}")
    print(f"\nReference point: {results[0][0]} at Z={ref}")
    print("Adjust bed screws so all offsets are as close to 0 as possible.")
 
if __name__ == "__main__":
    main()

