import pdfplumber
import pandas as pd
from datetime import datetime
import os
import logging
import re

# Import category mapping dictionary from category_mapping.py
from category_mapping import category_mapping

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def extract_transactions(pdf_path):
    all_text = ''
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            all_text += page.extract_text() + '\n'
    logging.debug(f"Extracted text: {all_text[:1000]}...")  # Log the first 1000 characters of the extracted text
    return all_text

def extract_year_from_text(text):
    match = re.search(r'\b\d{4}\b', text)
    if match:
        return match.group(0)
    else:
        logging.warning("Year not found in the text.")
        return "2020"  # Fallback to 2020 if year not found

def line_contains_transaction(line):
    # Match lines with dates and amounts
    pattern = re.compile(r'(\b\w{3} \d{2}\b).+?(-?[\d,]+\.\d{2}\b)')
    return bool(pattern.search(line))

def parse_transaction_line(line, year):
    try:
        # Extracting dates, description, and amount using regular expressions
        match = re.search(r'(\w{3} \d{2}) (\w{3} \d{2}) (.+?) (-?[\d,]+\.\d{2})', line)
        if not match:
            logging.debug(f"No match found for line: {line}")
            return None
        transaction_date = match.group(1)
        posted_date = match.group(2)
        description = match.group(3).strip()
        cad_amount = match.group(4).replace(',', '')  # Remove commas from the amount
        
        logging.debug(f"Parsed line: transaction_date={transaction_date}, posted_date={posted_date}, description={description}, cad_amount={cad_amount}")
        
        # Use the extracted year and format the date
        transaction_date = datetime.strptime(f"{year} {transaction_date}", '%Y %b %d').strftime('%Y-%m-%d')
        posted_date = datetime.strptime(f"{year} {posted_date}", '%Y %b %d').strftime('%Y-%m-%d')
        
        return {
            'posted_date': posted_date,
            'description': description,
            'cad_amount': cad_amount,
        }
    except (IndexError, ValueError, AttributeError) as e:
        logging.warning(f"Failed to parse line: {line}, error: {e}")
        return None

def parse_text(text):
    lines = text.split('\n')
    year = extract_year_from_text(text)
    transactions = []
    in_payments_section = False
    in_other_details_section = False

    for line in lines:
        logging.debug(f"Processing line: {line}")
        if "Payments received" in line:
            in_payments_section = True
        elif "Returns and other credits" in line or "Purchases" in line:
            in_payments_section = False
        elif "Other details about your account" in line:
            in_other_details_section = True

        if in_other_details_section:
            continue

        if line_contains_transaction(line):
            if not in_payments_section:
                transaction = parse_transaction_line(line, year)
                if transaction:
                    transactions.append(transaction)

    logging.debug(f"Identified transactions: {transactions}")
    return transactions

def categorize_transaction(description):
    for keyword, (sub_category, category) in category_mapping.items():
        if keyword in description.upper():
            return sub_category, category
    return "Uncategorized", "Uncategorized"  # Default if no match found

def clean_transactions(transactions):
    cleaned_data = []
    for transaction in transactions:
        try:
            date = format_date(transaction['posted_date'])
            amount = float(transaction['cad_amount'])
            description = transaction['description']
            sub_category, category = categorize_transaction(description)
            category_type = 'EXPENSE'

            if amount < 0:
                debit = ""
                credit = abs(amount)
            else:
                debit = amount
                credit = ""

            cleaned_data.append({
                'account': 'Mastercard',
                'date': date,
                'blank_1': '',
                'blank_2': '',
                'blank_3': '',
                'description': description,
                'debit': debit,
                'credit': credit,
                'blank_4': '',
                'sub_category': sub_category,
                'category': category,
                'category_type': category_type
            })
        except Exception as e:
            logging.warning(f"Failed to clean transaction: {transaction}, error: {e}")
    logging.debug(f"Cleaned transactions: {cleaned_data}")
    return cleaned_data

def format_date(date_str):
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
        return date.strftime('%Y-%m-%d')
    except ValueError:
        logging.warning(f"Date format error: {date_str}")
        return None

def save_to_excel(cleaned_data, excel_path):
    if not cleaned_data:
        logging.warning("No transactions to save.")
        return
    df = pd.DataFrame(cleaned_data)
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    df = df[['account', 'date', 'blank_1', 'blank_2', 'blank_3', 'description', 'debit', 'credit', 'blank_4', 'sub_category', 'category', 'category_type']]
    df.columns = ['Account', 'Date', 'Blank_1', 'Blank_2', 'Blank_3', 'Description', 'Debit', 'Credit', 'Blank_4', 'Sub-category', 'Category', 'Category Type']
    logging.debug(f"DataFrame to save: {df}")

    with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='New Transactions', index=False)
        workbook = writer.book
        worksheet = writer.sheets['New Transactions']
        date_format = workbook.add_format({'num_format': 'yyyy-mm-dd'})
        worksheet.set_column('B:B', None, date_format)
    
    logging.info("Transactions successfully saved to Excel.")

def process_pdfs(folder_path, excel_path):
    files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
    for file in files:
        pdf_path = os.path.join(folder_path, file)
        logging.info(f"Processing file: {pdf_path}")
        text = extract_transactions(pdf_path)
        transactions = parse_text(text)
        cleaned_data = clean_transactions(transactions)
        save_to_excel(cleaned_data, excel_path)

def main():
    folder_path = '/<path_to_PDF_directory>/PDFs/'
    excel_path = '/<path_to_Excel_sheet>/Transactions.xlsx'
    
    process_pdfs(folder_path, excel_path)

if __name__ == "__main__":
    main()
