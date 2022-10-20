from dataclasses import dataclass
from ntpath import join

import os
import random
import sys
import time
from time import sleep


@dataclass
class Orb:
    x: int
    y: int
    dx: int
    dy: int


if os.name == 'nt':
    import msvcrt
    import ctypes

    class _CursorInfo(ctypes.Structure):
        _fields_ = [("size", ctypes.c_int),
                    ("visible", ctypes.c_byte)]


def hide_cursor():
    if os.name == 'nt':
        ci = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = False
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
    elif os.name == 'posix':
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()


def clear_term():
    if os.name == 'nt':
        os.system('cls')
    elif os.name == 'posix':
        os.system('clear')


def main():
    if len(sys.argv) > 1:
        rim = sys.argv[1]

    clear_term()
    hide_cursor()

    random.seed(time.time())
    orb_count = 10
    fps = 60
    radius = 100
    rim = 2
    inner_radius = radius * (1 + 0.25 * rim)

    term_x, term_y = os.get_terminal_size()
    term_y *= 2
    speed = 1 / fps
    radius = 100 / (term_x * term_y)


    orbs = [Orb(x=random.randint(0, term_x),
                y=random.randint(0, term_y),
                dx=-1 if random.randint(0, term_x) % 2 == 0 else 1,
                dy=-1 if random.randint(0, term_y) % 2 == 0 else 1,
                ) for i in range(orb_count)]

    while True:
        screen = [[' ' for i in range(term_x)] for i in range(int(term_y/2))]
        #  move orbs
        for orb in orbs:
            if orb.x + orb.dx >= term_x or orb.x + orb.dx < 0:
                orb.dx *= -1

            if orb.y + orb.dy >= term_y or orb.y + orb.dy < 0:
                orb.dy *= -1

            orb.x += orb.dx
            orb.y += orb.dy
        # print(f'{orbs[0]=}')

        # render
        for x_index in range(term_x):
            for y_index in range(int(term_y / 2)):
                # calculate the two halfs of the block at the same time
                sum = [0.0, 0.0]

                for j2 in range(2):
                    for orb in orbs:
                        y = y_index * 2 + j2
                        try:
                            sum[j2] += 1.0 / ((x_index - orb.x) * (x_index - orb.x) + (y - orb.y) * (y - orb.y))
                        except ZeroDivisionError:
                            sum[j2] += 1
                if sum[0] > radius:
                    if sum[1] > radius:
                        screen[y_index][x_index] = "█"
                    else:
                        screen[y_index][x_index] = "▀"
                else:
                    if sum[1] > radius:
                        screen[y_index][x_index] = "▄"

                if rim:
                    if sum[0] > inner_radius:
                        if sum[1] > inner_radius:
                            screen[y_index][x_index] = "█"
                        else:
                            screen[y_index][x_index] = "▄"
                    else:
                        if sum[1] > inner_radius:
                            screen[y_index][x_index] = "▀"
        sc = ''.join(''.join([''.join(line) for line in screen]))
        sys.stdout.write(sc)
        sleep(speed)
        sys.stdout.flush()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        ...
    clear_term()
