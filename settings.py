#!/usr/bin/python
# -*- coding: utf-8 -*-
import screeninfo
monitor_width = screeninfo.get_monitors()[0].width
monitor_height = screeninfo.get_monitors()[0].height

X_size = 800
Y_size = 600
BG_SIZE = str(X_size) + "x" + str(Y_size) # this variable describes size of display

AppX_size = 1000
AppY_size = 750
AppBG_SIZE = str(AppX_size) + "x" + str(AppY_size)
