# Build a number-base converter supporting binary, decimal, octal, and hexadecimal.

# Author: Ethan Brothers
# Date: 2026-08-26

def number_converter(inputNumber, base):
    outputNumber = 0
    match base:
        case 1:
            outputNumber = bin(inputNumber)
        case 2:
            outputNumber = inputNumber
        case 3:
            outputNumber = oct(inputNumber)
        case 4:
            outputNumber = hex(inputNumber)
        case 5:
            if inputNumber < 0:
                value = inputNumber & 0xFF

                outputNumberBin = format(value, "08b")
                outputNumberDec = inputNumber
                outputNumberOct = format(value, "o").upper()
                outputNumberHex = format(value, "02X")

            else:
                outputNumberBin = format(inputNumber, "08b")
                outputNumberDec = inputNumber
                outputNumberOct = oct(inputNumber)[2:].upper()
                outputNumberHex = hex(inputNumber)[2:].upper()

            print(f"\nThe original number was {inputNumber}\n\n"
                  f"Output number in different bases:\n"
                  f"Binary: {outputNumberBin}\n"
                  f"Decimal: {outputNumberDec}\n"
                  f"Octal: {outputNumberOct}\n"
                  f"Hexadecimal: {outputNumberHex}")
            return

    print(f"\nThe original number was {inputNumber} and the converted number is {outputNumber}")
    return

def main():

    print("Choose a number base:\n"
          "1. Binary\n"
          "2. Decimal\n"
          "3. Octal\n"
          "4. Hexadecimal\n"
          "5. All")

    base = int(input("Enter a number base: "))
    number = int(input("Enter a number: "))

    number_converter(number, base)

if __name__ == "__main__":
    main()