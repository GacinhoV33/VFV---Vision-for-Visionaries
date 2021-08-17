#!/usr/bin/python
# -*- coding: utf-8 -*-

from tkinter import *
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import numpy as np
from settings import BG_SIZE


if __name__ == "__main__":

    Root = Tk()
    Root.title("Vision For Visionaries")
    Root.geometry(BG_SIZE)  # 800x600

    # main display
    Lwelcome = Label(Root, text="Welcome in VFV - Vision for Visionaries")
    Lwelcome.grid(column=0, row=0, columnspan=3)

    Root.mainloop()


