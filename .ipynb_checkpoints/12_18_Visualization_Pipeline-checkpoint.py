#!/usr/bin/env python
# coding: utf-8

# In[4]:


from PIL import Image, ImageDraw, ImageFont
import os
import time
import PyPDF2
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black, white
from reportlab.lib.units import inch


# ## Creates PDF1 with Analysis Figures
# 1. change path of directories and number of directories included in function.
# 2. Keep in mind target size based on number of directories. 

# In[18]:


def pair_imgs_to_pdf(dirs, output_pdf, target_size=None, special_string=None):
    """
    Pair images from multiple directories based on their exact names and save them as a PDF.
    If a special string is provided, images containing that string in their name are placed individually in the PDF.
    Images with identical names across directories are paired.

    :param dirs: List of directories containing PNG, JPG, JPEG files.
    :param output_pdf: Output PDF file name.
    :param target_size: Optional tuple (width, height) to resize each individual image.
    :param special_string: Optional string to identify special images for individual placement. If None, no special treatment.
    """
    start_time = time.time()  # Start timing
    all_images = []

    # Collect images from each directory
    image_files = {dir: sorted([f for f in os.listdir(dir) if f.endswith(('.png', '.jpg', '.jpeg'))]) for dir in dirs}

    # Find matching images across directories
    paired_images = set()
    for dir, files in image_files.items():
        for file in files:
            if special_string and special_string in file:
                # Process special images
                img_path = os.path.join(dir, file)
                img = Image.open(img_path).convert('RGB')
                if target_size:
                    img = img.resize(target_size, Image.Resampling.LANCZOS)
                all_images.append(img)
            elif file not in paired_images:
                # Pair matching images
                imgs = []
                for other_dir in dirs:
                    other_path = os.path.join(other_dir, file)
                    if os.path.exists(other_path):
                        img = Image.open(other_path).convert('RGB')
                        if target_size:
                            img = img.resize(target_size, Image.Resampling.LANCZOS)
                        imgs.append(img)
                        paired_images.add(file)

                if len(imgs) > 1:
                    total_width = sum(img.width for img in imgs)
                    max_height = max(img.height for img in imgs)
                    new_img = Image.new('RGB', (total_width, max_height))

                    x_offset = 0
                    for img in imgs:
                        new_img.paste(img, (x_offset, 0))
                        x_offset += img.width

                    all_images.append(new_img)

    # Check if there are images to be saved in the PDF
    if not all_images:
        print("No images to create PDF.")
        return

    # Save all images to a PDF
    all_images[0].save(output_pdf, save_all=True, append_images=all_images[1:])
    print(f"PDF created successfully: {output_pdf}")

    end_time = time.time()  # End timing
    print(f"The function took {end_time - start_time} seconds to run.")

# Example usage
dir1 = '/Users/idohaber/Desktop/Data_Visualization_Output/All Output/12_06_23_Pilot/Averaging EPOCHs/erp_noreref'
dir2 = '/Users/idohaber/Desktop/Data_Visualization_Output/All Output/12_06_23_Pilot/Averaging EPOCHs/erp_avgref'

# Add or remove directories as needed
# Replace None based on special string 
pair_imgs_to_pdf([dir1, dir2], 'figures_combined.pdf', target_size=(1000, 1000), special_string='raw') 


# ## Create PDF2 with titles for figures
# 1. Make sure to change X dimention with respect to the number of figures in PDF1. 2Figs=2000, 3Figs=3000.
# 

# In[3]:


