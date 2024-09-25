#include <cs50.h>
#include <stdio.h>

bool validate_card(long num);
void print_card_type(long number);

int main(void)
{
    long number = get_long("Input Card Number: ");
    if (validate_card(number))
    {
        print_card_type(number);
    }
    else
    {
        printf("INVALID\n");
    }
}

// validate card number
bool validate_card(long num)
{
    int sum = 0;
    int digit_count = 0;

    for (long n = num; n > 0; n /= 10)
    {
        int digit = n % 10;

        if (digit_count % 2 == 0) // If it is an odd number of digits (counting from the right)
        {
            sum += digit;
        }
        else
        {
            int doubled = digit * 2;
            sum += (doubled / 10) + (doubled % 10);
        }

        digit_count++;
    }

    return sum % 10 == 0;
}

// Determine and output the credit card type
void print_card_type(long number)
{
    int length = 0; // Get the length of the credit card number
    long temp = number;

    while (temp > 0)
    {
        temp /= 10;
        length++;
    }

    long first_two_digits = number;
    while (first_two_digits >= 100)
    {
        first_two_digits /= 10;
    }

    if (length == 15 && (first_two_digits == 34 || first_two_digits == 37))
    {
        printf("AMEX\n");
    }
    else if (length == 16 && (first_two_digits >= 51 && first_two_digits <= 55))
    {
        printf("MASTERCARD\n");
    }
    else if ((length == 13 || length == 16) && (first_two_digits / 10 == 4))
    {
        printf("VISA\n");
    }
    else
    {
        printf("INVALID\n");
    }
}
