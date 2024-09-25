#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define BLOCK_SIZE 512

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        return 1;
    }

    // Open the memory card image file
    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        return 1;
    }

    BYTE buffer[BLOCK_SIZE];
    FILE *img = NULL;
    char filename[8];
    int file_count = 0;
    int found_jpeg = 0; // Indicate whether a JPEG has been found

    // Iterate the memory card image file
    while (fread(buffer, sizeof(BYTE), BLOCK_SIZE, file))
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            if (found_jpeg == 1) // JPEG already exist
            {
                fclose(img);
            }
            else
            {
                found_jpeg = 1;
            }

            // Create a new JPEG file
            // Formats an integer to be at least 3 digits long, padding with leading zeros if
            // necessary.
            sprintf(filename, "%03i.jpg", file_count);
            img = fopen(filename, "w");
            if (img == NULL)
            {
                printf("Could not create file %s.\n", filename);
                return 1;
            }

            file_count++;
        }

        if (found_jpeg == 1)
        {
            fwrite(buffer, sizeof(BYTE), BLOCK_SIZE, img);
        }
    }

    if (img != NULL)
    {
        fclose(img);
    }

    fclose(file);

    return 0;
}
