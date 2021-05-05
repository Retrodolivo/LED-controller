'''
import serial.tools.list_ports

for port in serial.tools.list_ports.comports():
    print(port.vid + port.pid)
'''

import sys
import glob

import serial
import tkinter as tk
from tkinter import ttk
from functools import partial

win = tk.Tk()
win.geometry("350x300")
win.title("RGB LED Control Panel")

com = {'ser': 0, 'is_found': False}
color = {'red': 0, 'green': 0, 'blue': 0}

def init(com):
    if not com['is_found']:
        led_on_btn["state"] = "disabled"
        led_off_btn["state"] = "disabled"
        color_red_slide["state"] = "disabled"
        color_green_slide["state"] = "disabled"
        color_blue_slide["state"] = "disabled"
        

def serial_ports():
    if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    else:
        raise EnvironmentError('Unsupported platform')
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass     
    return result

def hookup(com):
    if com_connect_btn["text"] == "Disconnect":
       print(com['ser'].name, "is closed")
       com['ser'].close()
       com_combobox["state"] = "normal"
       com_connect_btn["text"] = "Connect"
       led_on_btn["state"] = "disabled"
       led_off_btn["state"] = "disabled"
       color_red_slide["state"] = "disabled"
       color_green_slide["state"] = "disabled"
       color_blue_slide["state"] = "disabled"
       
    else:
        com['ser'] = serial.Serial(com_combobox.get())
        if com['ser'].is_open:
            print(com['ser'].name, "is open")
            com['is_found'] = True
            com_connect_btn["text"] = "Disconnect"
            led_on_btn["state"] = "normal"
            led_off_btn["state"] = "normal"
            com_combobox["state"] = "disabled"
            color_red_slide["state"] = "normal"
            color_green_slide["state"] = "normal"
            color_blue_slide["state"] = "normal"

def led_on(com):
    if com['is_found']:
        tx_data = "led on~"
        for byte in tx_data:
            com['ser'].write(bytearray(byte, 'utf-8'))

def led_off(com):
    if com['is_found']:
        tx_data = "led off~"
        for byte in tx_data:
            com['ser'].write(bytearray(byte, 'utf-8'))

def set_color(com, color):
    if com['is_found']:
        tx_data = 'C' + chr(red.get()) + chr(green.get()) + chr(blue.get()) + '~'
        print(tx_data)
        for byte in tx_data:
            com['ser'].write(bytearray(byte, 'iso8859-1'))

#--------Connection--------------#
connection_lframe = tk.LabelFrame(win, text = "Connection", font = "Arial 10",
                                  width = 200, height = 100)
connection_lframe.grid(row = 0, column = 0, pady = 10, padx = 10)

com_label = tk.Label(connection_lframe, text = "COM", font = "Arial 10")
com_label.grid(row = 0, column = 0, pady = 5, padx = 5)

com_combobox = ttk.Combobox(connection_lframe, values = serial_ports(),
                            width = 7)
com_combobox.grid(row = 0, column = 1, pady = 5, padx = 5)

com_connect_btn = tk.Button(text = "Connect", font = "Arial 10", command = partial(hookup, com))
com_connect_btn.grid(in_ = connection_lframe, pady = 3, padx = 3)
com_connect_btn.bind("<Button-1>")
#--------LED control--------------#
led_control_lframe = tk.LabelFrame(win, text = "LED control", font = "Arial 10",
                                   width = 100, height = 200)
led_control_lframe.grid(row = 0, column = 1, pady = 10, padx = 10)
led_on_btn = tk.Button(text = "ON", font = "Arial 10", command = partial(led_on, com))
led_on_btn.grid(in_ = led_control_lframe, row = 0, column = 0, pady = 3, padx = 3)
led_on_btn.bind("<Button-1>")

led_off_btn = tk.Button(text = "OFF", font = "Arial 10", command = partial(led_off, com))
led_off_btn.grid(in_ = led_control_lframe, row = 0, column = 1, pady = 3, padx = 3)
led_off_btn.bind("<Button-1>")
#--------Color--------------------#
color_lframe = tk.LabelFrame(win, text = "Color", font = "Arial 10",
                                   width = 100, height = 100)
color_lframe.grid(row = 1, column = 1, pady = 10, padx = 10)

color_red_label = tk.Label(color_lframe, text = "R", font = "Arial 10 bold", fg = "white", bg = "red")
color_red_label.grid(row = 0, column = 0, pady = 2, padx = 2)

color_red_label = tk.Label(color_lframe, text = "G", font = "Arial 10 bold", fg = "white", bg = "green")
color_red_label.grid(row = 1, column = 0, pady = 2, padx = 2)

color_red_label = tk.Label(color_lframe, text = "B", font = "Arial 10 bold", fg = "white", bg = "blue")
color_red_label.grid(row = 2, column = 0, pady = 2, padx = 2)

red = tk.IntVar()
green = tk.IntVar()
blue = tk.IntVar()

color_red_slide = tk.Scale(color_lframe, font = "Arial 10 bold", orient = tk.HORIZONTAL,
                     from_ = 0, to_ = 255, resolution = 1, variable = red, command = partial(set_color, com))
color_red_slide.grid(in_ = color_lframe, row = 0, column = 1, pady = 3, padx = 3)
color_green_slide = tk.Scale(color_lframe, font = "Arial 10 bold", orient = tk.HORIZONTAL,
                     from_ = 0, to_ = 255, resolution = 1, variable = green, command = partial(set_color, com))
color_green_slide.grid(in_ = color_lframe, row = 1, column = 1, pady = 3, padx = 3)
color_blue_slide = tk.Scale(color_lframe, font = "Arial 10 bold", orient = tk.HORIZONTAL,
                     from_ = 0, to_ = 255, resolution = 1, variable = blue, command = partial(set_color, com))
color_blue_slide.grid(in_ = color_lframe, row = 2, column = 1, pady = 3, padx = 3)


init(com)
win.mainloop()
