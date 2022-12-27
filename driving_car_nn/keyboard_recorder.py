from pynput.keyboard import Key, Listener
# from getkey

class keyboard_recorder:
    def __init__(self):
        print("Created a keyboard recorder...")

    def on_press(key):
        print("Pressed key", key , '{0} pressed'.format(
            key))