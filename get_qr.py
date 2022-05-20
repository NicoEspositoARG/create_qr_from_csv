"""Script to convert URLs from CSV to QR as png files
    and create a resultant csv file with file name."""
# https://realpython.com/python-csv/
# https://towardsdatascience.com/generate-qrcode-with-python-in-5-lines-42eda283f325

import csv
import logging
import sys
import qrcode
from requests.utils import requote_uri

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(formatter)
logger.addHandler(stdout_handler)

_ = logger


def _create_file_name(raw_url):
    vendor_name = raw_url.split("utm_source=")[1]
    end_index = vendor_name.find(';')
    return vendor_name[:end_index]


def _create_qr_code(parsed_url, qr_file_name):
    """Creating an instance of qrcode"""

    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5)
    qr.add_data(parsed_url)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save(qr_file_name)


def process_csv_row(row, line):
    raw_url = str(row[0])
    _.info(f"Raw URL: {raw_url}")
    parsed_url = requote_uri(raw_url)
    _.info(f"Parsed URL: {parsed_url}")
    vendor_name = _create_file_name(raw_url)
    qr_file_name = f'images/{line}-{vendor_name}.png'
    _create_qr_code(parsed_url, qr_file_name)
    file_result_name = qr_file_name.split('images/')[1]
    return (parsed_url, file_result_name)


def process_file():
    with open('Vendedores TV.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        output_row = []
        with open('results.csv', mode='w') as result_file:
            results_writer = csv.writer(
                result_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in csv_reader:
                if line_count == 0:
                    _.info(f'Column names are {", ".join(row)}')
                    output_row = row
                else:
                    parsed_url, file_result_name = process_csv_row(
                        row, line_count)
                    output_row = [parsed_url, file_result_name]

                # if line_count == 3:
                #     break
                line_count += 1
                results_writer.writerow(output_row)

        _.info(f"TOTAL: {line_count}")


if __name__ == "__main__":
    process_file()
