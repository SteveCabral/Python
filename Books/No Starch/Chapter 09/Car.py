"""A class that can be used to represent a car."""

class Battery:
	"""A simple attempt to model a battery for an electric car."""
	def __init__(self, battery_size=40):
		"""Initialize the battery's attributes."""
		self.battery_size = battery_size


	def describe_battery(self):
		"""Print a statement describing the battery size."""
		print(f"This car has a {self.battery_size}-kWh battery.")


	def get_range(self):
		"""Print a statement about the range this battery provides."""
		if self.battery_size == 40:
			range = 150
		elif self.battery_size == 65:
			range = 225
		
		print(f"This car can go about {range} miles on a full charge.")


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
	"""
	Initialize attributes of the parent class.
	Then initialize attributes specific to an electric car.
	"""
	def __init__ (self,make, model, year):
		super().__init__(make, model, year)
		self.battery = Battery()

	def describe_battery(self):
		print(f"This car has a {self.battery.battery_size}-kWh battery.")

	def fill_gas_tank(self):
		print("This is an electric vehicle... it does not have a gas tank.")
