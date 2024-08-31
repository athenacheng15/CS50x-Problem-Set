#include "../cs50.h"
#include <ctype.h>
#include <stdio.h>
#include <string.h>

bool validate_key(string key);
string encrypt(string plaintext, string key);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    string key = argv[1];
    if (!validate_key(key))
    {
        printf("Key must contain 26 characters, each only once.\n");
        return 1;
    }

    string plaintext = get_string("plaintext: ");
    string ciphertext = encrypt(plaintext, key);
    printf("ciphertext: %s\n", ciphertext);

    return 0;
}

bool validate_key(string key)
{
    int length = strlen(key);
    if (length != 26)
    {
        return false;
    }

    bool appeared[26] = {false};

    for (int i = 0; i < length; i++)
    {
        if (!isalpha(key[i]))
        {
            return false;
        }

        int index = toupper(key[i]) - 'A';

        if (appeared[index])
        {
            return false;
        }

        appeared[index] = true;
    }

    return true;
}

string encrypt(string plaintext, string key)
{
    int length = strlen(plaintext);
    string ciphertext = plaintext;

    for (int i = 0; i < length; i++)
    {
        if (isalpha(plaintext[i]))
        {
            bool is_upper = isupper(plaintext[i]);
            int index = toupper(plaintext[i]) - 'A';

            ciphertext[i] = is_upper ? toupper(key[index]) : tolower(key[index]);
        }
        else
        {
            ciphertext[i] = plaintext[i];
        }
    }

    return ciphertext;
}
