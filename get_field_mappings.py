import fitz  # PyMuPDF
import json


def generate_field_number_mapping(input_pdf, output_json):
    # Open the PDF file
    doc = fitz.open(input_pdf)

    # Initialize the dictionary
    field_mapping = {}
    field_number = 1

    # Iterate over all pages in the PDF
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)

        # Extract all form widgets (fields)
        widgets = page.widgets()
        if not widgets:
            continue  # Skip pages with no widgets

        for widget in widgets:
            field_name = widget.field_name  # Get the field name
            if field_name:
                field_mapping[field_name] = field_number
                field_number += 1

    # Save the mapping to a JSON file
    with open(output_json, "w") as json_file:
        json.dump(field_mapping, json_file, indent=4)

    print(f"Field number mapping saved to {output_json}")


# Example usage
if __name__ == "__main__":
    generate_field_number_mapping(
        "templates/1099_page_3.pdf", "field_number_mapping.json"
    )
