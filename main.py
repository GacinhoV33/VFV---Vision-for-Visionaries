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


Origin_image = r"images/No_img.png"
Img_name = None
Current_Img = None
Type_of_Image = None


def exit_total():
    Root.destroy()


def save_file():
    global Img_name, Type_of_Image
    save_counter = 1

    if os.path.exists("workspace/ActualImg.jpg"):
        Img_to_safe = cv2.imread("workspace/ActualImg.jpg")
        path_to_save = "C:/Users/gacek/Desktop/Projekty IT/Python/VFV---Vision-for-Visionaries/save/" + Img_name + "." + Type_of_Image
        if os.path.exists(path_to_save):
            while os.path.exists(path_to_save):
                path_to_save = "C:/Users/gacek/Desktop/Projekty IT/Python/VFV---Vision-for-Visionaries/save/" + Img_name + "({})".format(save_counter) + "." + Type_of_Image
                save_counter += 1
            cv2.imwrite(path_to_save, Img_to_safe)

        else:
            cv2.imwrite("C:/Users/gacek/Desktop/Projekty IT/Python/VFV---Vision-for-Visionaries/save/" + Img_name + "." + Type_of_Image, Img_to_safe)

        messagebox.showinfo("Save info", "You've saved your image successfully!")
    else:
        messagebox.showerror("Error")



# TODO decide whether we want act on paths or imgase - at first it look quicker and smarter to act on images
def MakeGray(path: str):
    global No_img, Origin_image, Img_name

    if os.path.exists("workspace/ActualImg.jpg"):
        os.remove("workspace/ActualImg.jpg")
    img = cv2.imread(path) #TODO complications with path
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imwrite("workspace/ActualImg.jpg", img)
    Origin_image = "workspace/ActualImg.jpg"
    No_img = ImageTk.PhotoImage((Image.open(Origin_image)).resize((int(AppX_size/2 + AppX_size/4), int(AppY_size/2))), Image.ANTIALIAS)
    Img_name += "+(gray)"


def Binarization(path: str):
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
    App.tk.call('wm', 'iconphoto', App._w, logo_img)
    App.geometry(AppBG_SIZE)

    app_background_img = ImageTk.PhotoImage(
        (Image.open("images/app_background.jpg")).resize((AppX_size, AppY_size), Image.ANTIALIAS))

    AppL = Label(App, image=app_background_img)
    AppL.place(x=0, y=0)

    No_img = ImageTk.PhotoImage((Image.open(Origin_image)).resize((int(AppX_size/2 + AppX_size/4), int(AppY_size/2))), Image.ANTIALIAS)
    WorkingArea = Label(App, image=No_img)
    WorkingArea.place(x=AppX_size/8, y=AppY_size/75)

    OpenFileButton = Button(App, text="Load file", padx=AppX_size/50, pady=AppY_size/150, command=lambda: open_file(App))
    OpenFileButton.place(x=AppX_size - AppX_size/9.7, y=AppY_size/75)

    if Origin_image == r"images/No_img.png":
        SaveFileButton = Button(App, text="Save file", padx=AppX_size/50, pady=AppY_size/150, state='disabled')
        SaveFileButton.place(x=AppX_size - AppX_size/9.7, y=AppY_size/75 * 10)
    else:
        SaveFileButton = Button(App, text="Save file", padx=AppX_size / 50, pady=AppY_size / 150, command=save_file)
        SaveFileButton.place(x=AppX_size - AppX_size / 9.7, y=AppY_size / 75 * 10)

    if Origin_image == r"images/No_img.png":
        ShowImageButton = Button(App, text="Show Image", padx=AppX_size/100, pady=AppY_size/150, state="disabled")
        ShowImageButton.place(x=AppX_size - AppX_size/9.7, y=AppY_size/75 * 20)
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
                                command=lambda: MakeGray(r"{}".format(Origin_image)))
        MakeGrayButton.place(x=AppX_size / 8, y=AppY_size / 1.9)

    if Origin_image == r"images/No_img.png":
        BinarizationButton = Button(App, text="Make Gray", padx=AppX_size / 100, pady=AppY_size / 150,
                                state="disabled")
        BinarizationButton.place(x=AppX_size / 8, y=AppY_size / 1.9)
    else:
        BinarizationButton = Button(App, text="Make Gray", padx=AppX_size / 100, pady=AppY_size / 150,
                                command=lambda: Binarization(r"{}".format(Origin_image)))
        BinarizationButton.place(x=AppX_size / 8, y=AppY_size / 1.9)






    App.mainloop()


def open_file(App):
    global Origin_image, No_img, Img_name, Type_of_Image
    filename = filedialog.askopenfilename(initialdir="/", title="Select a file",
                                              filetypes=(("png files", "*.png"), ("jpg files", "*.jpg")))

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
        App.destroy()
        App_func()


if __name__ == "__main__":

    Root = Tk()
    Root.title("Vision For Visionaries")
    Root.geometry(BG_SIZE)  # 800x600
    Root.wm_attributes('-transparentcolor', '#ab23ff')
    logo_img = PhotoImage(file='images/logo.png')
    Root.tk.call('wm', 'iconphoto', Root._w, logo_img)

    #main

    intro_img = ImageTk.PhotoImage(Image.open("images/intro.png"))

    #Creating a canvas

    mainCanv = Canvas(Root, width=X_size, height=Y_size)
    mainCanv.pack(fill="both", expand=True)

    # set img in canvas
    mainCanv.create_image(0, 0, image=intro_img, anchor="nw")

    #Adding a label - in canvas it looks different

    mainCanv.create_text(X_size/2, int(Y_size/1.5), text="VFV - Vision for Visionaries", font=("Helvetica", 30), fill="white")
    mainCanv.create_text(X_size/2, Y_size/8, text="Welcome!", font=("Helvetica", 50), fill="white")

    #adding button to canvas
    startButt = Button(Root, text="Start", padx=80, pady=10, command=App_func)
    startButt_window = mainCanv.create_window(X_size/2 - 80, Y_size - Y_size/11, anchor="nw", window=startButt)

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


