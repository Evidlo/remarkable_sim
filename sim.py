import tkinter as tk
from tkinter import ttk

display_scale = 3
screen_width = 1404 // display_scale

def round_rectangle(x1, y1, x2, y2, r=25, **kwargs):
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

        self.f1 = tk.Frame(
            self.root,
            width=1.123 * screen_width,
            height=1.6208 * screen_width,
            background='white'
        ).grid(row=0)
        self.screen = tk.Canvas(
            self.f1,
            width=screen_width,
            height=1.3333 * screen_width,
            background='gray'
        )
        self.screen.place(x=0.0600 * screen_width, y=0.1215 * screen_width)

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
        self.b3.bind('<ButtonPress>', lambda _: self.press(2))
        self.b3.bind('<ButtonRelease>', lambda _: self.release(2))



        self.f2 = tk.Frame(self.root).grid(row=1)

    def press(self, button):
        print(button, 'pressed')

    def release(self, button):
        print(button, 'released')



if __name__ == '__main__':
    root = tk.Tk()
    gui = GUI(root)
    tk.mainloop()
