class Dog:

	def __init__(self, name, age):
		self.name = name
		self.age = age

	def sit(self):
		msg_sit = f"{self.name} is now sitting."
		print(msg_sit)


	def roll_over(self):
		print(f"{self.name} rolled over.")
		#print(msg_sit)	#this will fail since msg_sit is defined in another function vs the class __init__ constructor function


my_dog = Dog('willie', 6)

print(f"My dog's name is {my_dog.name} and is {my_dog.age} years old.")
my_dog.sit()
my_dog.roll_over()