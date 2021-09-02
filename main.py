#!/usr/bin/python
# -*- coding: utf-8 -*-

from copy import deepcopy
import os
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import numpy as np
from settings import BG_SIZE, X_size, Y_size, AppX_size, AppY_size, AppBG_SIZE, monitor_height, monitor_width
# from func_app import App
import cv2
import CreateToolTip
from color_hist import color_histogram_equalization


PATH_C = "C:/Users/gacek/Desktop/Projekty IT/Python/VFV---Vision-for-Visionaries/"
Origin_image = r"images/No_img.png"


Img_CV = None
Img_name = None
Current_Img = None
Type_of_Image = None


def exit_total():
    Root.destroy()


def save_file(root):
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

    root.destroy()
    App_func()


def SpaceColor():
    root_space = Toplevel()
    root_space.geometry("{}x{}".format(int(X_size/3), int(Y_size/3)))
    root_space.title("Conversion")

    clicked1 = StringVar()
    clicked1.set("BGR")

    clicked2 = StringVar()
    clicked2.set("RGB")

    dropdown1 = ["BGR", "RGB", "HSV", "LAB", "YCbCr"]
    dropdown2 = ["RGB", "BGR", "HSV", "LAB", "YCbCr"]

    dropmenu = OptionMenu(root_space, clicked1, *dropdown1)
    dropmenu.place(x=int(X_size/30), y=int(Y_size/30))

    ToLabel = Label(root_space, text=" TO ")
    ToLabel.place(x=int(X_size/8.1), y=int(Y_size/24))

    dropmenu2 = OptionMenu(root_space, clicked2, *dropdown2)
    dropmenu2.place(x=int(X_size/6), y=int(Y_size/30))

    ConvertSpaceButton = Button(root_space, text="Convert", pady=5, padx=10, command=lambda: Convert(root_space, str(clicked1.get()), str(clicked2.get())))
    ConvertSpaceButton.place(x=int(X_size/8.1), y=int(Y_size/3.65))

    root_space.mainloop()


def Convert(root, fmt1: str, fmt2: str):
    global Img_CV
    mask = None

    if fmt1 == "RGB" and fmt2 == "BGR":
        mask = cv2.COLOR_RGB2BGR
    elif fmt1 == "RGB" and fmt2 == "HSV":
        mask = cv2.COLOR_RGB2HSV
    elif fmt1 == "RGB" and fmt2 == "LAB":
        mask = cv2.COLOR_RGB2LAB
    elif fmt1 == "RGB" and fmt2 == "YCrCb":
        mask = cv2.COLOR_RGB2YCrCb

    elif fmt1 == "BGR" and fmt2 == "RGB":
        mask = cv2.COLOR_BGR2RGB
    elif fmt1 == "BGR" and fmt2 == "HSV":
        mask = cv2.COLOR_BGR2HSV
    elif fmt1 == "BGR" and fmt2 == "LAB":
        mask = cv2.COLOR_BGR2LAB
    elif fmt1 == "BGR" and fmt2 == "YCrCb":
        mask = cv2.COLOR_BGR2YCrCb

    elif fmt1 == "HSV" and fmt2 == "RGB":
        mask = cv2.COLOR_HSV2RGB
    elif fmt1 == "HSV" and fmt2 == "BGR":
        mask = cv2.COLOR_HSV2BGR
    elif fmt1 == "HSV" and fmt2 == "LAB":
        mask = None # Can't do this
    elif fmt1 == "HSV" and fmt2 == "YCrCb":
        mask = cv2.COLOR_HSV2RGB

    elif fmt1 == "YCrCb" and fmt2 == "RGB":
        mask = cv2.COLOR_YCrCb2RGB
    elif fmt1 == "YCrCb" and fmt2 == "BGR":
        mask = cv2.COLOR_YCrCb2BGR
    # elif fmt1 == "YCrCb" and fmt2 == "HSV":
    #     mask = None # Can't do this
    # elif fmt1 == "YCrCb" and fmt2 == "LAB":
    #     mask = None # Can't do this

    elif fmt1 == "LAB" and fmt2 == "RGB":
        mask = cv2.COLOR_LAB2RGB
    elif fmt1 == "LAB" and fmt2 == "BGR":
        mask = cv2.COLOR_LAB2BGR

    if mask:
        Img_CV = cv2.cvtColor(Img_CV, mask)
    else:
        messagebox.showerror("Error", "Wrong format - conversion impossible.")

    root.destroy()


