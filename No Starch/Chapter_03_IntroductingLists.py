#Chapter 3 - Introducting Lists

#practice variables with whitespace
newline = '\n'
tab = '\t'
string = "Notes:" + newline + tab + "1. First Note" + newline + tab + "2. Second Note"

print(string)



#practice variable calling methods
myvariable = "steve cabral! 'where are you?'"

print(myvariable)
print("title(): " + myvariable.title())
print("upper(): " + myvariable.upper())
print("capitalize(): " + myvariable.capitalize())
print("casefold(): " + myvariable.casefold())
print("count('e'): " + str(myvariable.count("e")))
print('islower(): ' + str(myvariable.islower()))


number = 10 * 10 + 5 * 1
print("10 * 10 + 5 * 1 --> " + str(number))

number += 1
print("number += 1 --> " + str(number))

number. = 3 / 2
print("3 / 2 --> " + str(number))


people = ['Ann','Max','Ruchi','Taffiny']
print(people)
print(people[0])

print(people[-1]) #return lst item in list
print(people[-2]) #return lst item in list

