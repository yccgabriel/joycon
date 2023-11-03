from pyjoycon import ButtonEventJoyCon, get_L_id, get_R_id
import asyncio
import threading
from itertools import chain
from pynput.keyboard import Key, Controller
from morse import decode
import time
from collections import OrderedDict

class AsyncButtonEvent(ButtonEventJoyCon):
    """I don't like how to library handle events.
    need to use busy waiting to poll for events.
    it's draining battery life."""

    def joycon_button_event(self, button, state):
        asyncio.run_coroutine_threadsafe(
            queue.put((button, state)),
            loop
        )

try:
    joycon_L, joycon_R = AsyncButtonEvent(*get_L_id()), AsyncButtonEvent(*get_R_id())
except ValueError:
    print('check joycon connected? exit.')
    exit(1)

sigint_event = threading.Event()    # https://stackoverflow.com/a/71420261  # no use anymore.
loop = asyncio.get_event_loop()
queue = asyncio.Queue()
q2 = asyncio.Queue()

async def main_loop():
    buf = {'v': OrderedDict(), '^': OrderedDict()}
    A = 20000000  # in nano seconds
    B = 0.8     # overlap percentage
    while True:
        key, direction = await queue.get()
        if direction == 1:
            buf['v'][key] = time.perf_counter_ns()
            continue
        elif direction == 0:
            buf['^'][key] = {'vt': buf['v'][key], '^t': time.perf_counter_ns()}
            del buf['v'][key]
        else:
            raise ValueError(f'unexpected direction: {direction}')

        if len(buf['v'].keys()) == 0 and len(buf['^'].keys()) == 1:     # I'm the only one
            q2.put_nowait({key})
            del buf['^'][key]
            continue

        if len(buf['v'].keys()) == 1:   # wait for more
            continue

        if len(buf['v'].keys()) == 0 and len(buf['^'].keys()) == 2:
            # print(buf['^'])
            keyups = enumerate(buf['^'].items())
            _1, (k1, tt1) = next(keyups)
            _2, (k2, tt2) = next(keyups)
            # print(k1, k2)
            def is_overlap(tt1, tt2):
                d1 = tt1['^t'] - tt1['vt']
                d2 = tt2['^t'] - tt2['vt']
                return min(d1,d2) / max(d1,d2) >= B
            if abs(tt1['vt'] - tt2['vt']) > A:    # greater than threashold.  consider them not combo.
                # print('A', tt1['vt'] - tt2['vt'])
                q2.put_nowait({k1})
                del buf['^'][k1]
                q2.put_nowait({k2})
                del buf['^'][k2]
                continue
            elif not is_overlap(tt1, tt2):
                q2.put_nowait({k1})
                del buf['^'][k1]
                q2.put_nowait({k2})
                del buf['^'][k2]
                continue
            else:   # is overlap
                q2.put_nowait({k1,k2})
                del buf['^'][k1]
                del buf['^'][k2]
                continue

        print('not handled')
        buf = ''

async def pain_loop():
    keyboard = Controller()
    buf = ''
    while True:
        keys = await q2.get()
        # print(keys)
        if keys in [{'l'}, {'r'}]:
            buf += '.'
        if keys in [{'zl'}, {'zr'}]:
            buf += '-'
        if keys == {'l', 'r'} or keys == {'x'}:
            if buf == '':
                keyboard.press(Key.space)
                keyboard.release(Key.space)
            else:
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

