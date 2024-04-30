import PyPDF2


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
