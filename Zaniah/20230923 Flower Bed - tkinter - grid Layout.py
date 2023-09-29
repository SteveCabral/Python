import tkinter as tk
from tkinter import ttk

import math

# HELPER FUNCTIONS
def convert():
    # calculate area of garden
    garden_square_footage = garden_area(garden_length.get())
    fountain_square_footage = fountain_radius.get()
    flower_bed_square_footage = bed_area(garden_square_footage, fountain_square_footage)
    cubic_feet_of_soil = soil_volume(flower_bed_square_footage, depth.get())

    # update output labels
    garden_square_footage_output_string.set(f"The total square footage of the garden is {garden_square_footage}")
    fountain_square_footage_output_string.set(f"The square footage of the fountain is {fountain_square_footage}")
    flower_bed_square_footage_output_string.set(f"The square footage of the flower bed is {flower_bed_square_footage}")
    cubic_feet_of_soil_output_string.set(f"The flower bed needs {cubic_feet_of_soil} cubic feet of soil")
    


# returns the area of the garden
def garden_area(garden_length):
    return round(garden_length**2, 1)   # round all calculations to 1 decimal place

# returns area of the fountain
def fountain_area(fountain_radius):
    # Use the math module for the value of π
    return round(math.pi * (fountain_radius**2), 1) 

# returns the square footage of bed
def bed_area(garden_area, fountain_area):
    return round(garden_area - fountain_area, 1)    # Additionally, round all calculations to 1 decimal place.

# calculates the volume
def soil_volume(bed_area, depth):
    return round(bed_area * depth, 1) # Additionally, round all calculations to 1 decimal place.

# GUI INTERFACE:
# app window
window = tk.Tk()
window.title("Flower Bed Calculator")
#window.geometry("640x480") # set window width x height

# app title
title_label = ttk.Label(master = window 
                        ,text = 'Welcome to my Garden Plot Calculator' 
                        ,font = 'Calibri 16 bold')
title_label.grid(row = 1, columnspan = 2, ipadx = 20)
note_label = ttk.Label(master = window 
                        ,text = 'Note, all calculations are in feet' 
                        ,font = 'Calibri 12 bold')
note_label.grid(row = 2, columnspan = 2)



# input frame
input_frame = ttk.Frame(master = window)
input_frame.grid(row = 3, columnspan = 2, ipadx = 5)
garden_length_label = ttk.Label(
    master = input_frame,
    text =  "Please enter the length of one of the sides of the garden: ",
    font =  'Calibri 12')
garden_length_label.grid(row = 1,column = 1, sticky = 'E')
garden_length = tk.DoubleVar()
garden_length_entry = ttk.Entry(
    master = input_frame, 
    textvariable = garden_length)
garden_length_entry.grid(row = 1,column = 2)



fountain_radius_label = ttk.Label(
    master = input_frame,
    text =  "Please enter the radius of the fountain: ",
    font =  'Calibri 12')
fountain_radius_label.grid(row = 2,column = 1, sticky = 'E')
fountain_radius = tk.DoubleVar()
fountain_radius_entry = ttk.Entry(
    master = input_frame, 
    textvariable = fountain_radius)
fountain_radius_entry.grid(row = 2,column = 2)


depth_label = ttk.Label(
    master = input_frame,
    text =  "Please enter the depth of the flower bed: ",
    font =  'Calibri 12')
depth_label.grid(row = 3,column = 1, sticky = 'E')
depth = tk.DoubleVar()
depth_entry = ttk.Entry(
    master = input_frame, 
    textvariable = depth)
depth_entry.grid(row = 3,column = 2)


button = ttk.Button(
    master = input_frame,
    text = 'Convert',
    command = convert)
button.grid(row = 4, columnspan = 3, sticky = "E")


# output
garden_square_footage_output_string = tk.StringVar()
garden_square_footage_output_label = ttk.Label(
    master = window, 
    text = 'garden_square_footage_output_label', 
    font = 'Calibri 14', 
    textvariable = garden_square_footage_output_string)
garden_square_footage_output_label.grid(row = 5, columnspan = 2)

fountain_square_footage_output_string = tk.StringVar()
fountain_square_footage_output_label = ttk.Label(
    master = window, 
    text = 'fountain_square_footage_output_label', 
    font = 'Calibri 14', 
    textvariable = fountain_square_footage_output_string)
fountain_square_footage_output_label.grid(row = 6, columnspan = 2)

flower_bed_square_footage_output_string = tk.StringVar()
flower_bed_square_footage_output_label = ttk.Label(
    master = window, 
    text = 'flower_bed_square_footage_output_label', 
    font = 'Calibri 14', 
    textvariable = flower_bed_square_footage_output_string)
flower_bed_square_footage_output_label.grid(row = 7, columnspan = 2)

cubic_feet_of_soil_output_string = tk.StringVar()
cubic_feet_of_soil_output_label = ttk.Label(
    master = window, 
    text = 'cubic_feet_of_soil_output_label', 
    font = 'Calibri 14', 
    textvariable = cubic_feet_of_soil_output_string)
cubic_feet_of_soil_output_label.grid(row = 8, columnspan = 2)


# main task controls the execution flow of the garden soil calculator program
def main():
    garden_length_entry.focus_set()
    garden_length_entry.select_range(0, tk.END)
    window.mainloop()


# call main to execute Python program
main()