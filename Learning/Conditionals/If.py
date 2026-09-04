input_value = ''
while input_value != 'exit':
    input_value = input("Enter a number (or 'exit' to quit): ")
    if input_value.lower() == 'exit':
        print("Exiting the loop.")
        break
    try:
        number = float(input_value)
        if number > 0:
            print("The number is positive.")
        elif number < 0:
            print("The number is negative.")
        else:
            print("The number is zero.")
    except ValueError:
        print("That's not a valid number. Please enter a numeric value.")
