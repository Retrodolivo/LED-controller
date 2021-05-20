import sys
import glob
import time

import serial
import tkinter as tk
from tkinter import ttk
from functools import partial
from datetime import datetime

win = tk.Tk()
win.geometry("400x300")
win.resizable(width=False, height=False)
win.title("RGB LED Control Panel")
#win.configure(background='pink')

red = tk.IntVar()
green = tk.IntVar()
blue = tk.IntVar()

com = {'ser': 0, 'is_found': False, 'cmd_stop_byte': '~'}

cmds = {
        'led_on': {'tx_data': 'O' + com['cmd_stop_byte'],
                   'ack_byte': b'O',
                   'status': {'OK': "LED is ON",
                              'ERR': "ERR_O"}},
        
        'led_off': {'tx_data': 'F' + com['cmd_stop_byte'],
                    'ack_byte': b'F',
                    'status': {'OK': "LED is OFF",
                               'ERR': "ERR_F"}},
        
        'set_color': {'tx_data': 'filled below',
                      'ack_byte': b'C',
                      'status': {'OK': "filled below",
                                 'ERR': "ERR_C"}},
        
        'set_brightness': {'tx_data': 'filled below'},

        'launch_scheduler': {'tx_data': 'filled below',
                             'ack_byte': b'A',
                             'status': {'OK': "Time is set",
                                        'ERR': "ERR_A"}},
        
        'send_sys_time': {'tx_data': 'filled below',
                          'ack_byte': b'T',
                          'status': {'OK': "Systime was tx to mcu",
                                     'ERR': "ERR_T"}}
        }
                       
color = {'red': 0, 'green': 0, 'blue': 0}

time = {'hours': list(range(0, 24, 1)), 'min': list(range(0, 60, 1))}
dt = datetime.now()

def init(com):
    if not com['is_found']:
        led_on_btn["state"] = "disabled"
        led_off_btn["state"] = "disabled"
        color_red_slide["state"] = "disabled"
        color_green_slide["state"] = "disabled"
        color_blue_slide["state"] = "disabled"
        OFF_hour_combobox["state"] = "disabled"
        OFF_min_combobox["state"] = "disabled"
        Scheduler_btn["state"] = "disabled"
        brightness_slide.set(100)
    #check if serial_ports() find comports
    if("COM" in serial_ports()[0]):
        com_combobox.set(serial_ports()[0])



'''
find com ports
return: list of available com ports
'''
def serial_ports():
    if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
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

'''
make dis/connection to choosen comport
'''
def connection(com):
    if com_connect_btn["text"] == "Disconnect":
       com['ser'].close()
       Status_info_label['text'] = com['ser'].name + " is closed"
       
       com_connect_btn["text"] = "Connect"
       com_combobox["state"] = "normal"
       led_on_btn["state"] = "disabled"
       led_off_btn["state"] = "disabled"
       color_red_slide["state"] = "disabled"
       color_green_slide["state"] = "disabled"
       color_blue_slide["state"] = "disabled"
       OFF_hour_combobox["state"] = "disabled"
       OFF_min_combobox["state"] = "disabled"
       Scheduler_btn["state"] = "disabled"

    else:
        com['ser'] = serial.Serial(com_combobox.get())
        if com['ser'].is_open:
            com['is_found'] = True
            Status_info_label['text'] = com['ser'].name + " is open"
            send_sys_time()
            
            com_connect_btn["text"] = "Disconnect"
            led_on_btn["state"] = "normal"
            led_off_btn["state"] = "normal"
            com_combobox["state"] = "disabled"
            color_red_slide["state"] = "normal"
            color_green_slide["state"] = "normal"
            color_blue_slide["state"] = "normal"
            OFF_hour_combobox["state"] = "normal"
            OFF_min_combobox["state"] = "normal"
            Scheduler_btn["state"] = "normal"

#-------------vcp commands----------------------#                
def led_on():
    Status_info_label['text'] = send_cmd("led_on")
    
def led_off():
    Status_info_label['text'] = send_cmd("led_off")

def set_color(cmds):
    Color_canvas['bg'] = send_cmd("set_color")

def set_brightness(color):
    Color_canvas['bg'] = send_cmd("set_brightness")

def launch_scheduler():
    Status_info_label['text'] = send_cmd("launch_scheduler")

