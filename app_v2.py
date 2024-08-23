#!/usr/bin/env python3
import tkinter as tk
from datetime import datetime
import os
import sys

from file_operations import FileHandler

import RPi.GPIO as GPIO

class MainFrame(tk.Frame):
    def __init__(self, root):
        self.bg_col = "yellow"
        super().__init__(root, bg=self.bg_col)

        self.main_frame = self
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        #self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(0, weight=1) 

        self.data_file_name = "data.txt"
        self.file_ops = FileHandler(self.data_file_name)

        self.load_main_widgets()

    def load_main_widgets(self):
        self.draw_task_sidebar()
        self.draw_display_area()

    def draw_task_sidebar(self):
        self.task_sidebar = tk.Frame(
            self.main_frame,
            background="red",
        )
        self.task_sidebar.grid(column=0, row=0, sticky=tk.NSEW, padx=3, pady=3)
        
        self.task_sidebar.columnconfigure(0, weight=1)
        #self.task_sidebar.rowconfigure(0, weight=1)
        self.task_sidebar.rowconfigure(1, weight=1)
        self.task_sidebar.rowconfigure(2, weight=1)
        self.task_sidebar.rowconfigure(3, weight=1)

        title_label = tk.Label(self.task_sidebar, text="task_sidebar")
        title_label.grid(column=0, row=0, sticky='ew') 

        plant_watering_button = tk.Button(self.task_sidebar, text="Plant Watering")
        plant_watering_button.grid(column=0, row=1, sticky='nsew')

        task_2_button = tk.Button(self.task_sidebar, text="Weather")
        task_2_button.grid(column=0, row=2, sticky='nsew')

        task_3_button = tk.Button(self.task_sidebar, text="task 3")
        task_3_button.grid(column=0, row=3, sticky='nsew')


    def draw_display_area(self):
        self.display_area = tk.Frame(
            self.main_frame,
            background="green",
        )
        self.display_area.grid(column=1, row=0, sticky=tk.NSEW)

        self.display_area.columnconfigure(0, weight=1)
        self.display_area.rowconfigure(0, weight=0)
        self.display_area.rowconfigure(1, weight=1)


        title_label = tk.Label(self.display_area, text="display_area")
        title_label.grid(column=0, row=0, sticky='ew', padx=3, pady=3)

        self.draw_plant_monitor(self.display_area)


    def draw_plant_monitor(self, parent_frame):

        self.plant_monitor = tk.Frame(
            parent_frame,
            background="lightblue",
        )
        self.plant_monitor.grid(column=0, row=1, sticky=tk.NSEW, padx=3, pady=3)

        self.plant_monitor.columnconfigure(0, weight=4) # message display area, using pack here so seperate frame
        self.plant_monitor.columnconfigure(1, weight=1) # file display area
        self.plant_monitor.rowconfigure(0, weight=1) 

        self.plant_watered_datetime = None
        # get the datetime of the most recent plant watering from file
        if os.path.exists(self.data_file_name):
            print(f"[PLANT MONITOR] file name: {self.data_file_name} exists") 
            
            file_content_list = self.file_ops.read_file().split('\n')
            for line in file_content_list[::-1]:     
                # skip last line if its blank
                if line:
                    print("[PLANT MONITOR] line:", line)
                    self.plant_watered_datetime = datetime.fromisoformat(line)
                    break
            else:
                print("[PLANT MONITOR] data file is empty")
        else:
            print(f"[PLANT MONITOR] file name: {self.data_file_name} doesn't exist")

        print(f"[PLANT MONITOR] plant watered datetime: {self.plant_watered_datetime}")

        # -- message area ------------------------------------------------------
        fr = tk.Frame(
            self.plant_monitor, 
        )
        fr.grid(column=0, row=0, sticky=tk.NSEW)

        water_reminder_label = tk.Label(fr, text=f"Plant last watered at: {self.plant_watered_datetime}", font=("Arial", 18))
        water_reminder_label.pack(pady=(20, 0))

        time_since_plant_watered_label = tk.Label(fr, text="Plant not watered for (HH:MM:SS)", font=("Arial", 18))
        time_since_plant_watered_label.pack(pady=(20, 0))

        time_since_plant_watered_timer_label = tk.Label(fr, text="--:--:--", font=("Arial",72))
        time_since_plant_watered_timer_label.pack(pady=(20, 0))

        plant_watered_button = tk.Button(fr, text="Water Plant", command=lambda water_reminder_label: self.update_plant_watered_datetime(water_reminder_label))
        plant_watered_button.pack(pady=(20, 0))

        # -- file display area -------------------------------------------------
        file_display_listbox = tk.Listbox(self.plant_monitor)
        file_display_listbox.grid(column=1, row=0, sticky='nsew')

        # -- events ------------------------------------------------------------
        self.update_file_display(file_display_listbox)
        self.update_time_since_plant_watered(fr, time_since_plant_watered_timer_label)

    def update_file_display(self, file_display):
        '''
        PLANT MONITOR FUNCTION
        '''
        file_content_list = self.file_ops.read_file().split('\n')
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

    def update_time_since_plant_watered(self, frame, time_since_plant_watered_timer_label):
        '''
        PLANT MONITOR FUNCTION
        '''
        if not self.plant_watered_datetime:
            frame.after(1000, self.update_time_since_plant_watered, frame, time_since_plant_watered_timer_label)
            return

        diff = datetime.now() - self.plant_watered_datetime
        diff_seconds = int(diff.total_seconds())
        h = diff_seconds//3600
        m = (diff_seconds%3600)//60
        s = diff_seconds%60
        msg = f"{h:02}:{m:02}:{s:02}"
        #print(f"time difference: {diff}, {diff_seconds}, {msg}")
        time_since_plant_watered_timer_label.config(text=f"{msg}")

        frame.after(1000, self.update_time_since_plant_watered, frame, time_since_plant_watered_timer_label)
    
    def update_plant_watered_datetime(self, water_reminder_label):
        '''
        PLANT MONITOR FUNCTION
        '''
        # instead of displaying the current time, display the time in hours since last watering, or display that information in addition to date of last watering
        self.plant_watered_datetime = datetime.now()
        msg = self.plant_watered_datetime.strftime("%Y-%m-%d %H:%M:%S")
        water_reminder_label.config(text=f"Plant last watered at: {msg}")
        self.file_ops.append_line(msg+'\n')

        #self.update_file_display()

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

