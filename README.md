
## Image Pairing and PDF Generation
This project provides a Python script for pairing images stored in two different directories, optionally resizing them, and then combining these paired images into a single PDF document. It's particularly useful for visual comparison tasks, such as A/B testing results, before-and-after scenarios, or any situation where side-by-side image comparison is needed.

#### Features
Pair images from two separate directories based on matching filenames.
Optionally resize images to a specified target size.
Special handling for images with a defined keyword in their filenames.
Combine paired images into a single, easy-to-distribute PDF file.
Easily create titles and subtitles to your presentation. 

#### Prerequisites
Before running this script, ensure you have Python installed on your system. This project requires the following Python libraries:

- PIL (Python Imaging Library), also known as Pillow for image processing.
- PyPDF2
- reportlab
- os for directory and file operations.
- time for tracking the script's execution time.

You can install the required libraries using pip:

` pip install Pillow ` or `pip3 install Pillow` depending on your Python version and machine.

#### Usage

1. Prepare Your Directories: Organize your images into two separate directories. Ensure that the images meant to be paired have matching filenames across these directories.
2. Configure the Script: Modify the script parameters according to your needs:
- dirs: List of directories containing the images.
- output_pdf: Desired name for the output PDF file.
- target_size: Optional tuple specifying the width and height to resize each image (e.g., (1000, 1000)).
- special_string: Optional string to identify special images for individual treatment.
- Run the Script: Execute the script in your Python environment. The script will pair the images, optionally resize them, and then combine them into a single PDF document.
3. If you want to add titles and subtitles to your presentations - exectute the following two blocks. Make sure you change the titles content to your desires.

Example command:

` pair_imgs_to_pdf(['path/to/dir1', 'path/to/dir2'], 'output.pdf', target_size=(1000, 1000), special_string='special') `

#### Customization
You can customize the script to handle different scenarios by modifying the pair_imgs_to_pdf function. For example, you can change the logic for pairing images, adjust the resizing behavior, or modify the PDF generation process to suit your needs.


#### Example Code:

Attached are example images and output. If you want to replicate that, download the content and change the directories as necessary.

#### Contributing
Contributions to this project are welcome! Please feel free to fork the repository, make your changes, and submit a pull request.

#### License
This project is open source and available under the [MIT License](https://opensource.org/license/mit/)

#### Acknowledgments
Thanks to the Python community for providing the tools and documentation that made this project possible.