def send_sys_time():
    Status_info_label['text'] = send_cmd("send_sys_time")
    tx_data = 'T' + (chr(dt.year % 2000) + chr(dt.month) + chr(dt.day) +
                    chr(dt.hour) + chr(dt.minute) + chr(dt.second) +
                    com['cmd_stop_byte'])
    for byte in cmds['led_off']['tx_data']:
        com['ser'].write(bytearray(byte, 'iso8859-1'))


def send_cmd(cmd):
    if com['is_found']:
        #clear input vcp buffer
        com['ser'].flushInput()

        if(cmd in cmds.keys()):
            if(cmd == "led_on"):
                for byte in cmds[cmd]['tx_data']:
                    com['ser'].write(bytearray(byte, 'iso8859-1'))
                #check received data
                return ack_cmd(cmd)

            if(cmd == "led_off"):
                for byte in cmds[cmd]['tx_data']:
                    com['ser'].write(bytearray(byte, 'iso8859-1'))
                return ack_cmd(cmd)

            if(cmd == "set_color"):
                cmds[cmd]['tx_data'] = 'C' + chr(red.get()) + chr(green.get()) + chr(blue.get()) + com['cmd_stop_byte']
                for byte in cmds[cmd]['tx_data']:
                    com['ser'].write(bytearray(byte, 'iso8859-1'))
                while True:
                    rx_data = com['ser'].read()
                    if rx_data == cmds[cmd]['ack_byte']:
                        cmds[cmd]['status']['OK'] = '#%02x%02x%02x' % (red.get(), green.get(), blue.get())
                        status = cmds[cmd]['status']['OK']
                        return status
                        break
                    else:
                        status = cmds[cmd]['status']['ERR']
                        return status
                        break

            if(cmd == "set_brightness"):
                cmds[cmd]['tx_data'] = 'B' + chr(brightness.get()) + com['cmd_stop_byte']
                for byte in cmds[cmd]['tx_data']:
                    com['ser'].write(bytearray(byte, 'iso8859-1'))

            if(cmd == "launch_scheduler"):
                cmds[cmd]['tx_data'] = 'A' + (chr(int(OFF_hour_combobox.get())) + chr(int(OFF_min_combobox.get())) +
                                com['cmd_stop_byte'])
                for byte in cmds[cmd]['tx_data']:
                    com['ser'].write(bytearray(byte, 'utf-8'))
                return ack_cmd(cmd)

            if(cmd == "send_sys_time"):
                cmds[cmd]['tx_data'] = 'T' + (chr(dt.year % 2000) + chr(dt.month) + chr(dt.day) +
                                              chr(dt.hour) + chr(dt.minute) + chr(dt.second) + com['cmd_stop_byte'])
                for byte in cmds[cmd]['tx_data']:
                    com['ser'].write(bytearray(byte, 'utf-8'))
                return ack_cmd(cmd)

def ack_cmd(cmd):
    while True:
        rx_data = com['ser'].read()
        if rx_data == cmds[cmd]['ack_byte']:
            status = cmds[cmd]['status']['OK']
            return status
            break
        else:
            status = cmds[cmd]['status']['ERR']
            return status
            break    
            

#-----------------------------------GUI-------------------------------------------#

#--------Connection--------------#
connection_lframe = tk.LabelFrame(win, text = "Connection", font = "Arial 10", width = 200, height = 100)
connection_lframe.grid(row = 0, column = 0, pady = 10, padx = 10)

com_label = tk.Label(connection_lframe, text = "COM", font = "Arial 10")
com_label.grid(row = 0, column = 0, pady = 5, padx = 5)

com_combobox = ttk.Combobox(connection_lframe, values = serial_ports(), width = 7)
com_combobox.grid(row = 0, column = 1, pady = 5, padx = 5)

com_connect_btn = tk.Button(text = "Connect", font = "Arial 10", command = partial(connection, com), width = 10)
com_connect_btn.grid(in_ = connection_lframe, pady = 3, padx = 3)
com_connect_btn.bind("<Button-1>")
#--------LED control--------------#
led_control_lframe = tk.LabelFrame(win, text = "LED control", font = "Arial 10", width = 100, height = 200)
led_control_lframe.grid(row = 0, column = 1, pady = 10, padx = 10)
led_on_btn = tk.Button(text = "ON", font = "Arial 10", command = led_on)
led_on_btn.grid(in_ = led_control_lframe, row = 0, column = 0, pady = 3, padx = 3)
led_on_btn.bind("<Button-1>")

