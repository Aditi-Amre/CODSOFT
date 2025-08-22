def simple_calculator():
    """
    A simple calculator that performs basic arithmetic operations.
    Prompts the user for two numbers and an operation choice.
    Returns the result of the calculation.
    """
    
    # Display a welcome message
    print("=" * 50)
    print("          SIMPLE PYTHON CALCULATOR")
    print("=" * 50)
    print("Available operations:")
    print("+ : Addition")
    print("- : Subtraction")
    print("* : Multiplication")
    print("/ : Division")
    print("% : Modulus (remainder)")
    print("^ : Exponentiation")
    print("=" * 50)
    
    try:
        # Get user input
        num1 = float(input("Enter the first number: "))
        operation = input("Enter the operation (+, -, *, /, %, ^): ")
        num2 = float(input("Enter the second number: "))
        
        # Perform the calculation based on the operation
        if operation == '+':
            result = num1 + num2
            print(f"\n{num1} + {num2} = {result}")
            
        elif operation == '-':
            result = num1 - num2
            print(f"\n{num1} - {num2} = {result}")
            
        elif operation == '*':
            result = num1 * num2
            print(f"\n{num1} * {num2} = {result}")
            
        elif operation == '/':
            if num2 == 0:
                print("\nError: Division by zero is not allowed!")
                return
            result = num1 / num2
            print(f"\n{num1} / {num2} = {result}")
            
        elif operation == '%':
            if num2 == 0:
                print("\nError: Division by zero is not allowed!")
                return
            result = num1 % num2
            print(f"\n{num1} % {num2} = {result}")
            
        elif operation == '^':
            result = num1 ** num2
            print(f"\n{num1} ^ {num2} = {result}")
            
        else:
            print("\nError: Invalid operation selected!")
            return
            
        # Display the result in a formatted way
        print("=" * 50)
        print(f"Result: {result}")
        print("=" * 50)
        
    except ValueError:
        print("\nError: Please enter valid numbers!")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

# Function to check if the user wants to perform another calculation
def main():
    while True:
        simple_calculator()
        
        # Ask if the user wants to perform another calculation
        another_calculation = input("\nDo you want to perform another calculation? (y/n): ").lower()
        if another_calculation != 'y':
            print("\nThank you for using the calculator. Goodbye!")
            break
        print("\n" + "=" * 50 + "\n")

# Run the calculator
if __name__ == "__main__":
    main()