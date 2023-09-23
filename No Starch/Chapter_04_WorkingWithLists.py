#Chapter 04 - Working With Lists

Tab = '\t' #tab character

ColorList = ['Purple', 'Brown', 'Orange', 'Yellow', 'Red', 'Black', 'Green']


print("Print out " + str(len(ColorList)) + " colors from ColorList list:")
for Color in ColorList:
    print(Tab + Color)
    print(Tab + Tab + "retrieving next color...")
    #every line indented is part of the loop

#no longer indented so outside the loop
#is Color still in scope?
print("Check to see if Color is still in scope: " + Color)


#this line will throw an error since Python expects indented line after for statement (Uncomment to see error)
#for Color in ColorList:
#print("Bad code: " + Color)



#this code will loop through all lines indented even with multiple lines between them
for Color in ColorList:
    print("Color: " + Color)
    
    print("will this print?")



    print("what about this")





#unnecessary indents will throw an error (Uncomment to see error)
#Color = "Cyan"
#    print("unnecessary indent " + Color)





#here is an example of a list containing multiple items
MultiTypeList = [1, "Steve", 2, "Cabral"]
for MultiType in MultiTypeList:
    print(MultiType)



#here is an example of a list containing a list
ListOfLists = [ColorList, MultiTypeList]
for List in ListOfLists:
    print(List)


#if a list contains a list, changing the value in the list will reflect in the list containing the list
ColorList[0] = "Blue"

for List in ListOfLists:
    print(List)




#using range with a list (page 61)
for value in range(1,5):
    print(value)


#use the list() function to create a list from the range() function
SomeNumbers = list(range(1,11))
print(SomeNumbers)



#I will attempt to append a list to a list
ListOfLists.append(SomeNumbers)
print(ListOfLists)


#using range() to skip numbers (an interval)
even_numbers = list(range(2,11,2))
print(even_numbers)



#page 62
squares = []
for value in range(1,11):
    square = value**2
    squares.append(square)

print(squares)


squares = []
for value in range(1,11):
    squares.append(value**2)

print(squares)



#page 63
digits = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
print(digits)
print("min(digits) --> " + str(min(digits)))
print("max(digits) --> " + str(max(digits)))
print("sum(digits) --> " + str(sum(digits)))



#page 64 - list comprehension
squares = [value ** 2 for value in range(1,11)]
print(squares)


#page 65 - slicing
players = ['charles', 'martina', 'michael', 'florence', 'eli']
print(players[0:3])
print(players[2:-1])

print(players[:2])
print(players[2:])



#page 66 
for player in players[:3]:
    print(player.title())



#page 67
my_foods = ['pizza', 'falafel', 'carrot cake']
friend_foods = my_foods[:]

print("My favorite foods are:")
print(my_foods)

print("My friend's favorite foods are:")
print(friend_foods)

my_foods.append('cannoli')
friend_foods.append('ice cream')

print("My favorite foods are:")
print(my_foods)

print("My friend's favorite foods are:")
print(friend_foods)



#page 70 - tuples
dimensions = (200, 50)
print(dimensions[0])
print(dimensions[1])

for dimension in dimensions:
    print(dimension)

dimensions = (range(2, 21, 2))

for dimension in dimensions:
    print(dimension)

#notice when I print a tuple created using the range function that the declaration was printed
print(dimensions)    
