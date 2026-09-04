while True:
    user_input = input("Enter a number (or 'exit' to quit): ")
    if user_input.lower() == 'exit':
        print("Exiting the loop.")
        break
    try:
        number = float(user_input)
        print(f"You entered: {number}")
    except ValueError:
        print("That's not a valid number. Please try again.")