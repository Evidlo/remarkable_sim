import tkinter as tk
from tkinter import ttk

display_scale = 3
screen_width = 1404 // display_scale

# def round_rectangle(x1, y1, x2, y2, r=25, **kwargs):
#     points = (
#         x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2,
#         y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r,
#         y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1
#     )
#     return canvas.create_polygon(points, **kwargs, smooth=True)

class GUI(object):
    def __init__(self, root):
        self.root = root
        root.title("reMarkable simulator")

        # ----- Screen Area -----

        self.f1 = tk.Frame(
            self.root,
            width=1.123 * screen_width,
            height=1.6208 * screen_width,
            background='white'
        )
        self.f1.grid(row=0, column=0)
        self.screen = tk.Canvas(
            self.f1,
            width=screen_width,
            height=1.3333 * screen_width,
            background='gray'
        )
        self.screen.place(x=0.0600 * screen_width, y=0.1215 * screen_width)
        self.screen.bind('<ButtonPress-1>', self.screenclick)
        self.screen.bind('<B1-Motion>', self.screendrag)

        self.b1 = tk.Button(
            self.f1,
            relief='groove',
            width=int(0.0805 * screen_width),
            height=int(0.0805 * screen_width)
        )
        self.b1.place(x=0.0644 * screen_width, y=1.4919 * screen_width)
        self.b1.configure(width=2, height=2)
        self.b1.bind('<ButtonPress>', lambda _: self.press(1))
        self.b1.bind('<ButtonRelease>', lambda _: self.release(1))
        self.b2 = tk.Button(
            self.f1,
            relief='groove',
            width=int(0.0805 * screen_width),
            height=int(0.0805 * screen_width)
        )
        self.b2.place(x=0.5142 * screen_width, y=1.4919 * screen_width)
        self.b2.configure(width=2, height=2)
        self.b2.bind('<ButtonPress>', lambda _: self.press(2))
        self.b2.bind('<ButtonRelease>', lambda _: self.release(2))
        self.b3 = tk.Button(
            self.f1,
            relief='groove',
            width=int(0.0805 * screen_width),
            height=int(0.0805 * screen_width)
        )
        self.b3.place(x=0.9640 * screen_width, y=1.4919 * screen_width)
        self.b3.configure(width=2, height=2)
        self.b3.bind('<ButtonPress>', lambda _: self.press(3))
        self.b3.bind('<ButtonRelease>', lambda _: self.release(3))

        # ----- Config Area -----

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

        self.check1 = tk.IntVar()
        self.check2 = tk.IntVar()
        self.check3 = tk.IntVar()
        tk.Checkbutton(self.f2, variable=self.check1, text='Button 1').grid(row=0, column=4)
        tk.Checkbutton(self.f2, variable=self.check2, text='Button 2').grid(row=0, column=5)
        tk.Checkbutton(self.f2, variable=self.check3, text='Button 3').grid(row=0, column=6)

        self.hold = tk.Button(self.f2, text='Multi Press')
        self.hold.grid(row=1, column=4)
        self.hold.bind('<ButtonPress>', self.multipress)
        self.hold.bind('<ButtonRelease>', self.multirelease)

    def multipress(self, _):
        print(self.check1, self.check2, self.check3)
        if self.check1.get():
            self.press(1)
        if self.check2.get():
            self.press(2)
        if self.check3.get():
            self.press(3)

    def multirelease(self, _):
        if self.check1.get():
            self.release(1)
        if self.check2.get():
            self.release(2)
        if self.check3.get():
            self.release(3)

    def press(self, button):
        print(button, 'pressed')

    def release(self, button):
        print(button, 'released')

    def screenclick(self, event):
        print(
            event.x * display_scale,
            event.y * display_scale,
            'click'
        )

    def screendrag(self, event):
        print(
            event.x * display_scale,
            event.y * display_scale,
            'drag'
        )


if __name__ == '__main__':
    root = tk.Tk()
    gui = GUI(root)
    tk.mainloop()
