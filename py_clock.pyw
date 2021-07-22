# pylint: disable=unused-wildcard-import, method-hidden
#
# #---------------------------------------------------------------------------
# Name:        my_clock
# Purpose:
#
# Author:      PHedlund
#
# Created:     09/09/2020
# Copyright:   (c) PHedlund 2020
#---------------------------------------------------------------------------

##  ------------------------------------------------------------------------
##  Imports
##  ------------------------------------------------------------------------
import os
import sys
import time
import math
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import font
import winsound
from configparser import ConfigParser

from mylib.clock_face import my_clock
from mylib.seven_seg import Clock_Led

##  ------------------------------------------------------------------------
##  ToDo List
##  ------------------------------------------------------------------------
# DONE Save alarms to file
# DONE Read Alarms from file, if file does not exist create default
# DONE When Set Alarms window is called up place it over the clock
#      i.e. get current xy of clock then place new window at +10
# DONE Add quit to main screen (buttons down 1 center time)
# DONE Document array of IntVar() and StringVar()
# DONE Document array of checkbuttons / array of Entry (2)


##  ------------------------------------------------------------------------
##  Constants
##  ------------------------------------------------------------------------
alarms = (('11','59','58','1'), ('12','40','0','1'), ('16','25','0','1'),
          ('9','10','5','0'),   ('0','0','0','0'),   ('0','0','0','0'),
          ('0','0','0','0'),   ('0','0','0','0'))
fn = os.path.dirname(sys.argv[0]) + '\\' + 'py_clock.ini'
max_alarms = 8
analog = 0
digital = 1
display_type = analog
_debug_ = 0
my_colors = ('red', 'green', 'blue')
Version = 1.0
##  ------------------------------------------------------------------------
##  Classes
##  ------------------------------------------------------------------------


##  ------------------------------------------------------------------------
##  Functions
##  ------------------------------------------------------------------------


def save_alarms():
    config = ConfigParser()
    reload.set(0)
    if remember.get() == 1:
        xx, yy = get_xy_pos()
        if _debug_ == 1:
            print(f'{xx}, {yy}')
        x_pos.set(xx)
        y_pos.set(yy)
    newc = my_colors.index(c_var.get())
    if d_color.get() != newc:
        d_color.set(newc)
        reload.set(1)
    if display.get() != disp_mode.get():        
        reload.set(1)
    for x in range(0,max_alarms):
        config[f'alarm{x}'] = {'enable' : al_state[x].get(),
                               'hour'   : hr[x].get(),
                               'min'    : mn[x].get(),
                               'sec'    : sc[x].get() }
    config['display type'] = {'type' : display.get(),
                              'color' : d_color.get()}
    config['position'] = {'remember' : remember.get(),
                          'x_pos'    : x_pos.get(),
                          'y_pos'    : y_pos.get() }
    with open(fn, 'w') as configfile:
        config.write(configfile)


def load_alarms():
    config = ConfigParser()
    config.read(fn)
    for x in range(0,max_alarms):
        al_state[x].set(config[f'alarm{x}']['enable'])
        hr[x].set(config[f'alarm{x}']['hour'])
        mn[x].set(config[f'alarm{x}']['min'])
        sc[x].set(config[f'alarm{x}']['sec'])
    disp_mode.set(config['display type']['type'])
    d_color.set(config['display type']['color'])
    remember.set(config['position']['remember'])
    x_pos.set(config['position']['x_pos'])
    y_pos.set(config['position']['y_pos'])

def get_xy_pos():
    rg = root.geometry()
    xi = rg.find('+')
    yi = rg.find('+', xi+1)
    x = int(rg[xi+1:yi])
    y = int(rg[yi+1:len(rg)])
    return x, y


def setup_quit():
    global top
    if _debug_ == 1:
        for x in range(0, max_alarms):
            st = f'{x}:  {hr[x].get():>2} : {mn[x].get():>2} : {sc[x].get():>2}'
            st = st + f'  ST-{al_state[x].get()} '
            print(st)
    top.destroy()
    if reload.get() == 1:
        reload.set(0)
        # python = sys.executable
        # os.execl(python, python, * sys.argv)
        os.execv(sys.executable, ['Python'] + sys.argv)


def setup_window():
    global top
    try:
        if top.state() == 'normal':
            top.focus()
    except:
        top = Toplevel()
        top.title('Setting')
        x,y = get_xy_pos()
        top.geometry(f'190x270+{x+20}+{y+20}')
        for x in range(0,max_alarms):
            tk.Label(top, text='  ').grid(column=0, row=x+1)
            lb = tk.Label(top, text=str(x+1))
            lb.grid(column=1, row=x+1, padx=5)

            r = ttk.Checkbutton(top, variable=al_state[x])
            r.grid(column=2, row=x+1)

            en = tk.Entry(top, textvariable=hr[x], width=3)
            en.grid(column=3, row=x+1)

            lb = tk.Label(top, text=' : ')
            lb.grid(column=4, row=x+1)

            en = tk.Entry(top, textvariable=mn[x], width=3)
            en.grid(column=5, row=x+1)

            lb = tk.Label(top, text=' : ')
            lb.grid(column=6, row=x+1)

            en = tk.Entry(top, textvariable=sc[x], width=3)
            en.grid(column=7, row=x+1)

            tk.Label(top, text='   ').grid(column=8, row=x+1)
        tk.Label(top, text='  ').grid(column=3, row=x+2)
        display.set(disp_mode.get())
        ds1 = tk.Radiobutton(top, text='Analog', variable=display, value=0)
        ds1.grid(column=0, row=x+2, columnspan=3)
        ds2 = tk.Radiobutton(top, text='Digital', variable=display, value=1)
        ds2.grid(column=4, row=x+2, columnspan=3)
        rem = ttk.Checkbutton(top, variable=remember, text='Save x,y')
        rem.grid(column=0, row=x+3, columnspan=3)
        ddb = ttk.Combobox(top, values=my_colors, width=8, textvariable=c_var)
        ddb.grid(column=4, row=x+3, columnspan=3)
        ddb.current(d_color.get())

        qu = tk.Button(top, text='  Exit  ', command=setup_quit)
        qu.grid(column=4,row=x+5, columnspan=3, pady=3)
        qu2 = tk.Button(top, text='  SAVE  ', command=save_alarms)
        qu2.grid(column=0,row=x+5, columnspan=3, pady=3)


