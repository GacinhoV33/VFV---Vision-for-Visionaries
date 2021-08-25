#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import numpy as np
from settings import BG_SIZE, X_size, Y_size, AppX_size, AppY_size, AppBG_SIZE
# from func_app import App
import cv2

PATH_C = "C:/Users/gacek/Desktop/Projekty IT/Python/VFV---Vision-for-Visionaries/"
Origin_image = r"images/No_img.png"

Img_CV = None
Img_name = None
Current_Img = None
Type_of_Image = None


def exit_total():
    Root.destroy()


def save_file():
    global Img_name, Type_of_Image
    save_counter = 1

    if os.path.exists("workspace/ActualImg.png"):
        Img_to_safe = cv2.imread("workspace/ActualImg.png")
        path_to_save = "C:/Users/gacek/Desktop/Projekty IT/Python/VFV---Vision-for-Visionaries/save/" + Img_name + "." + Type_of_Image
        if os.path.exists(path_to_save):
            while os.path.exists(path_to_save):
                path_to_save = "C:/Users/gacek/Desktop/Projekty IT/Python/VFV---Vision-for-Visionaries/save/" + Img_name + "({})".format(
                    save_counter) + "." + Type_of_Image
                save_counter += 1
            cv2.imwrite(path_to_save, Img_to_safe)

        else:
            cv2.imwrite(
                "C:/Users/gacek/Desktop/Projekty IT/Python/VFV---Vision-for-Visionaries/save/" + Img_name + "." + Type_of_Image,
                Img_to_safe)

        messagebox.showinfo("Save info", "You've saved your image successfully!")
    else:
        messagebox.showerror("Error")


# TODO decide whether we want act on paths or imgase - at first it look quicker and smarter to act on images
def MakeGray():
    global No_img, Origin_image, Img_name, Img_CV
    print("I'm in!")
    img = cv2.imread(PATH_C + Origin_image)  # TODO complications with path
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    Img_CV = np.array(img).astype(np.uint8)
    # print(Img_CV)
    cv2.imwrite(PATH_C + "workspace/ActualImg.png", Img_CV)
    No_img = ImageTk.PhotoImage(
        (Image.open(Origin_image)).resize((int(AppX_size / 2 + AppX_size / 4), int(AppY_size / 2))), Image.ANTIALIAS)
    Img_name += "+(gray)"


def get_data_binarization():
    inv = BooleanVar()
    thresh1 = 0
    thresh2 = 255
    root_bin = Toplevel()
    root_bin.title("Binarization input")
    root_bin.geometry("{}x{}".format(int(X_size/3.5), int(Y_size/2)))
    Thresh1Label = Label(root_bin, text="Thresh down:", padx=10, pady=10)
    Thresh1Label.place(x=int(X_size/600), y=0)
    Thresh1Entry = Entry(root_bin, width=int(X_size/50), bg="white", fg="red", borderwidth=5)
    Thresh1Entry.place(x=int(X_size/8), y=5)
    Thresh1Entry.insert(1, str(132))

    Thresh2Label = Label(root_bin, text="Thresh up:", padx=10, pady=10)
    Thresh2Label.place(x=int(X_size / 600), y=(Y_size/10) - 5)
    Thresh2Entry = Entry(root_bin, width=int(X_size / 50), bg="white", fg="red", borderwidth=5)
    Thresh2Entry.place(x=int(X_size / 8), y=int(Y_size/10))
    Thresh2Entry.insert(1, str(242))

    CheckInv = Checkbutton(root_bin, text="INV Binarization", variable=inv, onvalue=True, offvalue=False)
    CheckInv.deselect()
    CheckInv.place(x=int(X_size/100), y=int(Y_size/6))
    EnterButton = Button(root_bin, text="Enter", pady=5, padx=30, command=lambda: Binarization(inv.get(), thresh1, thresh2))
    EnterButton.place(x=int(X_size/10), y=int(Y_size/2 - Y_size/11))

    root_bin.mainloop()


