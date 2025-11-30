# https://www.youtube.com/watch?v=mop6g-c5HEY&list=PLVsNqL_zRstHBRIB4JaYFeiC5UIv-Tq-l&index=4&t=122s

import tkinter as tk
#from tkinter import ttk # contains all of the widgets
import ttkbootstrap as ttk # replaces above for improved widgets

def convert():
    mile_input = entry_int.get()
    km_output = mile_input * 1.61
    output_string.set(km_output)

# create a window
window = ttk.Window(themename = 'darkly')   # OLD: window = tk.Tk()
window.title("Flower Bed Calculator")
window.geometry("480x320") # set window width x height

# title
title_label = ttk.Label(master = window \
                        ,text = 'Flower Bed Calculator' \
                        ,font = 'Calibri 24 bold')
title_label.pack()

# input frame
input_frame = ttk.Frame(master = window)
entry_int = tk.IntVar()
entry = ttk.Entry(
    master = input_frame, 
    textvariable = entry_int)
button = ttk.Button(
    master = input_frame,
    text = 'Convert',
    command = convert)
entry.pack(side = 'left', padx = 10)
button.pack(side = 'left')
input_frame.pack(pady = 10)

# output
output_string = tk.StringVar()
output_label = ttk.Label(
    master = window, 
    text = 'Output', 
    font = 'Calibri 14', 
    textvariable = output_string)
output_label.pack(pady = 5)


# run to see the window
window.mainloop()
