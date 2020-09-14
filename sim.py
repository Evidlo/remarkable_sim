# Evan Widloski - 2020-09-13

import argparse
import logging
import os
import stat
import tkinter as tk
from tkinter import ttk

logging.basicConfig(format='%(message)s')
log = logging.getLogger(__name__)

display_scale = 3
screen_width = 1404 // display_scale

def makefifo(fifo):
    if os.path.exists(fifo) and stat.S_ISFIFO(os.stat(fifo).st_mode):
        os.remove(fifo)

    os.mkfifo(fifo)

# fake evdev interface
fifo_input = makefifo('event0')
fifo_button = makefifo('event1')

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
            r=40,
            fill='gray98',
            outline='gray80'
        )
        round_rectangle(
            self.tablet,
            0.0132 * screen_width, 0.0132 * screen_width,
            1.1146 * screen_width, 1.6124 * screen_width,
            r=20,
            fill='gray90'
        )
        self.screen = tk.Canvas(
            self.tablet,
            width=screen_width,
            height=1.3333 * screen_width,
            background='gray90'
        )
        self.screen.place(x=0.0600 * screen_width, y=0.1215 * screen_width)
        self.screen.bind('<ButtonPress-1>', self.screen_click)
        self.screen.bind('<B1-Motion>', self.screen_drag)

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
        self.b1.bind('<ButtonPress>', lambda _: self.press(1))
        self.b1.bind('<ButtonRelease>', lambda _: self.release(1))
        self.b2 = tk.Button(
            self.tablet,
            relief='groove',
            width=int(0.0805 * screen_width),
            height=int(0.0805 * screen_width),
            background='gray95'
        )
        self.b2.place(x=0.5142 * screen_width, y=1.4919 * screen_width)
        self.b2.configure(width=2, height=2)
        self.b2.bind('<ButtonPress>', lambda _: self.press(2))
        self.b2.bind('<ButtonRelease>', lambda _: self.release(2))
        self.b3 = tk.Button(
            self.tablet,
            relief='groove',
            width=int(0.0805 * screen_width),
            height=int(0.0805 * screen_width),
            background='gray95'
        )
        self.b3.place(x=0.9640 * screen_width, y=1.4919 * screen_width)
        self.b3.configure(width=2, height=2)
        self.b3.bind('<ButtonPress>', lambda _: self.press(3))
        self.b3.bind('<ButtonRelease>', lambda _: self.release(3))
        self.bpow = tk.Button(
            self.tablet,
            relief='groove',
            width=int(0.0805 * screen_width),
            height=int(0.0805 * screen_width),
            background='gray95'
        )
        self.bpow.place(x=0.5142 * screen_width, y=0.0300 * screen_width)
        self.bpow.configure(width=2, height=1)
        self.bpow.bind('<ButtonPress>', lambda _: self.press('pow'))
        self.bpow.bind('<ButtonRelease>', lambda _: self.release('pow'))

        # ----- Settings Area -----

        self.f2 = tk.Frame(self.root)
        self.f2.grid(row=1, column=0)

        self.input = tk.StringVar()
        self.input.set('Stylus')
        tk.Label(self.f2, text='Input Method').grid(row=0, column=0)
        tk.OptionMenu(self.f2, self.input, 'Stylus', 'Touch').grid(row=0, column=1)

        tk.Label(self.f2, text='Pressure').grid(row=1, column=0)
        self.pressure = tk.Scale(self.f2, from_=0, to=100, orient='horizontal')
        self.pressure.grid(row=1, column=1)
        tk.Label(self.f2, text='Angle').grid(row=2, column=0)
        self.angle = tk.Scale(self.f2, from_=0, to=100, orient='horizontal')
        self.angle.grid(row=2, column=1)

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
        tk.Checkbutton(self.f2, variable=self.checkpow, text='Button 1').grid(row=0, column=4, sticky='w')
        tk.Checkbutton(self.f2, variable=self.check2, text='Button 2').grid(row=0, column=5, sticky='w')
        tk.Checkbutton(self.f2, variable=self.check3, text='Button 3').grid(row=0, column=6, sticky='w')
        tk.Checkbutton(self.f2, variable=self.check1, text='Power').grid(row=1, column=4, sticky='w')

        self.hold = tk.Button(self.f2, text='Multi Press')
        self.hold.grid(row=2, column=5)
        self.hold.bind('<ButtonPress>', self.multi_press)
        self.hold.bind('<ButtonRelease>', self.multi_release)

        self.root.after(screen_update_delay, self.load_screen)

    def load_screen(self):
        # FIXME: file is sometimes read before writing is finished
        img = tk.PhotoImage(file='fb.pgm')
        self.img_scaled = img.subsample(display_scale, display_scale)
        self.screen.create_image(0, 0, image=self.img_scaled, anchor='nw')
        self.root.after(screen_update_delay, self.load_screen)

    # event callbacks

    def multi_press(self, _):
        if self.check1.get():
            self.press(1)
        if self.check2.get():
            self.press(2)
        if self.check3.get():
            self.press(3)
        if self.checkpow.get():
            self.press('pow')

    def multi_release(self, _):
        if self.check1.get():
            self.release(1)
        if self.check2.get():
            self.release(2)
        if self.check3.get():
            self.release(3)
        if self.checkpow.get():
            self.release('pow')

    def press(self, button):
        print(button, 'pressed')

    def release(self, button):
        print(button, 'released')

    def screen_click(self, event):
        print(
            event.x * display_scale,
            event.y * display_scale,
            self.pressure.get(),
            self.angle.get(),
            self.input.get(),
            'click'
        )

    def screen_drag(self, event):
        print(
            event.x * display_scale,
            event.y * display_scale,
            self.pressure.get(),
            self.angle.get(),
            self.input.get(),
            'drag'
        )

    def write_evdev(self, f, e_type, e_code, e_value):
        pass


if __name__ == '__main__':
    root = tk.Tk()
    gui = GUI(root)

    try:
        tk.mainloop()
    except KeyboardInterrupt:
        os.remove('event0')
        os.remove('event1')
