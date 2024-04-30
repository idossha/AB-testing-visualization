from reportlab.lib.colors import black, white
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


def create_titles_pdf(titles, output_pdf, target_size=None):

    c = canvas.Canvas(output_pdf, pagesize=target_size)
    width, height = target_size
    font_size = 30

    # Define the consistent subtitle. The words will be separated equally along the x axis of the page.
    bottom_title = "   "
    bottom_font_size = 20

    # Split the bottom title into words
    bottom_title_words = bottom_title.split()

    # Calculate the total width of all words and the spacing needed
    total_words_width = sum(
        c.stringWidth(word, "Helvetica-Bold", bottom_font_size)
        for word in bottom_title_words
    )
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
        background_y = height - background_height - 25  # Adjust position as needed

        # Draw the background
        c.setFillColor(white)
        c.rect(
            background_x,
            background_y,
            background_width,
            background_height,
            stroke=0,
            fill=1,
        )

        # Draw the title text
        text_x = (width - text_width) / 2
        text_y = background_y + (background_height - text_height) / 2
        c.setFillColor(black)
        c.drawString(text_x, text_y, title)

        # Draw the consistent bottom title at specific x-coordinates
        bottom_text_y = 30  # Y-coordinate for bottom title
        x_positions = [120, 1120, 2120]  # X-coordinates for each word

        # Draw the bottom title
        c.setFont("Helvetica-Bold", bottom_font_size)
        x_position = space_between_words
        for word in bottom_title_words:
            c.drawString(x_position, 30, word)  # Y-coordinate adjusted for bottom title
            word_width = c.stringWidth(word, "Helvetica-Bold", bottom_font_size)
            x_position += word_width + space_between_words

        # Move to the next page
        c.showPage()

    c.save()


# Example function calls (if this module is run as a script)
if __name__ == "__main__":

    # create_titles_pdf example usage
    titles = ["Title 1", "Title 2", "Title 3"]
    output_pdf = "/path/to/titles.pdf"
    create_titles_pdf(titles, output_pdf)
