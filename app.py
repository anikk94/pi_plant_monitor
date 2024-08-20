#!/usr/bin/env python3
import tkinter as tk
from datetime import datetime
import os
import sys

from file_operations import FileHandler

import RPi.GPIO as GPIO

def draw_widgets():
    pass

def update_plant_watered_datetime():
    # instead of displaying the current time, display the time in hours since last watering, or display that information in addition to date of last watering
    global plant_watered_datetime
    plant_watered_datetime = datetime.now()
    msg = plant_watered_datetime.strftime("%Y-%m-%d %H:%M:%S")
    water_reminder_label.config(text=f"Plant last watered at: {msg}")
    file_ops.append_line(msg+'\n')

    update_file_display()

def update_time_since_plant_watered():
    if not plant_watered_datetime:
        root.after(1000, update_time_since_plant_watered)
        return

    diff = datetime.now() - plant_watered_datetime
    diff_seconds = int(diff.total_seconds())
    h = diff_seconds//3600
    m = (diff_seconds%3600)//60
    s = diff_seconds%60
    msg = f"{h:02}:{m:02}:{s:02}"
    #print(f"time difference: {diff}, {diff_seconds}, {msg}")
    time_since_plant_watered_timer_label.config(text=f"{msg}")

    root.after(1000, update_time_since_plant_watered)
    
def update_label():
    # TODO
    # make this event based not timer based
    W = root.winfo_width()
    H = root.winfo_height()
    msg = f"screen resolution: {W} x {H}"
    screen_info_label.config(text=msg)
    root.after(1000, update_label)

def read_file_line():
    print(f"file read: {file_ops.read_line()}")
    
def update_file_display():
    file_content_list = file_ops.read_file().split('\n')
    if file_content_list:
        print("file_content_list not empty")
        current_size = file_display.size()
        print(f"current size of file_display: {current_size}")
        file_display.delete(0, current_size)
        print("repopulating")
        for line in file_content_list:
            if line:
                line = datetime.fromisoformat(line)
            file_display.insert(tk.END, line)

def button_cb(channel):
    print(f"button pressed, cb arg: {channel}")
    update_plant_watered_datetime()
# ==============================================================================
# MAIN
# ==============================================================================

data_file_name = "data.txt"
file_ops = FileHandler(data_file_name)

root = tk.Tk()
root.title("DesktopDisplayApp")
root.geometry("1000x500")
#root.configure(bg='blue')

plant_watered_datetime = None
# get the datetime of the most recent plant watering from file
if os.path.exists(data_file_name):
    print(f"file name: {data_file_name} exists") 
    
    file_content_list = file_ops.read_file().split('\n')
    for line in file_content_list[::-1]:     
        if line:
            print("line:", line)
            plant_watered_datetime = datetime.fromisoformat(line)
            break
    else:
        print("data file is empty")
else:
    print(f"file name: {data_file_name} doesn't exist")

print(f"plant watered datetime: {plant_watered_datetime}")

draw_widgets()

root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)

# Frame 2
frame2 = tk.Frame(root)
frame2.configure(bg="green")
frame2.grid(row=0, column=0, sticky="nsew")

placeholder_label = tk.Label(frame2, text="frame2")
placeholder_label.pack(fill='x')

plant_water_task_label = tk.Label(frame2, text="Plant Watering")
plant_water_task_label.pack(fill='x')

task2_label = tk.Label(frame2, text="Task 2")
task2_label.pack(fill='x')

task3_label = tk.Label(frame2, text="Task 3")
task3_label.pack(fill='x')

button1 = tk.Button(frame2, text="Plant Watering")
button1.pack(fill='x')

button2 = tk.Button(frame2, text="task 2")
button2.pack(fill='x')

button3 = tk.Button(frame2, text="task 3")
button3.pack(fill='x')

# Frame 1
frame1 = tk.Frame(root)
frame1.configure(bg="lightblue")
frame1.grid(row=0, column=1, sticky="nsew")

date = datetime.today()
date_label = tk.Label(frame1, text=f"{date}")
date_label.pack(fill="x")

water_reminder_label = tk.Label(frame1, text=f"Plant last watered at: {plant_watered_datetime}", font=("Arial", 18))
water_reminder_label.pack(pady=(20, 0))

time_since_plant_watered_label = tk.Label(frame1, text="Plant not watered for (HH:MM:SS)", font=("Arial", 18))
time_since_plant_watered_label.pack(pady=(20, 0))
time_since_plant_watered_timer_label = tk.Label(frame1, text="--:--:--", font=("Arial",72))
time_since_plant_watered_timer_label.pack(pady=(20, 0))

plant_watered_button = tk.Button(frame1, text="Plant Watered", command=update_plant_watered_datetime)
plant_watered_button.pack(pady=(20, 0))

screen_info_label = tk.Label(frame1, text="screen_resolution: NaN")
screen_info_label.pack(side="bottom", fill="x")

file_display = tk.Listbox(frame1)
file_display.pack(pady=(20, 0))

button_pin = 11 # gpio 17

GPIO.setmode(GPIO.BOARD)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(button_pin, GPIO.RISING, callback=button_cb, bouncetime=1000)

# -- app initializations -------------------------------------------------------

update_file_display()

root.after(1000, update_label)
root.after(1000, update_time_since_plant_watered)

root.mainloop()

print("GPIO.cleanup()")
GPIO.cleanup()


