from pynput.keyboard import Key, Listener
# from getkey
from inputs import get_key
from inputs import devices

class keyboard_recorder:
    def __init__(self):
        print("Created a keyboard recorder...")
        for device in devices:
            print(device)

    def on_press(key):
        print("Pressed key", key , '{0} pressed'.format(
            key))

    def record_keys(self):
        c = 0
        while c < 1000:
            events = get_key()
            for event in events:
                ...
                print(event.ev_type, event.code, event.state)
            c = c + 1
