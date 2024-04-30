import os
import sys

from PIL import Image


def create_gif(image_folder, output_filepath, duration=500):
    images = []
    try:
        # Collecting images from the specified directory
        for file_name in sorted(os.listdir(image_folder)):
            if file_name.lower().endswith((".png", ".jpg", ".jpeg")):
                file_path = os.path.join(image_folder, file_name)
                images.append(Image.open(file_path))

        if not images:
            return "No images found in the specified directory."

        # Creating the GIF
        images[0].save(
            output_filepath,
            save_all=True,
            append_images=images[1:],
            optimize=False,
            duration=duration,
            loop=0,
        )
        return f"GIF created successfully and saved to {output_filepath}"
    except Exception as e:
        return f"An error occurred: {str(e)}"


def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py <image_folder> <output_filepath> [duration]")
        sys.exit(1)

    image_folder = sys.argv[1]
    output_filepath = sys.argv[2]
    duration = 500  # Default duration

    if len(sys.argv) > 3:
        duration = int(sys.argv[3])

    result = create_gif(image_folder, output_filepath, duration)
    print(result)


if __name__ == "__main__":
    main()
