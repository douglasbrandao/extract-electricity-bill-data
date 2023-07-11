from pathlib import Path

import pdfquery
import pandas as pd

current_dir = Path.cwd()
pdf_files = current_dir.glob('**/*.pdf')

def sanitize_string(plaintext: str) -> str:
    sanitized_string = plaintext
    if 'R$' in plaintext:
        sanitized_string = plaintext.lstrip('R$ ')
    return sanitized_string.replace(',', '.')

def extracted_data(pdf):
    customer_id = pdf.pq('LTTextLineHorizontal:overlaps_bbox("188.64, 1083.663, 242.04, 1093.173")').text()
    customer_name = pdf.pq('LTTextLineHorizontal:overlaps_bbox("15.72, 1103.656, 78.6, 1107.96")').text()
    installation_code = pdf.pq('LTTextLineHorizontal:overlaps_bbox("186.0, 1059.546, 244.08, 1069.042")').text()
    amount_due = pdf.pq('LTTextLineHorizontal:overlaps_bbox("206.88, 1030.407, 242.76, 1038.183")').text()
    billing_period = pdf.pq('LTTextLineHorizontal:overlaps_bbox("37.2, 1030.516, 72.24, 1038.299")').text()
    kwh_month_quantity = pdf.pq('LTTextLineHorizontal:overlaps_bbox("110.88, 796.569, 118.08, 800.885")').text()
    kwh_month_unit_price_with_taxes = pdf.pq('LTTextLineHorizontal:overlaps_bbox("132.72, 795.849, 150.72, 800.165")').text()
    kwh_month_price = pdf.pq('LTTextLineHorizontal:overlaps_bbox("208.68, 716.289, 221.88, 720.605")').text()
    cofins_price = pdf.pq('LTTextLineHorizontal:overlaps_bbox("184.8, 796.494, 195.6, 800.942")').text()
    icms_price_base = pdf.pq('LTTextLineHorizontal:overlaps_bbox("208.68, 796.569, 221.88, 800.885")').text()
    icms_aliquota = pdf.pq('LTTextLineHorizontal:overlaps_bbox("234.0, 796.569, 238.8, 800.885")').text()
    icms_price = pdf.pq('LTTextLineHorizontal:overlaps_bbox("246.96, 716.289, 257.76, 720.605")').text()
    unit_fee = pdf.pq('LTTextLineHorizontal:overlaps_bbox("266.52, 796.569, 284.52, 800.885")').text()

    return {
        'customer_id': customer_id,
        'customer_name': customer_name,
        'installation_code': installation_code,
        'amount_due': float(sanitize_string(amount_due)),
        'billing_period': billing_period,
        'kwh_month_quantity': int(kwh_month_quantity),
        'kwh_month_unit_price_with_taxes': float(sanitize_string(kwh_month_unit_price_with_taxes)),
        'kwh_month_price': float(sanitize_string(kwh_month_price)),
        'cofins_price': float(sanitize_string(cofins_price)),
        'icms_price_base': float(sanitize_string(icms_price_base)),
        'icms_aliquota': int(icms_aliquota),
        'icms_price': float(sanitize_string(icms_price)),
        'unit_fee': float(sanitize_string(unit_fee)),
    }

data = []

for pdf_file in pdf_files:
    pdf = pdfquery.PDFQuery(pdf_file)
    pdf.load()
    xml_file = current_dir / f'{pdf_file.stem}.xml'
    pdf.tree.write(xml_file.name, pretty_print=True)
    data.append(extracted_data(pdf))
    xml_file.unlink() # uncomment if you don't want to delete these .xml files

df = pd.DataFrame(data)
df.to_csv(current_dir / 'planilha.csv')