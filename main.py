import csv
import os
import fitz
import yaml

from utils.fill_form import fill_form


def read_yml() -> dict:
    with open("field_number_mapping.yml", "r") as file:
        data = yaml.safe_load(file)
    return data


def read_csv(input_file: str) -> list[list]:
    with open(input_file, "r") as file:
        reader = csv.reader(
            file, quotechar='"', delimiter=",", quoting=csv.QUOTE_MINIMAL
        )
        return list(reader)


def main(input_csv_file: str, template_path: str):
    field_mappings = read_yml()
    csv_data = read_csv(input_file=input_csv_file)
    big_doc = fitz.open()
    for i, row in enumerate(csv_data):
        fm = {}
        for field, csvidx in field_mappings.items():
            if isinstance(csvidx, list):
                fm[field] = " \n".join([row[idx] for idx in csvidx])
            else:
                fm[field] = row[csvidx]
        output_path = os.path.join("outputs", str(i) + ".pdf")
        fill_form(
            pdf_path=template_path,
            field_data=fm,
            output_pdf_path=output_path,
            # new_doc=big_doc,
        )
    # big_output_path = "outputs/big/big.pdf"
    # output_dir = os.path.dirname(big_output_path)
    # if not os.path.exists(output_dir):
    #     os.makedirs(output_dir)  # Create the output directory if it doesn't exist
    # big_doc.save(big_output_path)


if __name__ == "__main__":
    input_csv_file = "inputs/Tax 1099 print options MISC.csv"
    # input_csv_file = "inputs/example_input.csv"
    template_path = "templates/1099_page_3.pdf"
    main(input_csv_file=input_csv_file, template_path=template_path)
