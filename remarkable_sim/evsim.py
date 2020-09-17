import time
import os
import struct
import stat

def affine_map(x, a0, a1, b0, b1):
    """Map x in range (a0, a1) to (b0, b1)
    Args:
        x (float): input
        a0 (float): input range start
        a1 (float): input range start
        b0 (float): output range start
        b1 (float): output range start

    Returns:
        int: mapped coordinate
    """

    return int(((x - a0) / a1) * b1 + b0)

def makefifo(path):
    """Make a fifo, delete existing fifo

    Args:
        path (str): path to new fifo
    """

    if os.path.exists(path) and stat.S_ISFIFO(os.stat(path).st_mode):
        os.remove(path)

    os.mkfifo(path)

    return os.open(path, os.O_RDWR)


# write evdev events to fifos
def write_evdev(f, e_type, e_code, e_value):
    """Write evdev events to fifo

    Args:
        f (int): fd of fifo
        e_type (int): evdev event type
        e_code (int): evdev event code
        e_value (int): evdev event value
    """

    print(f, e_type, e_code, e_value)

    t = time.time_ns()
    t_seconds = int(t / 1e9)
    t_microseconds = int(t / 1e3 % 1e6)
    os.write(
        f,
        struct.pack(
            '2IHHi',
            t_seconds,
            t_microseconds,
            e_type,
            e_code,
            e_value
        )
    )

# ----- evdev codes -----
# see evdev_notes.md

# tuples containing (type, code)

code_sync = (0, 0, 0)

codes_stylus = {
    'toolpen': (1, 320),
    'toolrubber': (1, 321),
    'touch': (1, 330),
    'stylus': (1, 331),
    'stylus2': (1, 332),
    'abs_x': (3, 0),
    'abs_y': (3, 1),
    'abs_pressure': (3, 24),
    'abs_distance': (3, 25),
    'abs_tilt_x': (3, 26),
    'abs_tilt_y': (3, 27)
}

codes_touch = {
    'abs_mt_distance': (3, 25),
    'abs_mt_slot': (3, 47),
    'abs_mt_touch_major': (3, 48),
    'abs_mt_touch_minor': (3, 49),
    'abs_mt_orientation': (3, 52),
    'abs_mt_position_x': (3, 53),
    'abs_mt_position_y': (3, 54),
    'abs_mt_tracking_id': (3, 57),
    'abs_mt_pressure': (3, 58)
}

codes_button = {
    'home': (1, 102),
    'left': (1, 105),
    'right': (1, 106),
    'power': (1, 116),
    'wakeup': (1, 143)
}

stylus_max_x = 20967
stylus_max_y = 15725
touch_max_x = 767
touch_max_y = 1023
