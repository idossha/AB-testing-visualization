import os
import sys

from PIL import Image, ImageDraw, ImageFont


def draw_title_on_image(
    image, title, position=(10, 10), font=None, font_size=40, color="black"
):
    draw = ImageDraw.Draw(image)
    if font is None:
        font = ImageFont.load_default()
    else:
        font = ImageFont.truetype(font, font_size)
    draw.text(position, title, fill=color, font=font)
    return image


def images_to_pdf_with_titles(directory, output_pdf, titles, font_path=None):
    img_files = [
        f
        for f in os.listdir(directory)
        if f.endswith((".png", ".jpg", ".jpeg", ".bmp"))
    ]
    img_files.sort()

    if not img_files:
        return "No images found in the directory."

    if len(img_files) != len(titles):
        return "The number of titles does not match the number of images."

    images = []
    for img_file, title in zip(img_files, titles):
        img_path = os.path.join(directory, img_file)
        with Image.open(img_path).convert("RGB") as img:
            img_with_title = draw_title_on_image(img, title, font=font_path)
            images.append(img_with_title)

    first_img = images[0]
    other_imgs = images[1:]
    first_img.save(output_pdf, save_all=True, append_images=other_imgs)
    return f"PDF created successfully: {output_pdf}"


def main():
    if len(sys.argv) < 4:
        print(
            "Usage: python script.py <directory> <output_pdf> <titles_comma_separated>"
        )
        sys.exit(1)

    directory = sys.argv[1]
    output_pdf = sys.argv[2]
    titles = sys.argv[3].split(",")

    result = images_to_pdf_with_titles(directory, output_pdf, titles)
    print(result)


if __name__ == "__main__":
    main()
