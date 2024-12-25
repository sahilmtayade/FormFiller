# ImageFormMapper

Load a scanned form and some sample data to position all the elements needed in mass printing filled forms.

# How To Customize filled forms

Use the find_form_fields.py script to find all the element names you need to fill out in the form.
"""
python find_form_fields.py
"""

# Simple use

For the usecase this was made for, just need to install conda, activate environment, and run main.py with the correct csv input file as argument.

"""
conda env create -f environment.yml
conda activate formfiller
python main.py input_csv
"""