def MakeGray():
    global No_img, Origin_image, Img_name, Img_CV
    img = cv2.imread(PATH_C + Origin_image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    Img_CV = np.array(img).astype(np.uint8)
    cv2.imwrite(PATH_C + "workspace/ActualImg.png", Img_CV)
    No_img = ImageTk.PhotoImage(
        (Image.open(Origin_image)).resize((int(AppX_size / 2 + AppX_size / 4), int(AppY_size / 2))), Image.ANTIALIAS)
    Img_name += "+(gray)"


def get_data_binarization():
    global Img_CV
    inv = BooleanVar()

    root_bin = Toplevel()
    auto_thr = auto_thresh(Img_CV)
    root_bin.title("Binarization input")
    root_bin.geometry("{}x{}".format(int(X_size/3.5), int(Y_size/2)))
    Thresh1Label = Label(root_bin, text="Thresh down:", padx=10, pady=10)
    Thresh1Label.place(x=int(X_size/600), y=0)
    Thresh1Entry = Entry(root_bin, width=int(X_size/50), bg="white", fg="red", borderwidth=5)
    Thresh1Entry.place(x=int(X_size/8), y=5)
    Thresh1Entry.insert(1, str(auto_thr))

    Thresh2Label = Label(root_bin, text="Thresh up:", padx=10, pady=10)
    Thresh2Label.place(x=int(X_size / 600), y=(Y_size/10) - 5)
    Thresh2Entry = Entry(root_bin, width=int(X_size / 50), bg="white", fg="red", borderwidth=5)
    Thresh2Entry.place(x=int(X_size / 8), y=int(Y_size/10))
    Thresh2Entry.insert(1, str(255))

    CheckInv = Checkbutton(root_bin, text="INV Binarization", variable=inv, onvalue=True, offvalue=False)
    CheckInv.deselect()
    CheckInv.place(x=int(X_size/100), y=int(Y_size/6))
    EnterButton = Button(root_bin, text="Enter", pady=5, padx=30, command=lambda: Binarization(inv.get(), int(Thresh1Entry.get()), int(Thresh2Entry.get()), root_bin))
    EnterButton.place(x=int(X_size/10), y=int(Y_size/2 - Y_size/11))

    root_bin.mainloop()


def auto_thresh(image):
    img = np.array(image).astype(np.int8)
    img_hist = np.squeeze(cv2.calcHist([image], [0], None, [256], [0, 256]))
    hist_sum = img_hist.sum()
    k0 = int(hist_sum/img.shape[0]/image.shape[1])
    thr = 1
    while True:
        m0 = img[img <= k0].mean()
        m1 = img[img > k0].mean()
        k_new = (m0+m1)/2
        if abs(k0 - k_new) < thr:
            k_new = round(k_new)
            break
        else:
            k0 = k_new
    return abs(k_new)


def Binarization(inv, thresh1, thresh2, root_bin):
    global  No_img, Origin_image, Img_name, Img_CV

    if inv:
        for i in range(Img_CV.shape[0]):
            for j in range(Img_CV.shape[1]):
                if thresh1 <= Img_CV[i][j] <= thresh2:
                    Img_CV[i][j] = 0
                else:
                    Img_CV[i][j] = 255
    else:
        for i in range(Img_CV.shape[0]):
            for j in range(Img_CV.shape[1]):
                if thresh1 <= Img_CV[i][j] <= thresh2:
                    Img_CV[i][j] = 255
                else:
                    Img_CV[i][j] = 0

    if os.path.exists(PATH_C + "workspace/ActualImg.png"):
        os.remove(PATH_C + "workspace/ActualImg.png")
    cv2.imwrite(PATH_C + "workspace/ActualImg.png", Img_CV)

    No_img = ImageTk.PhotoImage(
        (Image.open(Origin_image)).resize((int(AppX_size / 2 + AppX_size / 4), int(AppY_size / 2))), Image.ANTIALIAS)
    Img_name += "+(bin)"
    root_bin.destroy()


def show_histogram():
    global Img_CV

    hist_img = cv2.calcHist([Img_CV], [0], None, [256], [0, 256])
    hist_figure = plt.figure(figsize=(6, 5), dpi=100)
    ax = hist_figure.add_subplot(111)

    hist_root = Toplevel()
    chart_type = FigureCanvasTkAgg(hist_figure, hist_root)
    chart_type.get_tk_widget().pack()

    ax.grid()
    ax.plot(hist_img)
    ax.set_title("Histogram of " + str(Img_name))
    hist_root.title(Img_name + " Histogram")
    hist_root.geometry("{}x{}".format(int(X_size/1.1), int(Y_size/1.6)))
    hist_root.mainloop()


def show_color_histogram():
    global Img_CV
    img = deepcopy(Img_CV)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    colors = ['r', 'g', 'b']


    img_eq, hist_eq = color_histogram_equalization(img)


    root_color_hist = Toplevel()
    root_color_hist.geometry("{}x{}".format(int(X_size / 0.7), int(Y_size / 0.8)))
    compare_figure, ((ax1IMG, ax1HIST), (ax2IMG, ax2HIST)) = plt.subplots(2, 2)
    compare_figure.set_size_inches([12, 8])
    compare_figure.suptitle("Comparison")

    chart_type = FigureCanvasTkAgg(compare_figure, root_color_hist)
    chart_type.get_tk_widget().place(x=0, y=0)

    ax1IMG.imshow(img)
    ax1IMG.set_title("Original Image")


    for i in range(3):
        img_h = cv2.calcHist([img], [i], None, [256], [0, 256])
        plt.plot(img_h, colors[i], label=colors[i])
        ax1HIST.plot(img_h, colors[i], label=colors[i].upper())
    ax1HIST.set_title("Original Histogram")
    ax1HIST.legend(colors)

    ax2IMG.imshow(img_eq)
    ax2IMG.set_title("Color image after equalizing")


    for i in range(3):
        img_he = cv2.calcHist([img_eq], [i], None, [256], [0, 256])
        ax2HIST.plot(img_he, colors[i], label=colors[i].upper())
    ax2HIST.set_title("Color histogram after equalizing")
    ax2HIST.legend(colors)

    SaveButton = Button(root_color_hist, text="Save", command=lambda: save_img(root_color_hist, img_eq, "ColorHistEq    "),
                        padx=10, pady=5)
    SaveButton.place(x=int(X_size / 0.78), y=int(Y_size / 60))

    DontSaveButton = Button(root_color_hist, text="Don't save", command=root_color_hist.destroy, padx=10, pady=5)
    DontSaveButton.place(x=int(X_size / 0.78), y=int(Y_size / 13))

    root_color_hist.mainloop()


def equal_histogram():
    global Img_CV

    img = deepcopy(Img_CV)
    hist_org = cv2.calcHist([img], [0], None, [256], [0, 256])
    img_eq = cv2.equalizeHist(img)
    hist_eq = cv2.calcHist([img_eq], [0], None, [256], [0, 256])
    root_equal = Toplevel()
    compare_figure, ((ax1IMG, ax1HIST), (ax2IMG, ax2HIST)) = plt.subplots(2, 2)
    compare_figure.set_size_inches([12, 8])
    compare_figure.suptitle("Comparison")

    chart_type = FigureCanvasTkAgg(compare_figure, root_equal)
    chart_type.get_tk_widget().place(x=0, y=0)

    ax1IMG.imshow(img)
    ax1IMG.set_title("Original Image")

    ax1HIST.plot(hist_org)
    ax1HIST.set_title("Original Histogram")

    ax2IMG.imshow(img_eq)
    ax2IMG.set_title("Image after histogram equalizing")

    ax2HIST.plot(hist_eq)
    ax2HIST.set_title("Histogram after equalizing")


    root_equal.geometry("{}x{}".format(int(X_size/0.7), int(Y_size/0.8)))
    root_equal.title(Img_name + " Histogram Equalizing")

    SaveButton = Button(root_equal, text="Save", command=lambda: save_img(root_equal, img_eq, "EqHist"), padx=10,
                        pady=5)
    SaveButton.place(x=int(X_size / 0.78), y=int(Y_size / 60))

    DontSaveButton = Button(root_equal, text="Don't save", command=root_equal.destroy, padx=10, pady=5)
    DontSaveButton.place(x=int(X_size / 0.78), y=int(Y_size / 13))
    root_equal.mainloop()


def save_img(root, img_after, operation):
    global Img_CV, Img_name
    Img_CV = img_after
    Img_name += str("({})").format(operation)
    if os.path.exists(PATH_C + "workspace/ActualImg.png"):
        os.remove(PATH_C + "workspace/ActualImg.png")
    cv2.imwrite(PATH_C + "workspace/ActualImg.png", Img_CV)

    root.destroy()


def normalize_histogram():
    global Img_CV
    img_org = deepcopy(Img_CV)
    img_hist = cv2.calcHist([img_org], [0], None, [256], [0, 256])
    img_after = cv2.normalize(img_org, np.zeros(Img_CV.shape[0]), alpha=0, beta=256, norm_type=cv2.NORM_MINMAX)
    hist_after = cv2.calcHist([img_after], [0], None, [256], [0, 256])

    root_normalize = Toplevel()
    compare_figure, ((ax1IMG, ax1HIST), (ax2IMG, ax2HIST)) = plt.subplots(2, 2)
    compare_figure.set_size_inches([12, 8])
    compare_figure.suptitle("Comparison")

    chart_type = FigureCanvasTkAgg(compare_figure, root_normalize)
    chart_type.get_tk_widget().place(x=0, y=0)

    ax1IMG.imshow(img_org)
    ax1IMG.set_title("Original Image")

    ax1HIST.plot(img_hist)
    ax1HIST.set_title("Original Histogram")

    ax2IMG.imshow(img_after)
    ax2IMG.set_title("Image after histogram normalizing")

    ax2HIST.plot(hist_after)
    ax2HIST.set_title("Histogram after normalizing")

    root_normalize.title(Img_name + " normalized histogram")
    root_normalize.geometry("{}x{}".format(int(X_size/0.7), int(Y_size/0.8)))

    SaveButton = Button(root_normalize, text="Save", command=lambda: save_img(root_normalize, img_after, "HistNorm"), padx=10, pady=5)
    SaveButton.place(x=int(X_size/0.78), y=int(Y_size/60))

    DontSaveButton = Button(root_normalize, text="Don't save", command=root_normalize.destroy, padx=10, pady=5)
    DontSaveButton.place(x=int(X_size/0.78), y=int(Y_size/13))
    root_normalize.mainloop()


def CLAHE_get_data():

    root_clahe = Toplevel()
    root_clahe.title("Getting Clahe information")
    root_clahe.geometry("{}x{}".format(int(X_size/3.5), int(Y_size/2)))

    ClipLimitLabel = Label(root_clahe, text="ClipLimit: ", padx=10, pady=10)
    ClipLimitLabel.place(x=int(X_size / 600), y=0)
    ClipLimitEntry = Entry(root_clahe, width=int(X_size / 50), bg="white", fg="red", borderwidth=5)
    ClipLimitEntry.place(x=int(X_size / 8), y=5)
    ClipLimitEntry.insert(1, 20.0)

    TileGridSizeLabel = Label(root_clahe, text="TileGridSize: ", padx=10, pady=10)
    TileGridSizeLabel.place(x=int(X_size / 600), y=(Y_size / 10) - 5)
    TileGridSizeEntry = Entry(root_clahe, width=int(X_size / 50), bg="white", fg="red", borderwidth=5)
    TileGridSizeEntry.place(x=int(X_size / 8), y=int(Y_size / 10))
    TileGridSizeEntry.insert(1, 10)
    # TileGridSizeLabelHelp = Label(root_clahe, text="This parameter describe size of square (grid) matrix")
    CreateToolTip.CreateToolTip(TileGridSizeLabel, text="This parameter describe size of square (grid) matrix")


    # # CheckInv = Checkbutton(root_clahe, text="INV Binarization", variable=inv, onvalue=True, offvalue=False)
    # CheckInv.deselect()
    # CheckInv.place(x=int(X_size / 100), y=int(Y_size / 6))

    EnterButton = Button(root_clahe, text="Enter", pady=5, padx=30,
                         command=lambda: CLAHE(root_clahe, int(TileGridSizeEntry.get()), float(ClipLimitEntry.get())))
    EnterButton.place(x=int(X_size / 10), y=int(Y_size / 2 - Y_size / 11))

    root_clahe.mainloop()


def CLAHE(root, tilegridsize: int, cliplimit: float):
    root.destroy()

    global Img_CV
    img = deepcopy(Img_CV)
    img_hist = cv2.calcHist([img], [0], None, [256], [0, 256])
    clahe_user = cv2.createCLAHE(clipLimit=cliplimit, tileGridSize=(tilegridsize, tilegridsize))
    img_clahe = clahe_user.apply(img)
    clahe_hist = cv2.calcHist([img_clahe], [0], None, [256], [0, 256])

    root_clahe = Toplevel()
    compare_figure, ((ax1IMG, ax1HIST), (ax2IMG, ax2HIST)) = plt.subplots(2, 2)
    compare_figure.set_size_inches([12, 8])
    compare_figure.suptitle("Comparison")

    chart_type = FigureCanvasTkAgg(compare_figure, root_clahe)
    chart_type.get_tk_widget().place(x=0, y=0)

    ax1IMG.imshow(img)
    ax1IMG.set_title("Original Image")

    ax1HIST.plot(img_hist)
    ax1HIST.set_title("Original Histogram")

    ax2IMG.imshow(img_clahe)
    ax2IMG.set_title("Image after CLAHE operation")

    ax2HIST.plot(clahe_hist)
    ax2HIST.set_title("Histogram after CLAHE operation")

    root_clahe.title(Img_name + " CLAHE")
    root_clahe.geometry("{}x{}".format(int(X_size / 0.7), int(Y_size / 0.8)))

    SaveButton = Button(root_clahe, text="Save", command=lambda: save_img(root_clahe, img_clahe, "CLAHE"),
                        padx=10, pady=5)
    SaveButton.place(x=int(X_size / 0.78), y=int(Y_size / 60))

    DontSaveButton = Button(root_clahe, text="Don't save", command=root_clahe.destroy, padx=10, pady=5)
    DontSaveButton.place(x=int(X_size / 0.78), y=int(Y_size / 13))
    root_clahe.mainloop()


def Resolution():

    root_res = Toplevel()
    root_res.geometry("{}x{}".format(int(X_size/2 ), int(Y_size/2)))
    root_res.title("Resolution")

    root_res.mainloop()


def show_image(root):
    root.destroy()
    App_func()
    # ImageWindow = Toplevel()
    # ImageWindow.title(Img_name + "  Type: ")
    #
    # ImageAct = ImageTk.PhotoImage(Image.open(Origin_image))
    # CreatedImageLabel = Label(ImageWindow, image=ImageAct)
    # CreatedImageLabel.pack()
    #
    # ImageWindow.mainloop()


def App_func():
    App = Toplevel()
    App.tk.call('wm', 'iconphoto', App._w, logo_img)
    screen_posx = (monitor_width) / 2 - AppX_size / 2
    screen_posy = (monitor_height) / 2 - AppY_size / 2

    App.geometry(f'{AppBG_SIZE}+{int(screen_posx)}+{int(screen_posy)}')

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
        SaveFileButton = Button(App, text="Save file", padx=AppX_size / 50, pady=AppY_size / 150, command=lambda: save_file(App))
        SaveFileButton.place(x=AppX_size - AppX_size / 9.7, y=AppY_size / 75 * 10)

    if Origin_image == r"images/No_img.png":
        ShowImageButton = Button(App, text="Show Image", padx=AppX_size / 100, pady=AppY_size / 150, state="disabled")
        ShowImageButton.place(x=AppX_size - AppX_size / 9.7, y=AppY_size / 75 * 20)
    else:
        ShowImageButton = Button(App, text="Show Image", padx=AppX_size / 100, pady=AppY_size / 150,
                                 command=lambda: show_image(App))
        ShowImageButton.place(x=AppX_size - AppX_size / 9.7, y=AppY_size / 75 * 20)

    if Origin_image == r"images/No_img.png":
        MakeGrayButton = Button(App, text="Make Gray", padx=AppX_size / 25.6, pady=AppY_size / 150,
                                state="disabled")
        MakeGrayButton.place(x=AppX_size / 8, y=AppY_size / 1.9)
    else:
        MakeGrayButton = Button(App, text="Make Gray", padx=AppX_size / 25.6, pady=AppY_size / 150,
                                command=MakeGray)
        MakeGrayButton.place(x=AppX_size / 8, y=AppY_size / 1.9)

    if Origin_image == r"images/No_img.png":
        BinarizationButton = Button(App, text="Binarization", padx=AppX_size / 28, pady=AppY_size / 150,
                                    state="disabled")
        BinarizationButton.place(x=AppX_size / 8, y=AppY_size / 1.74)
    else:
        BinarizationButton = Button(App, text="Binarization", padx=AppX_size / 28, pady=AppY_size / 150,
                                    command=get_data_binarization)
        BinarizationButton.place(x=AppX_size / 8, y=AppY_size / 1.74)

    if Origin_image == r"images/No_img.png":
        ShowHistogramButton = Button(App, text="Histogram", padx=AppX_size / 25.5, pady=AppY_size / 150,
                                    state="disabled")
        ShowHistogramButton.place(x=AppX_size / 8, y=AppY_size / 1.6)
    else:
        ShowHistogramButton = Button(App, text="Histogram", padx=AppX_size / 25.5, pady=AppY_size / 150,
                                    command=show_histogram)
        ShowHistogramButton.place(x=AppX_size / 8, y=AppY_size / 1.6)

    if Origin_image == r"images/No_img.png":
        ShowHistogramColorButton = Button(App, text="Color Histogram", padx=AppX_size / 43.5, pady=AppY_size / 150,
                                     state="disabled")
        ShowHistogramColorButton.place(x=AppX_size / 8, y=AppY_size / 1.48)
    else:
        ShowHistogramColorButton = Button(App, text="Color Histogram", padx=AppX_size / 43.5, pady=AppY_size / 150,
                                     command=show_color_histogram)
        ShowHistogramColorButton.place(x=AppX_size / 8, y=AppY_size / 1.48)  #TODO check whether possible or not

    if Origin_image == r"images/No_img.png":
        NormalizeHistogramButton = Button(App, text="Normalize Histogram", padx=AppX_size / 95.5, pady=AppY_size / 150,
                                     state="disabled")
        NormalizeHistogramButton.place(x=AppX_size / 8, y=AppY_size / 1.38)
    else:
        NormalizeHistogramButton = Button(App, text="Normalize Histogram", padx=AppX_size / 95.5, pady=AppY_size / 150,
                                     command=normalize_histogram)
        NormalizeHistogramButton.place(x=AppX_size / 8, y=AppY_size / 1.38)

    if Origin_image == r"images/No_img.png":
        EqualHistogramButton = Button(App, text="Equal Histogram", padx=AppX_size / 43, pady=AppY_size / 150,
                                          state="disabled")
        EqualHistogramButton.place(x=AppX_size / 8, y=AppY_size / 1.29)
    else:
        EqualHistogramButton = Button(App, text="Equal Histogram", padx=AppX_size / 43, pady=AppY_size / 150,
                                          command=equal_histogram)
        EqualHistogramButton.place(x=AppX_size / 8, y=AppY_size / 1.29)

    if Origin_image == r"images/No_img.png":
        CLAHEHistogramButton = Button(App, text="CLAHE", padx=AppX_size / 20.5, pady=AppY_size / 150,
                                      state="disabled")
        CLAHEHistogramButton.place(x=AppX_size / 8, y=AppY_size / 1.21)
    else:
        CLAHEHistogramButton = Button(App, text="CLAHE", padx=AppX_size / 20.5, pady=AppY_size / 150,
                                      command=CLAHE_get_data)
        CLAHEHistogramButton.place(x=AppX_size / 8, y=AppY_size / 1.21)
        CreateToolTip.CreateToolTip(CLAHEHistogramButton,
                                    text="CLAHE - Contrast Limited Adaptive Histogram Equalization\n This is more effective way of equalizing histogram. It eliminate noises and do not enhance them. ")

    if Origin_image == r"images/No_img.png":
        ColorConversionButton = Button(App, text="Space Color", padx=AppX_size / 90, pady=AppY_size / 150,
                                      state="disabled")
        ColorConversionButton.place(x=AppX_size - AppX_size / 9.7, y=AppY_size / 75 * 28)
    else:
        ColorConversionButton = Button(App, text="Space Color", padx=AppX_size / 90, pady=AppY_size / 150,
                                      command=SpaceColor)
        ColorConversionButton.place(x=AppX_size - AppX_size / 9.7, y=AppY_size / 75 * 28)
        CreateToolTip.CreateToolTip(ColorConversionButton,
                                    text="This function shows color histogram of photo. It also equalize it. If you want save ")

    if Origin_image == r"images/No_img.png":
        ResolutionButton = Button(App, text="Resolution", padx=AppX_size / 68, pady=AppY_size / 150,
                                      state="disabled")
        ResolutionButton.place(x=AppX_size - AppX_size / 9.7, y=AppY_size / 75 * 35.5)
    else:
        ResolutionButton = Button(App, text="Resolution", padx=AppX_size / 68, pady=AppY_size / 150,
                                      command=Resolution)
        ResolutionButton.place(x=AppX_size - AppX_size / 9.7, y=AppY_size / 75 * 35.5)


    App.mainloop()


def open_file(App):
    global Origin_image, No_img, Img_name, Type_of_Image, Img_CV
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
        if os.path.exists("workspace/ActualImg.png"):
            os.remove("workspace/ActualImg.png")

        img_act = cv2.imread(filename)
        Img_CV = np.array(img_act).astype(np.uint8)
        # Img_CV = cv2.cvtColor(Img_CV, cv2.COLOR_BGR2RGB)
        cv2.imwrite(PATH_C + "workspace/ActualImg.png", Img_CV)

        Origin_image = "workspace/ActualImg.png"
        App.destroy()
        App_func()


if __name__ == "__main__":
    Root = Tk()
    Root.title("Vision For Visionaries")

    screen_posx = (monitor_width) / 2 - X_size / 2
    screen_posy = (monitor_height) / 2 - Y_size / 2

    Root.geometry(f'{BG_SIZE}+{int(screen_posx)}+{int(screen_posy)}')  # 800x600
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
