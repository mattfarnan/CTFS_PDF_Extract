# Transaction Tracker Script

This script parses Canadian Tire Financial Services (ctfs.com) PDF statement files and extracts the relevant transaction information to save in an Excel file. It uses `pdfplumber` for PDF extraction, `pandas` for data manipulation, and `logging` for debug information.

## Prerequisites

- Python 3.x
- `pdfplumber`
- `pandas`
- `openpyxl`
- `xlsxwriter`

## Installation

First, ensure you have Python 3.x installed. Then, install the required libraries using pip:

```sh
pip install pdfplumber pandas openpyxl xlsxwriter
```

## Usage

1. **Place your PDF files**: Place all the PDF files you want to process in the specified folder. PDFs will be processed one-by-one and transactions will be appended to the end of the Excel file.
2. **Run the script**: Execute the script to process the PDFs and save the transactions to an Excel file.

### Steps:

1. **Extract Transactions**: Extract text from PDF files using `pdfplumber`.
2. **Parse Transactions**: Identify and parse transaction lines from the extracted text.
3. **Clean Transactions**: Format and categorize transaction data.
4. **Save to Excel**: Save the cleaned transactions to an Excel file.

### Configuration

- **Folder Path**: Update the `folder_path` variable with the path to your PDFs folder.
- **Excel Path**: Update the `excel_path` variable with the path where you want to save the Excel file.

### Running the Script

Run the script using the following command:

```sh
python ImportTransactions.py
```

## Logging

The script logs debug and warning information to help track the processing steps and identify any issues.

## Code Overview

### `extract_transactions(pdf_path)`

Extracts text from each page of the PDF file.

### `extract_year_from_text(text)`

Extracts the year from the text.

### `line_contains_transaction(line)`

Identifies if a line contains a transaction using regular expressions.

### `parse_transaction_line(line, year)`

Parses a line to extract transaction details such as date, description, and amount.

### `parse_text(text)`

Splits the text into lines and processes each line to identify and extract transactions.

### `categorize_transaction(description)`

Categorizes the transaction based on keywords in the description. The script uses a `category_mapping.py` file to map keywords to specific categories.

### `clean_transactions(transactions)`

Formats and cleans the transaction data.

### `format_date(date_str)`

Formats dates into a standard format.

### `save_to_excel(cleaned_data, excel_path)`

Saves the cleaned transactions to an Excel file with correct formatting.

### `process_pdfs(folder_path, excel_path)`

Processes all PDF files in the specified folder and saves the transactions to an Excel file.

### `main()`

Main function to set folder and Excel paths and initiate processing.

## Example

```python
def main():
    folder_path = '/path/to/your/pdfs/'
    excel_path = '/path/to/save/transactions.xlsx'
    
    process_pdfs(folder_path, excel_path)

if __name__ == "__main__":
    main()
```

Update the `folder_path` and `excel_path` with your specific paths and run the script. The transactions from the PDFs will be extracted and saved to the Excel file.

## `category_mapping.py`

This script uses a separate `category_mapping.py` file to categorize transactions. The `category_mapping.py` file should define a dictionary where the keys are keywords found in transaction descriptions, and the values are tuples containing the sub-category and category.

Example of `category_mapping.py`:

```python
category_mapping = {
    "GROCERY STORE": ("Groceries", "Food"),
    "GAS STATION": ("Gasoline", "Transport"),
    "RESTAURANT": ("Dining Out", "Food"),
    # Add more mappings as needed
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

This script was generated with the assistance of ChatGPT, a language model created by OpenAI.

Feel free to modify the script according to your requirements. For any issues or improvements, please open an issue or submit a pull request.

Happy Tracking!