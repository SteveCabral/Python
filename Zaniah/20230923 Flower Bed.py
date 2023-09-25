# import math module so that I can use math in my program
import math

# HELPER FUNCTIONS
# welcomes the user to my program
def welcome():
    print("Welcome to my Garden Plot Calculator")
    print("Note, all calculations are in feet")


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
   

# main task controls the execution flow of the garden soil calculator program
def main():
    # welcome the user
    welcome() 

    # get garden length, fountain radius, and flower bed depth
    garden_length = float(input("Please enter the length of one of the sides of the garden: "))
    print(f"You entered {garden_length}")
    fountain_radius = float(input("Please enter the radius of the fountain: "))
    print(f"You entered {fountain_radius}")    
    depth = float(input("Please enter the depth of the flower bed: "))
    print(f"You entered {depth}")
    
    # calculate area of garden
    garden_square_footage = garden_area(garden_length)
    fountain_square_footage = fountain_area(fountain_radius)
    flower_bed_square_footage = bed_area(garden_square_footage, fountain_square_footage)
    cubic_feet_of_soil = soil_volume(flower_bed_square_footage, depth)
    
    # display area of garden
    print(f"The total square footage of the garden is {garden_square_footage}")
    print(f"The square footage of the fountain is {fountain_square_footage}") #12.6
    print(f"The square footage of the flower bed is {flower_bed_square_footage}") #87.4
    print(f"The flower bed needs {cubic_feet_of_soil} cubic feet of soil") #39.3


# After you define your helper functions and the main function, don't forget to include a call to it afterwards:
main()