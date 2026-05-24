from pynput import keyboard
 
STEP = 10
pos = {'x': 0, 'y': 0, 'z': 0}

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
 
def main():
    print("Listening for arrow keys. Press ESC to quit.")
    with keyboard.Listener(on_press=on_press, on_release=on_release, suppress=True) as listener:
        while listener.running:
            print(f"x: {pos['x']} y: {pos['y']} z: {pos['z']}")

    print("Exited.")
 
if __name__ == "__main__":
    main()

