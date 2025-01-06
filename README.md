# ImageFormMapper

ImageFormMapper is a tool for mapping and filling out scanned forms using sample data. It allows you to position all the necessary elements for mass-printing filled forms.
This has been succesfully used for 1099 MISC and NEC form filling at enterprise scale.

## How to Customize Filled Forms

To identify the elements that need to be filled in the form, use the `find_form_fields.py` script. This script will list all the field names in your form.

```bash
python find_form_fields.py
```

Simple Usage

For the primary use case, follow these steps:

1. Install conda if you don’t already have it.
2. Create and activate the environment specified in environment.yml.
3. Run main.py with the path to your input CSV file as an argument.

```bash
conda env create -f environment.yml
conda activate formfiller
python main.py input_csv
```
