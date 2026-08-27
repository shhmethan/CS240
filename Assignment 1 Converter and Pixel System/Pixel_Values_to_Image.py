# Write a program that consumes pixel values and creates an image.

# Author: Ethan Brothers
# Date: 2026-08-26

from tkinter import Tk
from tkinter.filedialog import askopenfilename
from pathlib import Path
from PIL import Image

projectFolder = Path(__file__).resolve().parent
outputPath = projectFolder / "4-Output"


def pixel_to_image(pixel):
    pixelPath = Path(pixel)

    try:
        outputPath.mkdir(exist_ok=True)

        with open(pixel, "r") as f:
            # Read file header
            fileType = f.readline().strip()

            if fileType != "PVF1":
                print("Invalid PVF file.")
                return

            extensionLine = f.readline().strip()
            widthLine = f.readline().strip()
            heightLine = f.readline().strip()

            extension = extensionLine.split(":")[1].strip()
            width = int(widthLine.split(":")[1].strip())
            height = int(heightLine.split(":")[1].strip())

            pixels = []

            for line in f:
                pixelValues = line.strip().split()

                for pixelValue in pixelValues:
                    red, green, blue = pixelValue.split(",")

                    pixels.append(
                        (
                            int(red),
                            int(green),
                            int(blue)
                        )
                    )

        expectedPixels = width * height

        if len(pixels) != expectedPixels:
            print("Error: Pixel count does not match image dimensions.")
            print(f"Expected: {expectedPixels}")
            print(f"Found: {len(pixels)}")
            return

        newImage = Image.new("RGB", (width, height))
        newImage.putdata(pixels)

        outputFile = outputPath / f"{pixelPath.stem}{extension}"

        newImage.save(outputFile)

        print(f"Image saved to {outputFile}")

    except Exception as e:
        print(f"Error reading the .PVF: {e}")


def main():
    root = Tk()
    root.withdraw()

    root.attributes("-topmost", True)

    pixel_file = askopenfilename(
        title="Select a file to convert",
        filetypes=[
            ("Pixel Value File", "*.pvf"),
            ("All files", "*.*")
        ]
    )

    if pixel_file == "":
        print("No file was selected.")
    else:
        print("Selected:", pixel_file)
        pixel_to_image(pixel_file)


if __name__ == "__main__":
    main()