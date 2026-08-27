# Demonstrates and tests Assignment 1: Converter and Pixel System

# Author: Ethan Brothers
# Date: 2026-08-27

import random
import string
import subprocess
import sys

import ASCII_to_Decimal
import Number_Converter


def check_requirements():
    try:
        import PIL
        return True

    except ImportError:
        print("\nPillow is not installed.")
        print("Attempting to install Pillow...\n")

        try:
            subprocess.check_call([
                sys.executable,
                "-m",
                "pip",
                "install",
                "Pillow"
            ])

            print("\nPillow installed successfully!\n")
            return True

        except subprocess.CalledProcessError:
            print("\nERROR: Pillow could not be installed.")
            print("Please install requirements.txt using:")
            print("\n    pip install -r requirements.txt\n")
            return False


def test_ascii_converter():
    print("\n==========================================")
    print("ASCII TO DECIMAL TESTS")
    print("==========================================")

    # Generate 3 random printable ASCII characters
    for test in range(1, 4):
        characters = string.ascii_letters + string.digits

        if random.choice([True, False]):
            # Single character
            testValue = random.choice(characters)
        else:
            # Random string from 2 to 10 characters
            stringLength = random.randint(1, 10)
            testValue = "".join(
                random.choices(characters, k=stringLength)
            )

        print(f"\nTest {test}")
        print(f"Testing value: {testValue}")

        decimalValue = ASCII_to_Decimal.ascii_to_decimal(testValue)
        print(f"Decimal value: {decimalValue}")


def test_number_converter():
    print("\n==========================================")
    print("NUMBER BASE CONVERTER TESTS")
    print("==========================================")

    print("\n--- Random Tests ---")

    # Test 3 random values within an 8-bit unsigned range
    for test in range(1, 4):
        number = random.randint(1, 254)

        print(f"\nRandom Test {test}")
        Number_Converter.number_converter(number, 5)

    print("\n==========================================")
    print("REQUIRED BOUNDARY TESTS")
    print("==========================================")

    print("\nBoundary Test 1: Zero")
    Number_Converter.number_converter(0, 5)

    print("\nBoundary Test 2: Largest 8-bit Unsigned Value")
    Number_Converter.number_converter(255, 5)

    print("\nBoundary Test 3: Negative Two's-Complement Value")
    Number_Converter.number_converter(-5, 5)


def run_automatic_tests():
    print("\n==========================================")
    print("AUTOMATIC ASSIGNMENT TESTS")
    print("==========================================")

    test_ascii_converter()
    test_number_converter()

    print("\n==========================================")
    print("AUTOMATIC TESTING COMPLETE")
    print("==========================================")
    input("\nPress Enter to return to the main menu...")


def main():
    if not check_requirements():
        return

    # These files require Pillow
    import Image_To_Pixel_Values
    import Pixel_Values_to_Image

    while True:
        print("\n==========================================")
        print("Assignment 1: Converter and Pixel System")
        print("==========================================")

        print("\n1. Run Automatic Tests")
        print("2. ASCII to Decimal Converter")
        print("3. Number Base Converter")
        print("4. Image to Pixel Values")
        print("5. Pixel Values to Image")
        print("0. Exit")

        choice = input("\nSelect an option: ")

        if choice == "1":
            run_automatic_tests()

        elif choice == "2":
            print("\n--- ASCII to Decimal Converter ---\n")
            ASCII_to_Decimal.main()

        elif choice == "3":
            print("\n--- Number Base Converter ---\n")
            Number_Converter.main()

        elif choice == "4":
            print("\n--- Image to Pixel Values ---\n")
            Image_To_Pixel_Values.main()

        elif choice == "5":
            print("\n--- Pixel Values to Image ---\n")
            Pixel_Values_to_Image.main()

        elif choice == "0":
            print("\nDemo complete.")
            break

        else:
            print("\nInvalid selection. Please enter 0 through 5.")


if __name__ == "__main__":
    main()