import fitz  # PyMuPDF


def extract_and_preserve_pages(
    input_doc: fitz.Document,
    page_index_start,
    page_index_end,
    target_doc: fitz.Document,
):
    # Insert pages into the new document from the specified range
    target_doc.insert_pdf(input_doc, from_page=page_index_start, to_page=page_index_end)

    # Iterate over the pages in the range and extract widgets
    for page_num in range(
        page_index_start, page_index_end + 1
    ):  # page_index_end is inclusive
        page = input_doc.load_page(page_num)  # Load the current page

        # Extract widgets (form fields) from the page
        form_widgets = page.widgets()

        # Get the corresponding new page where the widgets will be added
        new_page = target_doc[page_num - page_index_start]

        # Add the form fields/widgets to the new page
        for widget in form_widgets:
            new_page.add_widget(widget)


# Example usage
if __name__ == "__main__":
    # Open the original PDF file
    input_doc = fitz.open("templates/full.pdf")
    # Create a new PDF document
    target_doc = fitz.open()

    extract_and_preserve_pages(input_doc, 3, 3, target_doc=target_doc)

    # Save the new PDF containing the pages and their widgets
    target_doc.save("templates/1099_page_3.pdf")
