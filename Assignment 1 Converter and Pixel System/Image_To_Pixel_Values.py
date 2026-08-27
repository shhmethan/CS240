# Write a program that reads an image and prints its pixel values.

# Author: Ethan Brothers
# Date: 2026-08-26

from tkinter import Tk
from tkinter.filedialog import askopenfilename
from pathlib import Path
from PIL import Image

projectFolder = Path(__file__).resolve().parent
outputPath = projectFolder / "3-Output"


def image_to_pixel_values(image):
    imagePath = Path(image)
    outputFile = outputPath / f"{imagePath.stem}.pvf"

    try:
        outputPath.mkdir(exist_ok=True)

        with Image.open(image) as selectedImage:
            rgbImage = selectedImage.convert("RGB")

            width, height = rgbImage.size
            extension = imagePath.suffix.lower()

            with open(outputFile, "w") as f:
                f.write("PVF1\n")
                f.write(f"Extension: {extension}\n")
                f.write(f"Width: {width}\n")
                f.write(f"Height: {height}\n")

                for y in range(height):
                    row = []

                    for x in range(width):
                        red, green, blue = rgbImage.getpixel((x, y))
                        row.append(f"{red},{green},{blue}")

                    f.write(" ".join(row) + "\n")

        print(f"Pixel values saved to {outputFile}")

    except Exception as e:
        print(f"Error reading the image: {e}")



def main():
    root = Tk()
    root.withdraw()

    root.attributes("-topmost", True)

    image_file = askopenfilename(
        title="Select an image",
        filetypes=[
            ("Image files", "*.png *.jpg *.jpeg *.bmp"),
        ]
    )

    if image_file == "":
        print("No image was selected.")
    else:
        print("Selected:", image_file)
        image_to_pixel_values(image_file)


if __name__ == "__main__":
    main()