from pynput import keyboard
 
running = True
 
def on_press(key):
    if key == keyboard.Key.up:
        print("UP pressed")
    elif key == keyboard.Key.down:
        print("DOWN pressed")
    elif key == keyboard.Key.left:
        print("LEFT pressed")
    elif key == keyboard.Key.right:
        print("RIGHT pressed")
    elif key == keyboard.Key.esc:
        return False
    else:
        try:
            print(f"Key pressed: {key.char}")
        except AttributeError:
            print(f"Special key: {key}")
 
def on_release(key):
    if key == keyboard.Key.up:
        print("UP released")
    elif key == keyboard.Key.down:
        print("DOWN released")
    elif key == keyboard.Key.left:
        print("LEFT released")
    elif key == keyboard.Key.right:
        print("RIGHT released")
    elif key == keyboard.Key.esc:
        return False
 
def main():
    print("Listening for arrow keys. Press ESC to quit.")
    with keyboard.Listener(on_press=on_press, on_release=on_release, suppress=True) as listener:
        listener.join()
    print("Exited.")
 
if __name__ == "__main__":
    main()

