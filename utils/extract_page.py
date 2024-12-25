import fitz  # PyMuPDF


def extract_and_preserve_pages(input_pdf, page_index_start, page_index_end, output_pdf):
    # Open the original PDF file
    doc = fitz.open(input_pdf)

    # Create a new PDF document
    new_doc = fitz.open()

    # Insert pages into the new document from the specified range
    new_doc.insert_pdf(doc, from_page=page_index_start, to_page=page_index_end)

    # Iterate over the pages in the range and extract widgets
    for page_num in range(
        page_index_start, page_index_end + 1
    ):  # page_index_end is inclusive
        page = doc.load_page(page_num)  # Load the current page

        # Extract widgets (form fields) from the page
        form_widgets = page.widgets()

        # Get the corresponding new page where the widgets will be added
        new_page = new_doc[page_num - page_index_start]

        # Add the form fields/widgets to the new page
        for widget in form_widgets:
            new_page.add_widget(widget)

    # Save the new PDF containing the pages and their widgets
    new_doc.save(output_pdf)


# Example usage
if __name__ == "__main__":
    extract_and_preserve_pages("templates/full.pdf", 3, 3, "templates/1099_page_3.pdf")
