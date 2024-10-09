# Prompt user for a valid height between 1 and 8
while True:
    try:
        levels = int(input("Height: "))
        if 1 <= levels <= 8:
            break
    except ValueError:
        pass


for current_level in range(levels):
    spaces = " " * (levels - current_level - 1)
    hashes = "#" * (current_level + 1)
    print(f"{spaces}{hashes}  {hashes}")
