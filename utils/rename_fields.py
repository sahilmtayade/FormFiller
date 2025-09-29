import fitz  # PyMuPDF
import yaml


def rename_fields_with_mapping(
    pdf_path: str, mapping_path: str, output_path: str
) -> None:
    # Load the mapping from the YAML file
    with open(mapping_path, "r") as f:
        mapping = yaml.safe_load(f)["fields"]

    # Open the PDF document
    doc = fitz.open(pdf_path)

    # Iterate through all pages
    for page_number, page in enumerate(doc, start=1):
        widgets = page.widgets() or []

        for widget in widgets:
            old_name = widget.field_name

            # Check if the old name is in the mapping
            if old_name in mapping:
                new_name = mapping[old_name]
                widget.field_name = new_name
                print(f"Renamed '{old_name}' to '{new_name}'")
            else:
                print(f"Skipping '{old_name}' (not in mapping)")
            widget.update()

    # Save the modified document
    doc.save(output_path)
    print(f"Renamed fields saved to '{output_path}'")
    doc.close()


# Usage
rename_fields_with_mapping(
    "templates/nec_template.pdf",
    "utils/old_to_new_nec.yml",
    "templates/nec_template1.pdf",
)
# rename_fields_with_mapping("nec_page_3.pdf", "old_to_new_nec.yaml", "nec_template.pdf")
