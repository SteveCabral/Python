#FUNCTIONS:
def VerifyUser(key, value):
	print(f"\nChecking user: {key}")
	if value == False:
		users[key] = True
		print(f"\t{key.title()} was not verified ({value}) but has been verified.\n")
	else:
		print(f"\t{key.title()} was already verified ({value}).\n")


#create two lists for confirmed and unconfirmed users
users = {'alice': False, 'brian': True, 'candace': False}


#confirm users
print(f"Initial users dictionary:\n{users}")
for k, v in users.items():
	VerifyUser(k, v) #call function using positional arguments

print(f"\nAfter first verify:\n{users}")

#add david as user:
users['david'] = False
print(f"\nAfter adding david:\n{users}")

#confirm users again wih
for k, v in users.items():
	VerifyUser(key = k, value = v) #call function using keyword arguments

print(f"\nFinal pring of users:\n{users}")



