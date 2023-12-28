#Book:      No Starch Press - Python Crash Course
#Chapter:   3 Introducing Lists

#here is how you create a list:
bicycles = ['trek', 'cannondale', 'redline', 'specialized']



#if you print a list, everything including brackets is shown
print( "print(bicycles) --> " + str(bicycles) )


#to print individual items, reference them as an array (zero-based)
print( "To print first item in bicycle list: print(bicycles[0]) --> " + bicycles[0] )
print( "To print last item in bicycle list: print(bicycles[-1]) --> " + bicycles[-1] )

message = "My first bicycle was a " + bicycles[0].title() + "."
print("print(message) --> " + message)


# 3-1. Names: Store the names of a few of your friends in a list called names. Print
# each person’s name by accessing each element in the list, one at a time.
friends = ['friend one', 'friend two', 'friend three', 'friend four', 'friend five']
print( "print(friend(0)) --> " + friends[0] )
print( "print(friend(1)) --> " + friends[1] )
print( "print(friend(2)) --> " + friends[2] )
print( "print(friend(3)) --> " + friends[3] )


#modifying a list item
friends[2] = "friend three (modified)"
print( "friend[2] was modified --> " + str(friends) )


#adding to a list
friends.append("friend appended")
print( "friend was appended --> " + str(friends) )

friends.insert(-1, "friend inserted at [-1]")
print( "friend inserted at [-1] --> " + str(friends) )



#Removing an Item Using the del Statement
del friends[-1]
print( "deleted friends[-1] --> " + str(friends) )


#removing an item using pop
popped_friend = friends.pop();

print( "popped_friend = friends.pop() --> " + popped_friend )
print ( "friends after pop --> " + str(friends) )


popped_friend = friends.pop(3)

print( "popped_friend = friends.pop(3) --> " + popped_friend )
print ( "friends after pop --> " + str(friends) )
