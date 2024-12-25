import os
import fitz  # PyMuPDF


def fill_form(pdf_path, output_pdf_path, field_data):
    # Ensure the output directory exists
    output_dir = os.path.dirname(output_pdf_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # Create the output directory if it doesn't exist

    doc = fitz.open(pdf_path)

    # Loop through each page to find form fields
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)

        # Get all form fields (widgets) on the page
        form_fields = page.widgets()

        for field in form_fields:
            # Check if the field name matches the ones in the field_data dictionary
            if field.field_name in field_data:
                field_value = field_data[field.field_name]

                # Handle different field types using constants
                if field.field_type == 7:  # PDF_WIDGET_TYPE_TEXT (7)
                    field.field_value = field_value
                    print(
                        f"Filled text field '{field.field_name}' on page {page_num + 1}"
                    )

                elif field.field_type == 2:  # PDF_WIDGET_TYPE_CHECKBOX (2)
                    field.field_value = (
                        True if field_value.lower() == "checked" else False
                    )
                    print(
                        f"Checked checkbox '{field.field_name}' on page {page_num + 1}"
                    )

                elif field.field_type == 5:  # PDF_WIDGET_TYPE_RADIOBUTTON (5)
                    # Handle radio button field (implement based on field_value)
                    print(f"Radio button '{field.field_name}' on page {page_num + 1}")

                # Other widget types can be handled similarly
                elif field.field_type == 1:  # PDF_WIDGET_TYPE_BUTTON (1)
                    print(f"Button field '{field.field_name}' on page {page_num + 1}")
                elif field.field_type == 3:  # PDF_WIDGET_TYPE_COMBOBOX (3)
                    print(f"Combobox field '{field.field_name}' on page {page_num + 1}")
                elif field.field_type == 4:  # PDF_WIDGET_TYPE_LISTBOX (4)
                    print(f"Listbox field '{field.field_name}' on page {page_num + 1}")
                elif field.field_type == 6:  # PDF_WIDGET_TYPE_SIGNATURE (6)
                    print(
                        f"Signature field '{field.field_name}' on page {page_num + 1}"
                    )
                else:
                    print(
                        f"Unknown field type '{field.field_name}' on page {page_num + 1}"
                    )
                field.update()

    # Save the modified PDF
    doc.save(output_pdf_path)


if __name__ == "__main__":
    pdf_path = "templates/sample_pdf.pdf"
    output_pdf_path = "outputs/output_filled_form.pdf"

    # Dictionary containing the field names and the corresponding data to fill
    field_data = {
        "Name": "John Doe",
        "Address": "123 Main St.",
        "Check Box1": "checked",  # Set to 'checked' or 'unchecked'
    }

    fill_form(pdf_path, output_pdf_path, field_data)
