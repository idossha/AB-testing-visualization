import os
import time

import PyPDF2
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.colors import black, white
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


def sbs(dirs, output_pdf, target_size=None):
    """
    :param dirs: List of directories containing PNG, JPG, JPEG files.
    :param output_pdf: Output PDF file name.
    :param page_titles: List of titles for each PDF page.
    :param target_size: Optional tuple (width, height) to resize each individual image.
    """
    start_time = time.time()  # Start timing
    # Initialize list for the paired images and file names from each directory
    paired_images = []
    all_files = []

    # Process each directory
    for dir in dirs:
        files = [f for f in os.listdir(dir) if f.endswith((".png", ".jpg", ".jpeg"))]
        files.sort()
        all_files.append(files)

    # Check if any directory is empty
    if any(not files for files in all_files):
        print("PNG or JPEG files missing in one or more directories.")
        return

    # Process and pair the images
    for i, files in enumerate(zip(*all_files)):
        imgs = []
        for dir, file in zip(dirs, files):
            img_path = os.path.join(dir, file)
            img = Image.open(img_path)

            if target_size:
                img = img.resize(target_size, Image.Resampling.LANCZOS)

            img = img.convert("RGB")
            imgs.append(img)

        # Calculate dimensions for the new image
        total_width = sum(img.width for img in imgs)
        max_height = max(img.height for img in imgs)

        # Create a new image and paste the individual images
        new_img = Image.new("RGB", (total_width, max_height))
        x_offset = 0
        for img in imgs:
            new_img.paste(img, (x_offset, 0))
            x_offset += img.width

        paired_images.append(new_img)

    # Check if there are images to be saved in the PDF
    if not paired_images:
        print("No images to create PDF.")
        return

    # Save all paired images to a PDF
    paired_images[0].save(output_pdf, save_all=True, append_images=paired_images[1:])
    print(f"PDF created successfully: {output_pdf}")

    end_time = time.time()  # End timing
    print(f"The function took {end_time - start_time} seconds to run.")


def ontop(input_path, output_path, images_per_page, target_size=None):
    """
    :param dir_path: Directory where images images are stored.
    :param output_pdf: Output PDF file name.
    :param images_per_page: Number of images to stack on each page of the PDF.
    :param target_size: Optional tuple (width, height) to resize each individual image.
    """
    start_time = time.time()  # Start timing

    # Get all PNG files in the directory
    files = [f for f in os.listdir(input_path) if f.endswith(".png")]
    files.sort()  # Sort files to maintain order

    if not files:
        print("No PNG files found in the directory.")
        return

    # Initialize list for the stacked images
    stacked_images_pages = []

    for i in range(0, len(files), images_per_page):
        imgs = [
            Image.open(os.path.join(input_path, file))
            for file in files[i : i + images_per_page]
        ]

        if target_size:
            imgs = [img.resize(target_size, Image.Resampling.LANCZOS) for img in imgs]

        # Convert images to RGB
        imgs = [img.convert("RGB") for img in imgs]

        # Calculate dimensions for the new stacked image
        max_width = max(img.width for img in imgs)
        total_height = sum(img.height for img in imgs)

        # Create a new image for the stacked images
        new_img = Image.new("RGB", (max_width, total_height))
        y_offset = 0
        for img in imgs:
            new_img.paste(img, (0, y_offset))
            y_offset += img.height

        stacked_images_pages.append(new_img)

    # Check if there are images to be saved in the PDF
    if not stacked_images_pages:
        print("No images to create PDF.")
        return

    # Save all stacked images to a PDF
    stacked_images_pages[0].save(
        output_path, save_all=True, append_images=stacked_images_pages[1:]
    )
    print(f"PDF created successfully: {output_path}")

    end_time = time.time()  # End timing
    print(f"The function took {end_time - start_time} seconds to run.")


# Example function calls (if this module is run as a script)
if __name__ == "__main__":
    # sbs example usage
    dirs = ["/path/to/dir1", "/path/to/dir2"]
    output_pdf = "/path/to/output.pdf"
    sbs(dirs, output_pdf, target_size=(1000, 1000))

    # ontop example usage
    input_path = "/path/to/images"
    output_path = "/path/to/stacked_images.pdf"
    images_per_page = 3
    ontop(input_path, output_path, images_per_page)
