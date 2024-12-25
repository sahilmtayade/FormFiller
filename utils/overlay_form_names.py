import os
import fitz  # PyMuPDF
import json


def overlay_field_names(input_pdf, output_pdf=None):
    if output_pdf is None:
        input_dir = os.path.dirname(input_pdf)  # Get the directory of the input PDF
        output_pdf = os.path.join(
            input_dir, os.path.basename(input_pdf).replace(".pdf", "_overlay.pdf")
        )
    # Open the original PDF file
    doc = fitz.open(input_pdf)

    # Create a list to store field names and positions
    field_data = []

    # Iterate over all pages in the PDF
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)

        # Find all widgets (form fields) on the page
        widgets = page.widgets()

        # For each widget, overlay the field name and save its details
        for widget in widgets:
            field_name = widget.field_name
            if field_name:  # Skip fields with no name
                rect = widget.rect  # Get the rectangle area of the widget
                x, y = rect.tl.x, rect.tl.y  # Top-left coordinates of the widget

                # Draw the field name as text on top of the widget
                page.insert_text(
                    (x, y - 12), field_name, fontsize=8, color=(0, 0, 0)
                )  # You can adjust the position and color

                # Store the field name and its position
                field_data.append(
                    {"field_name": field_name, "page": page_num, "coordinates": (x, y)}
                )

    # Save the updated PDF
    doc.save(output_pdf)

    # Save the field names and positions as JSON for later use
    with open("field_names.json", "w") as json_file:
        json.dump(field_data, json_file, indent=4)


if __name__ == "__main__":
    # Example usage: Overlay field names and save the modified PDF and JSON
    overlay_field_names("templates/1099_page_3.pdf")