##  ------------------------------------------------------------------------
##  Controls
##  ------------------------------------------------------------------------


def reload_time():
    tm = time.localtime(time.time())
    for x in range(0, max_alarms):
        if al_state[x].get() == 1:
            if tm.tm_hour == int(hr[x].get()) and    \
                tm.tm_min == int(mn[x].get()) and    \
                tm.tm_sec == int(sc[x].get()) :
                alarming.set(1)
                alarm_snd.set(1)
    if int(disp_mode.get()) == analog:
        altitude.show_full_time(tm.tm_hour, tm.tm_min, tm.tm_sec)
    else :
        clk.num(tm.tm_hour, tm.tm_min, tm.tm_sec)
    my_tm = f'  {tm.tm_hour:02}:{tm.tm_min:02}:{tm.tm_sec:02}'
    if int(disp_mode.get()) == analog:
        lbl.config(text=my_tm)
    if alarm_snd.get() == 1:
        winsound.PlaySound('c:\\Windows\\Media\\Alarm01.wav', winsound.SND_ASYNC)
        alarm_snd.set(0)
    if alarming.get() == 1:
        if (tm.tm_sec % 2) == 0:
            cv.config(bg=bkgnd)
        else:
            cv.config(bg='red')
    else:
        cv.config(bg=bkgnd)
    root.after(1000, reload_time)


def quit_prog():
    root.destroy()


def quiet_prog():
    alarming.set(0)


##  ------------------------------------------------------------------------
##
##  GUI Program Starts Here
##
##  ------------------------------------------------------------------------

root = tk.Tk()
# root.wm_attributes("-topmost", 1)
disp_mode = IntVar()
display = IntVar()
remember = IntVar()
x_pos = IntVar()
y_pos = IntVar()
d_color = IntVar()
c_var = StringVar()
reload = IntVar()
disp_mode.set(0)
x_pos.set(10)
y_pos.set(10)
d_color.set(1)
c_var.set('')
reload.set(0)
bg_a = 'white'
bg_b = 'black'

al_state = []; hr = []; mn = []; sc=[]
for x in range(0,max_alarms):
    al_state.append(0)
    al_state[x] = IntVar()
    al_state[x].set(0)
    hr.append(0)
    hr[x] = StringVar()
    hr[x].set(0)
    mn.append(0)
    mn[x] = StringVar()
    mn[x].set(0)
    sc.append(0)
    sc[x] = StringVar()
    sc[x].set(0)
    if os.path.exists(fn) == False:
        al_state[x].set(alarms[x][3])
        hr[x].set(alarms[x][0])
        mn[x].set(alarms[x][1])
        sc[x].set(alarms[x][2])

if os.path.exists(fn) == False:
    save_alarms()
load_alarms()
if remember.get() == 0:
    x_pos.set(10)
    y_pos.set(10)

if disp_mode.get() == analog:
    bkgnd = bg_a
    root.geometry('%dx%d+%d+%d' % (245, 270, x_pos.get(), y_pos.get()))
    root.title("PyClock")

    cv = tk.Canvas(root, height=210, width=240, bg=bkgnd)
else :
    bkgnd = bg_b
    root.geometry('%dx%d+%d+%d' % (245, 150, x_pos.get(), y_pos.get()))
    root.title("PyClock")

    cv = tk.Canvas(root, height=90, width=240, bg=bkgnd)
cv.grid(column=0, row=1, columnspan=10)
s6 = ttk.Style()
s6.configure('red.TButton', background='Red')

alarming = IntVar()
alarm_snd = IntVar()

alarming.set(0)
alarm_snd.set(0)
if _debug_ == 1:
    print(disp_mode.get())

_font = font.Font(weight='bold')

alt_mtr = {'X1': 40, 'Y1': 30, 'width':160 }

if int(disp_mode.get()) == analog:
    altitude = my_clock(cv, alt_mtr)
else :
    clk = Clock_Led(cv, x=25, y=20, mode=1, myfill=my_colors[d_color.get()])

lbl = tk.Label(root, text='', font = _font)
lbl.grid(column=0, row=4, columnspan=3)

stop2_b = tk.Button(root, text=' Settings ', command= setup_window)
stop2_b.grid(column=0, row=5, padx=1)

stop2_a = tk.Button(root, text=' Cancel Alarm ', command=quiet_prog)
stop2_a.grid(column=1, row=5, padx=1)

quit = ttk.Button(root, text=' Quit ', command=quit_prog, style='red.TButton')
quit.grid(column=2, row=5, padx=1)

reload_time()

root.mainloop()

