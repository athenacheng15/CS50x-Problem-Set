#include <cs50.h>
#include <stdio.h>

void print_hashes(int n);

int main(void)
{
    int height;

    do
    {
        height = get_int("Input height: ");
    }
    while (height < 1 || height > 8);

    for (int i = 1; i <= height; i++)
    {
        int space = height - i;

        printf("%*s", space, "");
        print_hashes(i);
        printf("  ");
        print_hashes(i);

        printf("\n");
    }
}

void print_hashes(int n)
{
    for (int i = 0; i < n; i++)
    {
        printf("#");
    }
}
