## How to Customize Filled Forms

To identify the elements that need to be filled in the form, use the `find_form_fields.py` script. This script will list all the field names in your form.

```bash
python find_form_fields.py
```

## Steps to Prepare 1099 NEC and 1099 MISC Forms

1. **Download the latest PDF forms**
   - Get the most recent 1099 NEC and 1099 MISC PDFs from the IRS website.

2. **Extract the Copy B page**
   - Use the `utils/extract_page.py` script to extract the Copy B form (usually page 3):
   - Edit the script to set the correct input and output filenames.
   - Example:
     ```bash
     python utils/extract_page.py --input 1099nec.pdf --output 1099nec_copyb.pdf --page 3
     ```

3. **View form field names**
   - Run the `overlay_form_mapping` utility to see the field names in the PDF form.

4. **Field mapping for MISC and NEC**
   - For 1099 MISC: Field names map directly to CSV columns.
   - For 1099 NEC: Field names are mapped to human-readable names using `utils/old_to_new_nec.yml`, then mapped to CSV columns.

5. **Check for field name changes**
   - Field names may change between years (e.g., `rightCol` → `rightCollumn`, `header` → `PgHeader` or `PgBHeader`).
   - Make sure the field names in your mapping files match those in the latest PDF.

6. **Update mapping files as needed**
   - For 1099 MISC: Edit `misc_field_number_mapping.yml` at the top level of the project.
   - For 1099 NEC: Edit `utils/old_to_new_nec.yml`.

---

**Tip:** If you want a more permanent template and wish to avoid downloading a new PDF each year, check out the `rename fields` file. This allows you to rename the fields directly on the PDF itself, making future updates easier.