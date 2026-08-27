# Assignment 1: Converter and Pixel System

**Author:** Ethan Brothers  
**Course:** CS 240  
**Module:** Module 1: Information as Bits

## Overview

This project contains multiple programs that demonstrate how information can be represented using bits, number bases, ASCII values, and pixel data.

The assignment includes:

1. An ASCII-to-decimal converter
2. A number-base converter
3. An image-to-pixel-value converter
4. A pixel-value-to-image converter
5. Automatic testing for normal and boundary cases

## How to Run

Run the main demonstration program:

```bash
python Demo.py
```

The demo provides a menu that allows each program to be run individually or tested automatically.

## Requirements

This project uses the Python `Pillow` library for image processing.

If Pillow is not already installed, `Demo.py` will attempt to install it automatically.

Dependencies can also be installed manually using:

```bash
pip install -r requirements.txt
```

The `requirements.txt` file contains:

```text
Pillow
```

## Files

### `Demo.py`

Main demonstration program.

- Provides access to all assignment programs
- Runs automatic tests
- Tests random normal values
- Tests required boundary cases

### `ASCII_to_Decimal.py`

Converts ASCII characters and strings into decimal ASCII values.

### `Number_Converter.py`

Converts numbers between:

- Binary
- Decimal
- Octal
- Hexadecimal

The converter also demonstrates 8-bit two's-complement representation for negative values.

### `Image_To_Pixel_Values.py`

Reads an image and converts its RGB pixel values into a custom Pixel Value File (`.pvf`).

The PVF file contains:

- File format identifier
- Image width
- Image height
- RGB values for each pixel

### `Pixel_Values_to_Image.py`

Reads a `.pvf` file and reconstructs the original image using the stored RGB pixel values.

## Automatic Testing

The automatic test option in `Demo.py` tests both normal and boundary cases.

### ASCII Tests

Random characters or strings are generated and passed directly to the ASCII-to-decimal converter.

### Number Converter Tests

The program generates random values within the supported range and converts them to each number base.

The required boundary tests include:

| Test | Value |
|---|---:|
| Zero | `0` |
| Largest 8-bit unsigned value | `255` |
| Negative two's-complement value | `-5` |

For example, `-5` represented using 8-bit two's complement is:

```text
Binary:      11111011
Decimal:     -5
Octal:       373
Hexadecimal: FB
```

## Custom PVF Format

The image programs use a custom `.pvf` file format.

Example:

```text
PVF1
Width: 3
Height: 2
255,0,0 0,255,0 0,0,255
255,255,255 0,0,0 128,128,128
```

Each RGB pixel is represented as:

```text
red,green,blue
```

## Output Folders

Generated pixel-value files are saved in:

```text
3-Output
```

Images reconstructed from `.pvf` files are saved in:

```text
4-Output
```

### Sources

- W3Schools. "Python File Handling."
  https://www.w3schools.com/python/python_file_handling.asp

- Python Software Foundation. "Reading and Writing Files."
  https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files

- Python Software Foundation. "Built-in Functions."
  https://docs.python.org/3/library/functions.html

- GeeksforGeeks. "Number System in Python."
  https://www.geeksforgeeks.org/python/number-system-in-python/

- Pillow Documentation. "Image Module."
  https://pillow.readthedocs.io/en/stable/reference/Image.html

- GeeksforGeeks. "Python Pillow - Working with Images."
  https://www.geeksforgeeks.org/python/python-pillow-working-with-images/

- GeeksforGeeks. "Python - Ways to Convert List of ASCII Values to String."
  https://www.geeksforgeeks.org/python/python-ways-to-convert-list-of-ascii-value-to-string/

All submitted source code was reviewed and understood before submission.