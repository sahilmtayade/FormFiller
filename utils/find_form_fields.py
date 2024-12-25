import fitz  # PyMuPDF


def check_form_fields(pdf_path):
    doc = fitz.open(pdf_path)

    # Loop through each page to check for form fields
    fields_found = False
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)

        # Get all form fields (widgets) on the page
        form_fields = page.widgets()

        if form_fields:
            fields_found = True
            print(f"Form fields on page {page_num + 1}:")
            for field in form_fields:
                print(f"  Field Name: {field.field_name}")
                print(f"  Type: {field.field_type}")
                print(f"  Rect: {field.rect}")
                print("-" * 40)

    if not fields_found:
        print("No form fields found in the document.")


if __name__ == "__main__":
    pdf_path = "templates/1099_page_3.pdf"
    check_form_fields(pdf_path)