def update_label():
    # TODO
    # make this event based not timer based
    W = root.winfo_width()
    H = root.winfo_height()
    msg = f"screen resolution: {W} x {H}"
    screen_info_label.config(text=msg)
    root.after(1000, update_label)

def button_cb(channel):
    print(f"button pressed, cb arg: {channel}")
    update_plant_watered_datetime()
# ==============================================================================
# MAIN
# ==============================================================================

if 0:
    data_file_name = "data.txt"
    file_ops = FileHandler(data_file_name)

root = tk.Tk()
root.title("DesktopDisplayApp_v2")
root.geometry("1000x500")
root.resizable(width=False, height=False)
my_app_instance = MainFrame(root)
#root.configure(bg='blue')


if 0:
    draw_widgets()

    root.columnconfigure(1, weight=1)
    root.rowconfigure(0, weight=1)

# Frame 1
    frame1 = tk.Frame(root)
    frame1.configure(bg="lightblue")
    frame1.grid(row=0, column=1, sticky="nsew")

    date = datetime.today()
    date_label = tk.Label(frame1, text=f"{date}")
    date_label.pack(fill="x")

    screen_info_label = tk.Label(frame1, text="screen_resolution: NaN")
    screen_info_label.pack(side="bottom", fill="x")

    button_pin = 11 # gpio 17

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(button_pin, GPIO.RISING, callback=button_cb, bouncetime=1000)

# -- app initializations -------------------------------------------------------

    update_file_display()

    root.after(1000, update_label)
    root.after(1000, update_time_since_plant_watered)

root.mainloop()

if 0:
    print("GPIO.cleanup()")
    GPIO.cleanup()


