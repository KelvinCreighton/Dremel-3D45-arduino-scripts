from pynput import keyboard
import serial
import time
 
PORT = '/dev/ttyUSB0'
BAUD = 250000
STEP = 1
FEEDRATE = 3000
TICK = 0.02

pos = {'x': 0, 'y': 0, 'z': 0}

ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)

def on_press(key):
    if key == keyboard.Key.up:
        pos['y'] = STEP
    elif key == keyboard.Key.down:
        pos['y'] = -STEP

    if key == keyboard.Key.left:
        pos['x'] = -STEP
    elif key == keyboard.Key.right:
        pos['x'] = STEP

    if key == keyboard.Key.page_up:
        pos['z'] = STEP
    elif key == keyboard.Key.page_down:
        pos['z'] = -STEP

    if key == keyboard.Key.esc:
        return False
 
def on_release(key):
    if key == keyboard.Key.up and pos['y'] > 0:
        pos['y'] = 0
    if key == keyboard.Key.down and pos['y'] < 0:
        pos['y'] = 0

    if key == keyboard.Key.left and pos['x'] < 0:
        pos['x'] = 0
    if key == keyboard.Key.right and pos['x'] > 0:
        pos['x'] = 0

    if key == keyboard.Key.page_up and pos['z'] > 0:
        pos['z'] = 0
    if key == keyboard.Key.page_down and pos['z'] < 0:
        pos['z'] = 0

    if key == keyboard.Key.esc:
        return False

def send(cmd):
    ser.write(f"{cmd}\n".encode())

def setup():
    send("G91") # set absolute mode

def teardown():
    send("G90") # restore absolute mode
    send("M84") # release steppers
    ser.close()

def main():
    setup()

    print("Listening for arrow keys. Press ESC to quit.")
    with keyboard.Listener(on_press=on_press, on_release=on_release, suppress=True) as listener:
        while listener.running:
            x, y, z = pos['x'], pos['y'], pos['z']
            if x != 0 or y != 0 or z != 0:
                print(f"x: {x} y: {y} z: {z}")
                cmd = f"G1"
                if x != 0: cmd += f" X{x}"
                if y != 0: cmd += f" Y{y}"
                if z != 0: cmd += f" Z{z}"
                cmd += f" F{FEEDRATE}"
                send(cmd)
            time.sleep(TICK)

    teardown()
    print("Exited.")
 
if __name__ == "__main__":
    main()

