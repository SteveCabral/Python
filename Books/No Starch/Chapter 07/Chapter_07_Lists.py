#create two lists for confirmed and unconfirmed users
unconfirmed_users = ['alice', 'brian', 'candace']
confirmed_users = []

#move each 'verified' user to the confirmed user list
while unconfirmed_users:
	current_user = unconfirmed_users.pop()  #remove a user from unconfirmed list
	
	print(f"Verifying user: {current_user.title()}")
	confirmed_users.append(current_user)	#store user in confirmed list

#display all confirmed users
print("\nThe following users have been confirmed:")
for confirmed_user in confirmed_users:
	print(confirmed_user.title())
