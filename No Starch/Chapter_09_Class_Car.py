class Car:
	def __init__ (self,make, model, year):
		self.make = make
		self.model = model
		self.year = year
		self.odometer_reading = 0	#not passed as argument during instance creation by constructor
		self.gas_tank = 0

	def get_descriptive_name(self):
		long_name = f"{self.year} {self.make} {self.model}"
		return long_name.title()
	
	def read_odometer(self):
		print(f"This car has {self.odometer_reading} miles on it.")
	
	def update_odometer(self, mileage):
		if mileage >= self.odometer_reading:
			self.odometer_reading = mileage
		else:
			print(f"Attempting to change the odometer from {self.odometer_reading} to {mileage}. You can't roll back an odometer!")

	def increment_odometer(self, miles):
		self.odometer_reading += miles
		print(f"Incremented the odometer {miles}. The odometer is now {self.odometer_reading}.")

	def fill_gas_tank(self, gallons):
		self.gas_tank += gallons
		print(f"Added {gallons} gallons to the gas tank bringing the total gallons to {self.gas_tank}.")


class ElectricCar(Car):
	def __init__ (self,make, model, year):
		super().__init__(make, model, year)
		self.battery_size = 40

	def describe_battery(self):
		print(f"This car has a {self.battery_size}-kWh battery.")

	def fill_gas_tank(self):
		print("This is an electric vehicle... it does not have a gas tank.")


my_new_car = Car('audi', 'a4', 2024)
print(my_new_car.get_descriptive_name())
my_new_car.odometer_reading = 23
my_new_car.read_odometer()
my_new_car.update_odometer(123)
my_new_car.read_odometer()
my_new_car.update_odometer(45)
my_new_car.increment_odometer(23_500)
my_new_car.read_odometer()
my_new_car.fill_gas_tank(24)


my_leaf = ElectricCar('nissan','leaf',2024)
print(my_leaf.get_descriptive_name())
my_leaf.describe_battery()
my_leaf.fill_gas_tank()



my_new_car.read_odometer	# DO NOT CALL a class method like this without the parentheses since it will not throw an error but nothing happens