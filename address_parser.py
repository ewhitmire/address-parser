import pandas as pd
import usaddress
import os
from collections import OrderedDict
from tkinter.filedialog import askopenfilename
import argparse


COLUMN_NAME = "Addresses"

def recover_misparsed(parsed_string):
    data = OrderedDict()
    for (value, key) in parsed_string:
        if key not in data:
            data[key] = value
    return data

def process_excel_file(excel_file_in, excel_file_out):
    data = pd.read_excel(excel_file_in)
    column_headers = list(data.columns.values)
    if COLUMN_NAME in column_headers:
        col_id = column_headers.index(COLUMN_NAME)
    else:
        col_id = 0
        print("Warning: No column named {} found. Using first column.".format(COLUMN_NAME))

    col_name = column_headers[col_id]

    parsed_data = pd.DataFrame()
    for address in data[col_name]:
        try:
            tagged_address, address_type = usaddress.tag(address)
        except usaddress.RepeatedLabelError as e:
            print("Error:")
            print(e.parsed_string, e.original_string)
            tagged_address = recover_misparsed(e.parsed_string)

        parsed_data = pd.concat([parsed_data, pd.DataFrame(tagged_address, index=[0])])
    parsed_data.to_excel(excel_file_out, index=False)

def run():

    parser = argparse.ArgumentParser(description='Parse addresses in Excel file.')
    parser.add_argument('file', metavar='file', type=str, nargs='?',
                        help='File to parse')

    args = parser.parse_args()
    if args.file is not None:
        excel_file = args.file
    else:
        excel_file = askopenfilename()

    (base, ext) = os.path.splitext(os.path.basename(excel_file))
    excel_file_out = os.path.join(os.path.dirname(excel_file), base + "_parsed" + ext)
    process_excel_file(excel_file, excel_file_out)


if __name__ == "__main__":
    run()