import fitz  # PyMuPDF


def list_annotations(pdf_path):
    # Open the PDF file
    doc = fitz.open(pdf_path)

    # Iterate over each page
    annotations = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        page_annot = page.annots()  # Get all annotations in the page
        if page_annot:
            for annot in page_annot:
                # Collect annotation info (id, position, and text)
                annot_info = {
                    "page": page_num + 1,
                    "id": annot.info.get("title", "No ID"),
                    "rect": annot.rect,  # Coordinates of the annotation
                    "field_name": annot.field_name,
                }
                annotations.append(annot_info)

    # Print out the list of annotations
    for i, annot in enumerate(annotations):
        print(f"Annotation {i + 1}:")
        print(f"  Page: {annot['page']}")
        print(f"  ID: {annot['id']}")
        print(f"  Field Name: {annot['field_name']}")
        print(f"  Rect: {annot['rect']}")
        print("-" * 40)


if __name__ == "__main__":
    pdf_path = "templates/form1099msc.pdf"  # Path to your 1099 form
    list_annotations(pdf_path)