def Binarization(inv, thresh1, thresh2):
    global root_bin, No_img, Origin_image, Img_name, Img_CV

    if inv:
        bin_inv = cv2.THRESH_BINARY_INV
    else:
        bin_inv = cv2.THRESH_BINARY
    print(inv)
    up_board = 255
    Img_CV = cv2.threshold(Img_CV, thresh1, up_board, bin_inv)[1]
    #TODO convert format
    print(Img_CV, type(Img_CV))
    Img_CV = np.array(Img_CV).astype(np.uint8)

    if os.path.exists(PATH_C + "workspace/ActualImg.png"):
        os.remove(PATH_C + "workspace/ActualImg.png")
    cv2.imwrite(PATH_C + "workspace/ActualImg.png", Img_CV)
    No_img = ImageTk.PhotoImage(
        (Image.open(Origin_image)).resize((int(AppX_size / 2 + AppX_size / 4), int(AppY_size / 2))), Image.ANTIALIAS)
    Img_name += "+(bin)"


def show_histogram():

    pass

def show_color_histogram():
    pass


def show_image():
    ImageWindow = Toplevel()
    ImageWindow.title(Img_name + "  Type: ")

    ImageAct = ImageTk.PhotoImage(Image.open(Origin_image))
    CreatedImageLabel = Label(ImageWindow, image=ImageAct)
    CreatedImageLabel.pack()

    ImageWindow.mainloop()


def App_func():
    App = Toplevel()
    # App.update()
    App.tk.call('wm', 'iconphoto', App._w, logo_img)
    App.geometry(AppBG_SIZE)

    app_background_img = ImageTk.PhotoImage(
        (Image.open("images/app_background.jpg")).resize((AppX_size, AppY_size), Image.ANTIALIAS))

    AppL = Label(App, image=app_background_img)
    AppL.place(x=0, y=0)

    No_img = ImageTk.PhotoImage(
        (Image.open(Origin_image)).resize((int(AppX_size / 2 + AppX_size / 4), int(AppY_size / 2))), Image.ANTIALIAS)
    WorkingArea = Label(App, image=No_img)
    WorkingArea.place(x=AppX_size / 8, y=AppY_size / 75)

    OpenFileButton = Button(App, text="Load file", padx=AppX_size / 50, pady=AppY_size / 150,
                            command=lambda: open_file(App))
    OpenFileButton.place(x=AppX_size - AppX_size / 9.7, y=AppY_size / 75)

    if Origin_image == r"images/No_img.png":
        SaveFileButton = Button(App, text="Save file", padx=AppX_size / 50, pady=AppY_size / 150, state='disabled')
        SaveFileButton.place(x=AppX_size - AppX_size / 9.7, y=AppY_size / 75 * 10)
    else:
        SaveFileButton = Button(App, text="Save file", padx=AppX_size / 50, pady=AppY_size / 150, command=save_file)
        SaveFileButton.place(x=AppX_size - AppX_size / 9.7, y=AppY_size / 75 * 10)

    if Origin_image == r"images/No_img.png":
        ShowImageButton = Button(App, text="Show Image", padx=AppX_size / 100, pady=AppY_size / 150, state="disabled")
        ShowImageButton.place(x=AppX_size - AppX_size / 9.7, y=AppY_size / 75 * 20)
    else:
        ShowImageButton = Button(App, text="Show Image", padx=AppX_size / 100, pady=AppY_size / 150,
                                 command=show_image)
        ShowImageButton.place(x=AppX_size - AppX_size / 9.7, y=AppY_size / 75 * 20)

    if Origin_image == r"images/No_img.png":
        MakeGrayButton = Button(App, text="Make Gray", padx=AppX_size / 100, pady=AppY_size / 150,
                                state="disabled")
        MakeGrayButton.place(x=AppX_size / 8, y=AppY_size / 1.9)
    else:
        MakeGrayButton = Button(App, text="Make Gray", padx=AppX_size / 100, pady=AppY_size / 150,
                                command=MakeGray)
        MakeGrayButton.place(x=AppX_size / 8, y=AppY_size / 1.9)

    if Origin_image == r"images/No_img.png":
        BinarizationButton = Button(App, text="Binarization", padx=AppX_size / 100, pady=AppY_size / 150,
                                    state="disabled")
        BinarizationButton.place(x=AppX_size / 8, y=AppY_size / 1.74)
    else:
        BinarizationButton = Button(App, text="Binarization", padx=AppX_size / 100, pady=AppY_size / 150,
                                    command=get_data_binarization)
        BinarizationButton.place(x=AppX_size / 8, y=AppY_size / 1.74)

    if Origin_image == r"images/No_img.png":
        ShowHistogramButton = Button(App, text="Histogram", padx=AppX_size / 100, pady=AppY_size / 150,
                                    state="disabled")
        ShowHistogramButton.place(x=AppX_size / 8, y=AppY_size / 1.6)
    else:
        ShowHistogramButton = Button(App, text="Histogram", padx=AppX_size / 100, pady=AppY_size / 150,
                                    command=show_histogram)
        ShowHistogramButton.place(x=AppX_size / 8, y=AppY_size / 1.6)

    if Origin_image == r"images/No_img.png":
        ShowHistogramColorButton = Button(App, text="Color Histogram", padx=AppX_size / 100, pady=AppY_size / 150,
                                     state="disabled")
        ShowHistogramColorButton.place(x=AppX_size / 8, y=AppY_size / 1.6)
    else:
        ShowHistogramColorButton = Button(App, text="Color Histogram", padx=AppX_size / 100, pady=AppY_size / 150,
                                     command=show_histogram)
        ShowHistogramColorButton.place(x=AppX_size / 8, y=AppY_size / 1.6)  #TODO check whether possible or not


    App.mainloop()


