import argparse
import csv
import os
import traceback
import fitz
import yaml

from utils.fill_form import fill_form


def read_yml(mapping_path="field_number_mapping.yml") -> dict:
    with open(mapping_path, "r") as file:
        data = yaml.safe_load(file)
    return data


def read_csv(input_file: str) -> list[list]:
    with open(input_file, "r") as file:
        reader = csv.reader(
            file, quotechar='"', delimiter=",", quoting=csv.QUOTE_MINIMAL
        )
        return list(reader)


def main(
    input_csv_file: str,
    template_path: str,
    one_doc=False,
    output_big_file="big",
    fm_path=None,
    skip_header=False,
):
    filled = 0
    field_mappings = read_yml(mapping_path=fm_path)
    csv_data = read_csv(input_file=input_csv_file)
    if one_doc:
        big_doc = fitz.open()
    else:
        big_doc = None
    for i, row in enumerate(csv_data):
        if skip_header and i == 0:
            continue
        if not row:
            continue
        fm = {}
        for field, csvidx in field_mappings.items():
            if csvidx == "-1":
                continue
            if isinstance(csvidx, list):
                fm[field] = " \n".join([row[idx] for idx in csvidx])
            else:
                try:
                    fm[field] = row[csvidx]
                except Exception:
                    print(f"Error {traceback.format_exc()}")
                    print(f"Error row = {row}")
                    print(f"{len(row)=}")
                    exit()

        output_path = os.path.join("outputs", str(i) + ".pdf")
        fill_form(
            pdf_path=template_path,
            field_data=fm,
            output_pdf_path=output_path,
            # flatten=flatten,
            new_doc=big_doc,
        )
        filled += 1
    print(f"Finished, filled {filled}")
    big_output_path = f"outputs/big/{output_big_file}.pdf"
    output_dir = os.path.dirname(big_output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # Create the output directory if it doesn't exist
    big_doc.save(big_output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process an input file from the inputs folder."
    )
    parser.add_argument(
        "input_file",
        type=str,
        help="Name of the input file located in the 'inputs' folder.",
    )
    parser.add_argument(
        "--template",
        "-t",
        type=str,
        default="misc",
        help="Specify 'nec', 'misc', or a valid file path",
    )
    parser.add_argument(
        "--skip-header",
        "-s",
        action="store_true",
        help="Set this flag to skip first line. Default is False.",
    )
    args = parser.parse_args()

    # Join 'inputs' folder path with the provided file name
    inputs_folder = "inputs"
    input_file_path = os.path.join(inputs_folder, args.input_file)

    # Check if the file exists
    if not os.path.exists(input_file_path):
        print(f"Error: File '{input_file_path}' does not exist.")
        exit()

    # input_csv_file = "inputs/Tax 1099 print options MISC.csv"
    # input_csv_file = "inputs/example_input.csv"
    if args.template == "misc":
        template_path = "templates/1099_page_3.pdf"
        output_big = "misc_big"
        mapping_path = "misc_field_number_mapping.yml"
    elif args.template == "nec":
        template_path = "templates/nec_template.pdf"
        output_big = "nec_big"
        mapping_path = "nec_fnm.yml"
    else:
        template_path = args.template
        output_big = "big"
        mapping_path = "field_number_mapping_custom.yml"

    # flatten = True
    one_doc = True
    main(
        input_csv_file=input_file_path,
        template_path=template_path,
        one_doc=one_doc,
        output_big_file=output_big,
        fm_path=mapping_path,
        skip_header=args.skip_header,
    )
