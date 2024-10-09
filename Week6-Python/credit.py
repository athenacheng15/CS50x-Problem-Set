def validate_card(num):
    sum = 0
    digit_count = 0

    # Loop through each digit of the number from right to left
    while num > 0:
        digit = num % 10

        # If it's an odd position (from the right), just add the digit
        if digit_count % 2 == 0:
            sum += digit
        else:
            # If it's an even position, double the digit and add both digits
            doubled = digit * 2
            sum += (doubled // 10) + (doubled % 10)

        num //= 10  # Move to the next digit
        digit_count += 1

    # If the sum is divisible by 10, the card is valid
    return sum % 10 == 0


def print_card_type(number):
    length = len(str(number))  # Get the length of the credit card number
    first_two_digits = int(str(number)[:2])  # Get the first two digits as an integer

    if length == 15 and (first_two_digits == 34 or first_two_digits == 37):
        print("AMEX")
    elif length == 16 and (51 <= first_two_digits <= 55):
        print("MASTERCARD")
    elif (length == 13 or length == 16) and (first_two_digits // 10 == 4):
        print("VISA")
    else:
        print("INVALID")


def main():
    number = int(input("Input Card Number: "))

    if validate_card(number):
        print_card_type(number)
    else:
        print("INVALID")


if __name__ == "__main__":
    main()
