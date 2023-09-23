import math #import math module so that I can use math in my program

def welcome():#defined a function named welcome so that I can easily welcome the user to my program
    print("Welcome to my Garden plot calculator!")
    ("Note, all calculations are in feet")
   
def garden_length(garden) :#defined a function named garden length
    print(float(input("Enter the length of side one of your garden here: ")))
    print("You entered:",garden_length)
    garden_area = (garden_length**2) #finds the area of the garden

    return garden_area #returns the total area of the garden

def fountain_radius(fountain):
    print(float(input("Enter the radius of the fountain here: ")))  #asks the user for the radius of the fountain
    print("You entered:", fountain_radius) #echos the variable back to user
    fountain_area = math.pi * (fountain_radius**2) #finds area of the fountain
    return fountain_area#returns the square footage

def bed_area(depth):
    print(float(input("Enter the depth of the flower bed here: "))) #asks user for depth of flower bed
    print("You entered:",depth) #echos variable back to user
    bed_area=(garden_area-fountain_area) #returns the square footage of bed
    return bed_area#returns square footage

def soil_volume(soil):
    soil_volume=(bed_area*depth) #calculates the volume
    return soil_volume #returns the volume
   
def main(garden_area,fountain_area,bed_area,soil_volume):
    print(float("The total square footage of the garden is", garden_area)
    print(float("The square footage of the fountain is", fountain_area)
    print(float("The square footage of the flower bed is", bed_area)