led_off_btn = tk.Button(text = "OFF", font = "Arial 10", command = led_off)
led_off_btn.grid(in_ = led_control_lframe, row = 0, column = 1, pady = 3, padx = 3)
led_off_btn.bind("<Button-1>")
#--------Color--------------------#
color_lframe = tk.LabelFrame(win, text = "Color", font = "Arial 10", width = 100, height = 100)
color_lframe.grid(row = 1, column = 1, pady = 10, padx = 10)

color_red_label = tk.Label(color_lframe, text = "R", font = "Arial 10 bold", fg = "white", bg = "red")
color_red_label.grid(row = 0, column = 0, pady = 2, padx = 2)

color_red_label = tk.Label(color_lframe, text = "G", font = "Arial 10 bold", fg = "white", bg = "green")
color_red_label.grid(row = 1, column = 0, pady = 2, padx = 2)

color_red_label = tk.Label(color_lframe, text = "B", font = "Arial 10 bold", fg = "white", bg = "blue")
color_red_label.grid(row = 2, column = 0, pady = 2, padx = 2)


color_red_slide = tk.Scale(color_lframe, font = "Arial 10 bold", orient = tk.HORIZONTAL,
                     from_ = 0, to_ = 255, resolution = 1, variable = red, command = set_color)
color_red_slide.grid(in_ = color_lframe, row = 0, column = 1, pady = 3, padx = 3)
color_green_slide = tk.Scale(color_lframe, font = "Arial 10 bold", orient = tk.HORIZONTAL,
                     from_ = 0, to_ = 255, resolution = 1, variable = green, command = set_color)
color_green_slide.grid(in_ = color_lframe, row = 1, column = 1, pady = 3, padx = 3)
color_blue_slide = tk.Scale(color_lframe, font = "Arial 10 bold", orient = tk.HORIZONTAL,
                     from_ = 0, to_ = 255, resolution = 1, variable = blue, command = set_color)
color_blue_slide.grid(in_ = color_lframe, row = 2, column = 1, pady = 3, padx = 3)
#--------Brightness----------------#
brightness = tk.IntVar()

brightness_slide = tk.Scale(win, font = "Arial 10 bold", orient = tk.VERTICAL,
                     from_ = 100, to_ = 0, resolution = 1, variable = brightness, command = set_brightness)
brightness_slide.place(relx = 0.85, rely = 0.5)

img = tk.PhotoImage(file = r"C:\Users\User\Desktop\LED-controller\Software\Python_App\img\brightness.png")
img = img.subsample(7)
brigh_lbl = tk.Label(win, image = img)
brigh_lbl.place(relx = 0.895, rely = 0.35)
#--------Scheduler-----------------#
Scheduler_lframe = tk.LabelFrame(win, text = "Scheduler", font = "Arial 10", width = 200, height = 100)
Scheduler_lframe.grid(row = 1, column = 0, pady = 10, padx = 10)

OFF_label = tk.Label(Scheduler_lframe, text = "OFF", font = "Arial 10 bold")
OFF_label.grid(row = 1, column = 0, pady = 2, padx = 2)

OFF_hour_combobox = ttk.Combobox(Scheduler_lframe, values = time['hours'], width = 3)
OFF_hour_combobox.grid(row = 1, column = 1, pady = 5, padx = 5)

OFF_min_combobox = ttk.Combobox(Scheduler_lframe, values = time['min'], width = 3)
OFF_min_combobox.grid(row = 1, column = 2, pady = 5, padx = 5)

Scheduler_btn = tk.Button(text = "Launch", font = "Arial 10", command = launch_scheduler)
Scheduler_btn.grid(in_ = Scheduler_lframe, pady = 3, padx = 3)
Scheduler_btn.bind("<Button-1>")
#--------Status bar----------------#
Status_label = tk.Label(win, text = "Status:", font = "Arial 10 bold")
Status_label.place(relx = 0.04, rely = 0.85)

Status_info_label = tk.Label(win, text = "", font = "Arial 10")
Status_info_label.place(relx = 0.16, rely = 0.85)
#--------Color status--------------#
Color_canvas = tk.Canvas(win, width = 30, height = 30, bg='white')
Color_canvas.place(relx = 0.895, rely = 0.87)


init(com)
win.mainloop()
