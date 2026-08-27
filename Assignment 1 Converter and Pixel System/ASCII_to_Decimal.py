# Build an ASCII-to-decimal converter.

# Author: Ethan Brothers
# Date: 2026-08-26
def ascii_to_decimal(inputString):
    outputString = ""

    for i in inputString:
        if outputString != "":
            outputString += " "

        outputString += str(ord(i))

    return outputString

def main():
    inputString = input("Enter an ASCII code: ")
    decimal_value = ascii_to_decimal(inputString)
    print(f"The decimal value(s) of {inputString} is \"{decimal_value}\"")

if __name__ == "__main__":
    main()