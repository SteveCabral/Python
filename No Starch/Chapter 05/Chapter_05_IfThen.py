#Chapter 05 - If Then

#page 76 - A Simple Example

MyCar = "Audi"
cars = ['audi', 'bmw', 'subaru', 'toyota']

for car in cars:
    if car == 'bmw':
        print(car.upper())
    else:
        print(car.title())

    if car == 'audi':
        if car == MyCar:
            print(car + " = " + MyCar)
        else:
            print(car + " != " + MyCar)


#Checking Whether a Value Is or Not in a List
WifeCar = 'honda'

if WifeCar in cars:
    print(WifeCar + " is in " + cars)

if WifeCar not in cars:
    print(WifeCar + " is not in cars list")


#boolean expressions - variables testing
iHateBadFood = True

if iHateBadFood:
    print("I hate bad food")

#one more change

