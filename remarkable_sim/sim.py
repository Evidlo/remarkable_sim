# Evan Widloski - 2020-09-13

import argparse
import logging
import os
import stat
import tkinter as tk
from tkinter import ttk
from remarkable_sim.evsim import (
    makefifo, write_evdev, codes_stylus, codes_touch, codes_button, code_sync,
    stylus_max_x, stylus_max_y, touch_max_x, touch_max_y, affine_map
)

logging.basicConfig(format='%(message)s')
log = logging.getLogger(__name__)

display_scale = 3
screen_width = 1404 // display_scale
screen_height = 4 * screen_width // 3

# fake evdev interface
path_fifo_stylus = 'event0'
path_fifo_touch = 'event1'
path_fifo_button = 'event2'
# screen buffer
path_fb = 'fb.pgm'

# period between reading framebuffer
screen_update_delay = 100 # (ms)


def round_rectangle(canvas, x1, y1, x2, y2, r=25, **kwargs):
    points = (
        x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2,
        y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r,
        y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1
    )
    return canvas.create_polygon(points, **kwargs, smooth=True)

class GUI(object):
    def __init__(self, root):
        self.root = root
        root.title("reMarkable simulator")

        # ----- Screen Area -----

        self.f1 = tk.Frame(
            self.root,
            width=1.3 * screen_width,
            height=1.7 * screen_width,
            background='white'
        )
        self.f1.grid(row=0, column=0)
        self.tablet = tk.Canvas(
            self.f1,
            width=1.1278 * screen_width,
            height=1.6256 * screen_width,
            background='white',
            highlightthickness=0,
            bd=0
        )
        # center tablet canvas in frame
        # TODO: use .pack() instead of manual positioning
        self.tablet.place(
            # TODO: tkinter bug, canvas['width'] is a string?
            x=(self.f1['width'] - int(self.tablet['width'])) / 2,
            y=(self.f1['height'] - int(self.tablet['height'])) / 2,
        )
        round_rectangle(
            self.tablet,
            0, 0,
            1.1278 * screen_width - 1, 1.6256 * screen_width - 1,
            r=30,
            fill='gray98',
            outline='gray80'
        )
        round_rectangle(
            self.tablet,
            0.0132 * screen_width, 0.0132 * screen_width,
            1.1146 * screen_width, 1.6124 * screen_width,
            r=15,
            fill='gray90'
        )
        self.screen = tk.Canvas(
            self.tablet,
            width=screen_width,
            height=screen_height,
            background='gray90'
        )
        self.screen.place(x=0.0600 * screen_width, y=0.1215 * screen_width)
        self.screen.bind('<ButtonPress-1>', self.screen_press)
        self.screen.bind('<B1-Motion>', self.screen_motion)
        self.screen.bind('<ButtonRelease-1>', self.screen_release)

        # Buttons

        self.b1 = tk.Button(
            self.tablet,
            relief='groove',
            width=int(0.0805 * screen_width),
            height=int(0.0805 * screen_width),
            background='gray95'
        )
        self.b1.place(x=0.0644 * screen_width, y=1.4919 * screen_width)
        self.b1.configure(width=2, height=2)
        self.b1.bind('<ButtonPress>', lambda _: self.press('left'))
        self.b1.bind('<ButtonRelease>', lambda _: self.release('left'))
        self.b2 = tk.Button(
            self.tablet,
            relief='groove',
            width=int(0.0805 * screen_width),
            height=int(0.0805 * screen_width),
            background='gray95'
        )
        self.b2.place(x=0.5142 * screen_width, y=1.4919 * screen_width)
        self.b2.configure(width=2, height=2)
        self.b2.bind('<ButtonPress>', lambda _: self.press('home'))
        self.b2.bind('<ButtonRelease>', lambda _: self.release('home'))
        self.b3 = tk.Button(
            self.tablet,
            relief='groove',
            width=int(0.0805 * screen_width),
            height=int(0.0805 * screen_width),
            background='gray95'
        )
        self.b3.place(x=0.9640 * screen_width, y=1.4919 * screen_width)
        self.b3.configure(width=2, height=2)
        self.b3.bind('<ButtonPress>', lambda _: self.press('right'))
        self.b3.bind('<ButtonRelease>', lambda _: self.release('right'))
        self.bpow = tk.Button(
            self.tablet,
            relief='groove',
            width=int(0.0805 * screen_width),
            height=int(0.0805 * screen_width),
            background='gray95'
        )
        self.bpow.place(x=0.5142 * screen_width, y=0.0300 * screen_width)
        self.bpow.configure(width=2, height=1)
        self.bpow.bind('<ButtonPress>', lambda _: self.press('power'))
        self.bpow.bind('<ButtonRelease>', lambda _: self.release('power'))

        # ----- Settings Area -----

        self.f2 = tk.Frame(self.root)
        self.f2.grid(row=0, column=1)

        self.input = tk.StringVar()
        self.input.set('Stylus')
        tk.Label(self.f2, text='Input Method').grid(row=0, column=0)
        tk.OptionMenu(self.f2, self.input, 'Stylus', 'Touch').grid(row=0, column=1)

        tk.Label(self.f2, text='Stylus Pressure').grid(row=1, column=0)
        self.pressure = tk.Scale(self.f2, from_=0, to=4095, orient='horizontal')
        self.pressure.grid(row=1, column=1)
        tk.Label(self.f2, text='Stylus Tilt X').grid(row=2, column=0)
        self.tiltx = tk.Scale(self.f2, from_=-6300, to=6300, orient='horizontal')
        self.tiltx.grid(row=2, column=1)
        tk.Label(self.f2, text='Stylus Tilt Y').grid(row=3, column=0)
        self.tilty = tk.Scale(self.f2, from_=-6300, to=6300, orient='horizontal')
        self.tilty.grid(row=3, column=1)

        ttk.Separator(self.f2, orient='vertical').grid(row=0, column=2, rowspan=3, sticky='ns')

        # Checkboxes

        # make colums 4, 5, 6 equal width for checkboxes
        self.f2.grid_columnconfigure(4, uniform='check')
        self.f2.grid_columnconfigure(5, uniform='check')
        self.f2.grid_columnconfigure(6, uniform='check')

        self.check1 = tk.IntVar()
        self.check2 = tk.IntVar()
        self.check3 = tk.IntVar()
        self.checkpow = tk.IntVar()
        self.c1 = tk.Checkbutton(self.f2, variable=self.checkpow, text='Button 1')
        self.c1.grid(row=0, column=4, sticky='w')
        self.c2 = tk.Checkbutton(self.f2, variable=self.check2, text='Button 2')
        self.c2.grid(row=0, column=5, sticky='w')
        self.c3 = tk.Checkbutton(self.f2, variable=self.check3, text='Button 3')
        self.c3.grid(row=0, column=6, sticky='w')
        self.cpow = tk.Checkbutton(self.f2, variable=self.checkpow, text='Power')
        self.cpow.grid(row=1, column=4, sticky='w')

        self.hold = tk.Button(self.f2, text='Multi Press')
        self.hold.grid(row=2, column=5)
        self.hold.bind('<ButtonPress>', self.multi_press)
        self.hold.bind('<ButtonRelease>', self.multi_release)

        self.root.after(screen_update_delay, self.load_screen)

        # ----- FIFOs -----

        self.fifo_stylus = makefifo(path_fifo_stylus)
        self.fifo_touch = makefifo(path_fifo_touch)
        self.fifo_button = makefifo(path_fifo_button)

    def load_screen(self):
        # FIXME: file is sometimes read before writing is finished
        if os.path.exists(path_fb):
            img = tk.PhotoImage(file=path_fb)
            self.img_scaled = img.subsample(display_scale, display_scale)
            self.screen.create_image(0, 0, image=self.img_scaled, anchor='nw')
            self.root.after(screen_update_delay, self.load_screen)

    # ----- Event Callbacks -----

    # handle multi button press
    def multi_press(self, _):
        if self.check1.get():
            self.press('left')
        if self.check2.get():
            self.press('home')
        if self.check3.get():
            self.press('right')
        if self.checkpow.get():
            self.press('power')

    # handle multi button release
    def multi_release(self, _):
        if self.check1.get():
            self.release('left')
        if self.check2.get():
            self.release('home')
        if self.check3.get():
            self.release('right')
        if self.checkpow.get():
            self.release('power')

    # handle single button press
    def press(self, button):
        write_evdev(self.fifo_button, *codes_button[button], 1)
        write_evdev(self.fifo_button, *code_sync)

    # handle single button release
    def release(self, button):
        write_evdev(self.fifo_button, *codes_button[button], 0)
        write_evdev(self.fifo_button, *code_sync)

    # screen initial press
    def screen_press(self, event):
        if self.input == 'Stylus':
            write_evdev(self.fifo_stylus, *codes_stylus['abs_distance'], 0)

        if self.input == 'Touch':
            pass

        self.screen_motion(event)

    # screen motion after press
    def screen_motion(self, event):
        if self.input.get() == 'Stylus':
            write_evdev(self.fifo_stylus, *codes_stylus['abs_pressure'], self.pressure.get())
            write_evdev(self.fifo_stylus, *codes_stylus['abs_tilt_x'], self.tiltx.get())
            write_evdev(self.fifo_stylus, *codes_stylus['abs_tilt_y'], self.tilty.get())
            write_evdev(
                self.fifo_stylus,
                *codes_stylus['abs_y'],
                affine_map(event.x, 0, screen_width, 0, stylus_max_y)
            )
            write_evdev(
                self.fifo_stylus,
                *codes_stylus['abs_x'],
                affine_map(event.y, 0, screen_width, stylus_max_x, 0)
            )
            write_evdev(self.fifo_stylus, *code_sync)

        if self.input.get() == 'Touch':
            pass

    # screen release
    def screen_release(self, event):
        if self.input == 'Stylus':
            write_evdev(self.fifo_stylus, *codes_stylus['abs_distance'], 100)
            write_evdev(self.fifo_stylus, *code_sync)

        if self.input == 'Touch':
            pass


def main():
    root = tk.Tk()
    gui = GUI(root)

    try:
        tk.mainloop()
    except KeyboardInterrupt:
        pass

    os.remove(path_fifo_stylus)
    os.remove(path_fifo_touch)
    os.remove(path_fifo_button)


if __name__ == '__main__':
    main()
