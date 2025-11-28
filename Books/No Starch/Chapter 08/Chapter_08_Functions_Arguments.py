#FUNCTIONS:
def make_pizza(*toppings):	#the asterisk causes Python to create a tupple containing the arbitrary number of arguments
	print(f"toppings argument:{toppings}")
	for topping in toppings:
		print(f"\t- {topping}")
	print("\n")


make_pizza('pepperoni')
make_pizza("ham",'cheese')
make_pizza('mushrooms','green peppers','sausage')
make_pizza('mushrooms',2,'sausage',4)