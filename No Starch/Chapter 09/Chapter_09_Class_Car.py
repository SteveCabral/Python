from Car import Car, ElectricCar

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
my_leaf.battery.describe_battery()
my_leaf.battery.get_range()




my_new_car.read_odometer	# DO NOT CALL a class method like this without the parentheses since it will not throw an error but nothing happens