def open_file(App):
    global Origin_image, No_img, Img_name, Type_of_Image, Img_CV
    filename = filedialog.askopenfilename(initialdir="/", title="Select a file",
                                          filetypes=(("png files", "*.png"), ("jpg files", "*.jpg")))
    print(filename)
    if filename == "":
        Origin_image = "images/No_img.png"

    else:
        Origin_image = filename
        help_var = 0
        help_var2 = 0
        for num, letter in enumerate(Origin_image, 1):
            if letter == "/":
                help_var = num
            if letter == ".":
                help_var2 = num

        Img_name = Origin_image[help_var:help_var2]
        Type_of_Image = Origin_image[help_var2:]
        print(Img_name + Type_of_Image)
        if os.path.exists("workspace/ActualImg.png"):
            os.remove("workspace/ActualImg.png")

        img_act = cv2.imread(filename)
        Img_CV = np.array(img_act).astype(np.uint8)
        print(Img_CV)
        cv2.imwrite(PATH_C + "workspace/ActualImg.png", Img_CV)

        Origin_image = "workspace/ActualImg.png"
        App.destroy()
        App_func()


if __name__ == "__main__":
    Root = Tk()
    Root.title("Vision For Visionaries")
    Root.geometry(BG_SIZE)  # 800x600
    Root.wm_attributes('-transparentcolor', '#ab23ff')
    logo_img = PhotoImage(file='images/logo.png')
    Root.tk.call('wm', 'iconphoto', Root._w, logo_img)

    # main

    intro_img = ImageTk.PhotoImage(Image.open("images/intro.png"))

    # Creating a canvas

    mainCanv = Canvas(Root, width=X_size, height=Y_size)
    mainCanv.pack(fill="both", expand=True)

    # set img in canvas
    mainCanv.create_image(0, 0, image=intro_img, anchor="nw")

    # Adding a label - in canvas it looks different

    mainCanv.create_text(X_size / 2, int(Y_size / 1.5), text="VFV - Vision for Visionaries", font=("Helvetica", 30),
                         fill="white")
    mainCanv.create_text(X_size / 2, Y_size / 8, text="Welcome!", font=("Helvetica", 50), fill="white")

    # adding button to canvas
    startButt = Button(Root, text="Start", padx=80, pady=10, command=App_func)
    startButt_window = mainCanv.create_window(X_size / 2 - 80, Y_size - Y_size / 11, anchor="nw", window=startButt)

    exitButt = Button(Root, text="Exit", padx=80, pady=10, command=exit_total)
    exitButt_window = mainCanv.create_window(X_size - 200, Y_size - Y_size / 11, anchor="nw", window=exitButt)

    optionButt = Button(Root, text="Options", padx=80, pady=10)
    optionButt_window = mainCanv.create_window(10, Y_size - Y_size / 11, anchor="nw", window=optionButt)

    # basic_img = No_img

    '''
    Lintro = Label(Root, image=intro_img)
    Lintro.place(x=0, y=0, relwidth=1, relheight=1)

    LWelcome = Label(Root, text="Welcome in VFV - Vision for Visionaries", font=("Helvetica", 25), fg="white").pack(pady=50)

    # Lwelcome = Button(Root, text="Welcome in VFV - Vision for Visionaries", image=intro_img, relief="flat", state="disabled")
    # Lwelcome.image = intro_img
    # Lwelcome.place(x=0, y=0)
    '''
    Root.mainloop()
