
'''
Quick GIF :This fuction creates a GIF with flexbile amount of images and 
speed of transition

To view output - either right click on file and open with 
Google Chrome.app or paste to Word.

'''

from PIL import Image
import os

def create_gif(image_folder, output_filepath, duration=500):
    """
    Create a GIF from a set of images.

    :param image_folder: Folder containing images.
    :param output_filepath: File path to save the GIF.
    :param duration: Duration between frames in milliseconds.
    """
    images = []

    # Collect image files from the specified folder
    for file_name in sorted(os.listdir(image_folder)):
        if file_name.endswith('.png') or file_name.endswith('.jpg'):
            file_path = os.path.join(image_folder, file_name)
            images.append(Image.open(file_path))

    # Save the images as a GIF
    images[0].save(output_filepath, save_all=True, append_images=images[1:], optimize=False, duration=duration, loop=0)


path = '/Users/idohaber/Desktop/Projects/00_Visualization_code/GIF_imgs_Example'

create_gif(path, 'output.gif', duration=500)
