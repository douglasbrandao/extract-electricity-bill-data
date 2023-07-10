from pathlib import Path

import pdfquery
import pandas as pd

pdf_files = Path.cwd().glob('**/*.pdf')

def extracted_data(pdf):
    customer_id = pdf.pq('LTTextLineHorizontal:overlaps_bbox("188.64, 1083.663, 242.04, 1093.173")').text()
    customer_name = pdf.pq('LTTextLineHorizontal:overlaps_bbox("15.72, 1103.656, 78.6, 1107.96")').text()
    installation_code = pdf.pq('LTTextLineHorizontal:overlaps_bbox("186.0, 1059.546, 244.08, 1069.042")').text()
    amount_due = pdf.pq('LTTextLineHorizontal:overlaps_bbox("206.88, 1030.407, 242.76, 1038.183")').text()
    billing_period = pdf.pq('LTTextLineHorizontal:overlaps_bbox("37.2, 1030.516, 72.24, 1038.299")').text()

    return pd.DataFrame({
        'customer_id': customer_id,
        'customer_name': customer_name,
        'installation_code': installation_code,
        'amount_due': amount_due,
        'billing_period': billing_period,
    }, index=[0])

for pdf_file in pdf_files:
    pdf = pdfquery.PDFQuery(pdf_file)
    pdf.load()
    xml_file = f'{pdf_file.stem}.xml'
    pdf.tree.write(xml_file, pretty_print=True)
    print(extracted_data(pdf))