def create_titles_pdf(titles, output_pdf, target_size=None):

    c = canvas.Canvas(output_pdf, pagesize=target_size)
    width, height = target_size
    font_size = 30

    # Define the consistent bottom title
    bottom_title = "Forehead_Reference Mastoid_Reference Average_Reference"
    bottom_font_size = 20  # You can adjust the font size for the bottom title
    
    # Split the bottom title into words
    bottom_title_words = bottom_title.split()

    # Calculate the total width of all words and the spacing needed
    total_words_width = sum(c.stringWidth(word, "Helvetica-Bold", bottom_font_size) for word in bottom_title_words)
    total_spacing = width - total_words_width
    space_between_words = total_spacing / (len(bottom_title_words) + 1)
    
    for title in titles:
        # Set up the title font
        c.setFont("Helvetica-Bold", font_size)
        
        # Calculate text width and height
        text_width = c.stringWidth(title, "Helvetica-Bold", font_size)
        text_height = font_size

        # Calculate background and text positions
        background_width = text_width + 2000
        background_height = text_height + 50
        background_x = (width - background_width) // 2
        background_y = height - background_height - 25 # Adjust position as needed

        # Draw the background
        c.setFillColor(white)
        c.rect(background_x, background_y, background_width, background_height, stroke=0, fill=1)

        # Draw the title text
        text_x = (width - text_width) / 2
        text_y = background_y + (background_height - text_height) / 2
        c.setFillColor(black)
        c.drawString(text_x, text_y, title)

        # Draw the consistent bottom title at specific x-coordinates
        bottom_text_y = 30  # Y-coordinate for bottom title
        x_positions = [120, 1120, 2120]  # X-coordinates for each word

        for word, x in zip(bottom_title_words, x_positions):
            c.drawString(x, bottom_text_y, word)


        
        # Move to the next page
        c.showPage()

    c.save()

# Example Usage
page_titles = ['Pseudo Randomaized Triggering During Sleep', 
               'Pseudo Randomaized Triggering During Sleep', 
               'Pseudo Randomaized Triggering During Sleep',
               'Pseudo Randomaized Triggering During Sleep',
               'Pseudo Randomaized Triggering During Sleep',
               'Pseudo Randomaized Triggering During Sleep',
               'Pseudo Randomaized Triggering During Sleep',
               'Pseudo Randomaized Triggering During Sleep']

create_titles_pdf(page_titles, "titles.pdf",  target_size=(2000,1100))


# ## Creates Final PDF by overlaying on ontop of Other.

# In[26]:


def merge_pdfs(base_pdf_path, overlay_pdf_path, output_pdf_path):
    # Open the base PDF
    base_pdf = PyPDF2.PdfReader(open(base_pdf_path, "rb"))

    # Open the overlay PDF
    overlay_pdf = PyPDF2.PdfReader(open(overlay_pdf_path, "rb"))

    # Create a PDF writer
    pdf_writer = PyPDF2.PdfWriter()

    # Check and adjust dimensions if necessary
    base_page = base_pdf.pages[0]
    overlay_page = overlay_pdf.pages[0]
    base_height = base_page.mediabox[3]
    overlay_height = overlay_page.mediabox[3]
    
    # Adjust base page size if overlay is taller
    if overlay_height > base_height:
        for page in base_pdf.pages:
            page.mediabox[3] = overlay_height
    
   # Iterate through base PDF pages and merge
    for page_num in range(len(base_pdf.pages)):
        base_page = base_pdf.pages[page_num]
        # Check if there's a corresponding overlay page, else use the last overlay page
        overlay_page = overlay_pdf.pages[min(page_num, len(overlay_pdf.pages) - 1)]

        # Merge the pages
        base_page.merge_page(overlay_page)

        # Add the merged page to the writer
        pdf_writer.add_page(base_page)

    # Write the merged PDF to file
    with open(output_pdf_path, "wb") as out:
        pdf_writer.write(out)


# In[33]:


merge_pdfs("figures_combined.pdf","titles.pdf", "final_output.pdf")`


# ## Old Version. Do not Touch
# 

# In[7]:


def pair_imgs_to_pdf(dirs, output_pdf, target_size=None):
    """
    Pair images from multiple directories and save them as a PDF.
    
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
        files = [f for f in os.listdir(dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
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

            img = img.convert('RGB')
            imgs.append(img)

        # Calculate dimensions for the new image
        total_width = sum(img.width for img in imgs)
        max_height = max(img.height for img in imgs)

        # Create a new image and paste the individual images
        new_img = Image.new('RGB', (total_width, max_height))
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


# In[16]:


dir1 = '/path1' # Replace with the path to your first directory
dir2 = '/path2' # Replace with the path to your second directory
dir3 = '/path3' # Replace with the path to your third directory
dir4 = '/path4' # Replace with the path to your third directory


"""
add or remove number of dirs from list based on your needs
set your desired target size per image
set name for pdf
"""

pair_imgs_to_pdf([dir1,dir2], 'figures_combined.pdf', target_size=(1000,1000)) 

