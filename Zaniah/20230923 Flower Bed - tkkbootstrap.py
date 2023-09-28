import tkinter as tk
import ttkbootstrap as ttk # replaces tkinter above for improved widgets

import math

# HELPER FUNCTIONS
def convert():
    mile_input = garden_length_entry.get()
    output_string.set(mile_input)

    # calculate area of garden
    garden_square_footage = garden_area(float(garden_length.get()))
    fountain_square_footage = float(fountain_radius.get())
    flower_bed_square_footage = bed_area(garden_square_footage, fountain_square_footage)
    cubic_feet_of_soil = soil_volume(flower_bed_square_footage, float(depth.get()))

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
# create a window
window = ttk.Window(
    title = "Flower Bed Calculator",
    themename = 'darkly',
    size = (480, 320),
    minsize = (480, 320))

# title
title_label = ttk.Label(master = window 
                        ,text = 'Flower Bed Calculator' 
                        ,font = 'Calibri 24 bold')
title_label.pack()

# input frame
input_frame = ttk.Frame(master = window)

garden_length_input_frame = ttk.Frame(master = window)
garden_length_label = ttk.Label(
    master = garden_length_input_frame,
    text =  "Please enter the length of one of the sides of the garden: ",
    font =  'Calibri 12')
garden_length_label.pack(side = 'left', padx = 5)
garden_length = tk.IntVar()
garden_length_entry = ttk.Entry(
    master = garden_length_input_frame, 
    textvariable = garden_length)
garden_length_entry.pack(side = 'left', padx = 10)
garden_length_input_frame.pack(pady = 10)

fountain_radius_input_frame = ttk.Frame(master = window)
fountain_radius_label = ttk.Label(
    master = fountain_radius_input_frame,
    text =  "Please enter the radius of the fountain: ",
    font =  'Calibri 12')
fountain_radius_label.pack(side = 'left', padx = 5)
fountain_radius = tk.IntVar()
fountain_radius_entry = ttk.Entry(
    master = fountain_radius_input_frame, 
    textvariable = fountain_radius)
fountain_radius_entry.pack(side = 'left', padx = 10)
fountain_radius_input_frame.pack(pady = 10)

depth_input_frame = ttk.Frame(master = window)
depth_label = ttk.Label(
    master = depth_input_frame,
    text =  "Please enter the depth of the flower bed: ",
    font =  'Calibri 12')
depth_label.pack(side = 'left', padx = 5)
depth = tk.IntVar()
depth_entry = ttk.Entry(
    master = depth_input_frame, 
    textvariable = depth)
depth_entry.pack(side = 'left', padx = 10)
depth_input_frame.pack(pady = 10)

button = ttk.Button(
    master = input_frame,
    text = 'Convert',
    command = convert)
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

garden_square_footage_output_string = tk.StringVar()
garden_square_footage_output_label = ttk.Label(
    master = window, 
    text = 'garden_square_footage_output_label', 
    font = 'Calibri 14', 
    textvariable = garden_square_footage_output_string)
garden_square_footage_output_label.pack(pady = 5)

fountain_square_footage_output_string = tk.StringVar()
fountain_square_footage_output_label = ttk.Label(
    master = window, 
    text = 'fountain_square_footage_output_label', 
    font = 'Calibri 14', 
    textvariable = fountain_square_footage_output_string)
fountain_square_footage_output_label.pack(pady = 5)

flower_bed_square_footage_output_string = tk.StringVar()
flower_bed_square_footage_output_label = ttk.Label(
    master = window, 
    text = 'flower_bed_square_footage_output_label', 
    font = 'Calibri 14', 
    textvariable = flower_bed_square_footage_output_string)
flower_bed_square_footage_output_label.pack(pady = 5)

cubic_feet_of_soil_output_string = tk.StringVar()
cubic_feet_of_soil_output_label = ttk.Label(
    master = window, 
    text = 'cubic_feet_of_soil_output_label', 
    font = 'Calibri 14', 
    textvariable = cubic_feet_of_soil_output_string)
cubic_feet_of_soil_output_label.pack(pady = 5)


# main task controls the execution flow of the garden soil calculator program
def main():
    # run to see the window
    window.mainloop()

# call main to execute Python program
main()