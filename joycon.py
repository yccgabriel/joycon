from pyjoycon import ButtonEventJoyCon, get_L_id, get_R_id
import asyncio
import threading
from itertools import chain
from pynput.keyboard import Key, Controller
from morse import decode

try:
    joycon_L, joycon_R = ButtonEventJoyCon(*get_L_id()), ButtonEventJoyCon(*get_R_id())
    # joycon_L = ButtonEventJoyCon(*get_L_id())
except ValueError:
    print('check joycon connected? exit.')
    exit(1)

sigint_event = threading.Event()    # https://stackoverflow.com/a/71420261
loop = asyncio.get_event_loop()
queue = asyncio.Queue()
q2 = asyncio.Queue()

def joycon_listener():
    while not sigint_event.is_set():
        for event_type, status in chain(joycon_L.events(), joycon_R.events()):
        # for event_type, status in chain(joycon_L.events()):
            asyncio.run_coroutine_threadsafe(queue.put((event_type, status)), loop)     # https://stackoverflow.com/a/43275001

async def main_loop():
    buf = {'v': [], '^': []}
    while not sigint_event.is_set():
        key, direction = await queue.get()
        if direction == 1:
            buf['v'].append(key)
        elif direction == 0:
            buf['v'].remove(key)
            buf['^'].append(key)
        else:
            raise ValueError(f'unexpected direction: {direction}')
        if len(buf['v']) == 0:
            q2.put_nowait(set(buf['^']))
            buf['^'].clear()

async def pain_loop():
    keyboard = Controller()
    buf = ''
    while not sigint_event.is_set():
        keys = await q2.get()
        if keys in [{'l'}, {'r'}]:
            buf += '.'
        if keys in [{'zl'}, {'zr'}]:
            buf += '-'
        if keys == {'l', 'r', 'zl', 'zr'} or keys == {'x'}:
            keyboard.type(decode(buf))
            buf = ''
        if keys == {'a'}:
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            buf = ''
        if keys == {'b'}:
            keyboard.press(Key.backspace)
            keyboard.release(Key.backspace)
            buf = ''

async def main():
    await asyncio.gather(
        asyncio.to_thread(joycon_listener),
        main_loop(),
        pain_loop(),
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

