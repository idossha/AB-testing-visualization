from PIL import Image, ImageDraw, ImageFont
import os

def draw_title_on_image(image, title, position=(10, 10), font=None, font_size=40, color='black'):
    """
    Draw a title on an image.

    Parameters:
    - image: The PIL Image object.
    - title: The title text to draw.
    - position: A tuple (x, y) specifying where the text should be drawn.
    - font: The path to a .ttf font file.
    - font_size: The size of the font.
    - color: The color of the font.
    """
    draw = ImageDraw.Draw(image)
    if font is None:
        font = ImageFont.load_default()
    else:
        font = ImageFont.truetype(font, font_size)
    draw.text(position, title, fill=color, font=font)
    return image

def images_to_pdf_with_titles(directory, output_pdf, titles, font_path=None):
    """
    Convert all images in a directory to a single PDF file with titles on each image.

    Parameters:
    - directory: Path to the directory containing the images.
    - output_pdf: Path for the output PDF file.
    - titles: A list of titles for each image. Must match the number of images.
    - font_path: Optional path to a .ttf font file.
    """
    img_files = [f for f in os.listdir(directory) if f.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.PNG'))]
    img_files.sort()

    if not img_files:
        print("No images found in the directory.")
        return

    if len(img_files) != len(titles):
        print("The number of titles does not match the number of images.")
        return

    images = []
    for img_file, title in zip(img_files, titles):
        img_path = os.path.join(directory, img_file)
        with Image.open(img_path).convert('RGB') as img:
            img_with_title = draw_title_on_image(img, title, font=font_path)
            images.append(img_with_title)

    first_img = images[0]
    other_imgs = images[1:]

    first_img.save(output_pdf, save_all=True, append_images=other_imgs)
    print(f"PDF created successfully: {output_pdf}")

# Example usage
directory_path = '/Users/idohaber/Desktop/presentation'
output_pdf_path = 'test.pdf'
titles = ["Title 1", "Title 2", "Title 3",'4','5']  # Add more titles as needed
#font_path = 'path/to/your/font.ttf'  # Optional: specify your font path here

images_to_pdf_with_titles(directory_path, output_pdf_path, titles, font_path=None)
