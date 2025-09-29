## VS Code & Conda Environment Setup

# Quick start
```bash
conda env create -f environment.yml
conda activate formfiller
python main.py -t misc input_csv
```
# Detailed Instructions
1. **Open VS Code in the FormFiller directory**
	- Launch VS Code and open the `FormFiller` folder.

2. **Place your input CSV files**
	- Put your input CSV files into the `inputs` folder. This is required for processing forms.


3. **Ensure Conda environment is active**
	- Switch to any shell besides PowerShell (recommended: Command Prompt or Bash).
	- In VS Code, click the dropdown arrow next to the plus sign in the terminal panel to select your shell.
	- Run:
	  ```sh
	  conda activate formfiller
	  ```

4. **On a new machine**
	- Create the environment using:
	  ```sh
	  conda env create -f environment.yml
	  ```

5. **Verify Python executable**
	- Run:
	  ```sh
	  which python
	  ```
	- This should show the path to the Python executable in your active environment.

6. **Output files**
	- The output will be either `misc_big.pdf` or `nec_big.pdf` depending on the type you specify.
	- If the file already exists, it will be overwritten.
		- To process your forms, use one of the following commands:
			```sh
			python main.py -t nec "<input_file.csv>"
			python main.py -t misc "<input_file.csv>"
			```
		- Replace `<input_file.csv>` with the name of your input file in the `inputs` folder.



# ImageFormMapper

ImageFormMapper is a tool for mapping and filling out scanned forms using sample data. It allows you to position all the necessary elements for mass-printing filled forms.
This has been succesfully used for 1099 MISC and NEC form filling at enterprise scale.

## Form Mapping Reference

For detailed instructions on mapping form fields, see the [FormMapping documentation](./formmapping.md).



