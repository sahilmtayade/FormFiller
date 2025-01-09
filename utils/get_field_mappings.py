import fitz  # PyMuPDF
import json

import yaml


def generate_field_number_mapping(input_pdf, output_yaml):
    # Open the PDF file
    doc = fitz.open(input_pdf)

    # Initialize the dictionary
    field_mapping = {}

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
                field_mapping[field_name] = -1

    # Save the mapping to a YAML file
    with open(output_yaml, "w") as yaml_file:
        yaml.dump(field_mapping, yaml_file, default_flow_style=False)

    print(f"Field name mapping saved to {output_yaml}")


# Example usage
if __name__ == "__main__":
    generate_field_number_mapping("templates/nec_template.pdf", "nec_fnm.yml")
