from pyjoycon import ButtonEventJoyCon, get_L_id, get_R_id
import asyncio
import threading
from itertools import chain
from pynput.keyboard import Key, Controller
from morse import decode

try:
    joycon_L, joycon_R = ButtonEventJoyCon(*get_L_id()), ButtonEventJoyCon(*get_R_id())
except ValueError:
    print('check joycon connected? exit.')
    exit(1)

sigint_event = threading.Event()    # https://stackoverflow.com/a/71420261
loop = asyncio.get_event_loop()
queue = asyncio.Queue()

def joycon_listener():
    while not sigint_event.is_set():
        for event_type, status in chain(joycon_L.events(), joycon_R.events()):
            asyncio.run_coroutine_threadsafe(queue.put((event_type, status)), loop)     # https://stackoverflow.com/a/43275001

async def main_loop():
    keyboard = Controller()
    buf = ''
    while not sigint_event.is_set():
        key_event = await queue.get()
        if key_event in [('r',1), ('l',1)]:
            buf += '.'
        if key_event in [('zr',1), ('zl', 1)]:
            buf += '-'
        if key_event in [('x',1)]:
            keyboard.type(decode(buf))
            buf = ''
        if key_event in [('a',1)]:
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            buf = ''
        if key_event in [('b',1)]:
            keyboard.press(Key.backspace)
            keyboard.release(Key.backspace)
            buf = ''

async def main():
    await asyncio.gather(
        asyncio.to_thread(joycon_listener),
        main_loop(),
    )

async def cleanup():
    sigint_event.set()

if __name__ == '__main__':
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        loop.run_until_complete(cleanup())
    finally:
        print('gracefully halt.')

