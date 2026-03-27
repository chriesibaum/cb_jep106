__author__ = "Thomas, Thomas@chriesibaum.dev"
__copyright__ = "Copyright 2025, Chriesibaum GmbH"

import enum
import pymupdf
import re
import argparse
import json


class DecodeStates(enum.Enum):
    """
    State machine states for JEP106 PDF decoding.
    """

    LOOKING_FOR_BANK = 1
    LOOKING_FOR_INDEX_MANU = 2
    DONE = 3


def process_jep106_pdf(jep106_pdf_file):
    """Process JEP106x.pdf and write results to jep106.csv."""
    bank = 1
    state = DecodeStates.LOOKING_FOR_INDEX_MANU

    doc = pymupdf.open(jep106_pdf_file)
    p_index_manu = re.compile(r'(?P<index>\d{1,3})  (?P<manufacturer>.+)')

    print('Processing JEP106 PDF: ')
    print(f'Bank: {bank}', end='', flush=True)

    jep106_data = {}

    for page in doc:
        text = page.get_text()

        for line in text.splitlines():
            line = line.strip()

            # Skip empty lines
            if line == '':
                continue

            # Look for end of relevant content "Annex A"
            if line.startswith('Annex A'):
                print(' - Done.')
                state = DecodeStates.DONE
                break

            # Look for the next bank header
            if state == DecodeStates.LOOKING_FOR_BANK:
                if line.startswith('The following numbers are all in bank'):
                    bank += 1
                    print(f' {bank}', end='', flush=True)
                    state = DecodeStates.LOOKING_FOR_INDEX_MANU
                    continue

            # Look for index/manufacturer lines and decode them
            elif state == DecodeStates.LOOKING_FOR_INDEX_MANU:
                m = p_index_manu.search(line)
                if m:
                    index = int(m.group('index'))
                    manufacturer = m.group('manufacturer')

                    jedec = (bank - 1) * 128 + index

                    d = {
                        'Bank': bank,
                        'Index': index,
                        '11-bit-JEDEC-Code': jedec,
                        'Manufacturer': manufacturer,
                    }
                    jep106_data[jedec] = d

                    if index >= 126:
                        state = DecodeStates.LOOKING_FOR_BANK

        # Check if we should stop after processing this page
        if state == DecodeStates.DONE:
            return jep106_data

    # If we reach here, we have processed all pages without finding "Annex A"
    # This likely means the PDF format has changed or the file is corrupted

    raise ValueError('Reached end of PDF without finding "Annex A". '
                     'The PDF format may have changed or the file may be corrupted.') \
        # pragma: no cover


def write_jep106_csv(jep106_data, jep106_csv_file):
    print(f'Writing JEP106 data to CSV file: {jep106_csv_file}')
    with open(jep106_csv_file, 'w', encoding='utf-8') as f_csv:
        f_csv.write('Bank,Index,11-bit-JEDEC-Code,Manufacturer\n')
        for jedec in sorted(jep106_data.keys()):
            d = jep106_data[jedec]
            f_csv.write(f'{d["Bank"]:3d}, '
                        f'{d["Index"]:3d}, '
                        f'{d["11-bit-JEDEC-Code"]:#05x}, '
                        f'"{d["Manufacturer"]}"\n')


def write_jep106_json(jep106_data, jep106_json_file):
    print(f'Writing JEP106 data to JSON file: {jep106_json_file}')
    with open(jep106_json_file, 'w', encoding='utf-8') as f_json:
        json.dump(jep106_data, f_json, indent=4, ensure_ascii=False)


__usage__ = \
    """Decode the Standard Manufacturer’s Identification Code PDF file (JEP106xx.pdf)
and generate machine readable output like a CSV or JSON file.

Note:
As the JEP106xx.pdf is not free to use, it is not included in the repository but
can be used by downloading the JEP106xx.pdf from JEDEC and running this script locally.
At the time of writing, the actual JEP106BN.pdf can be found at
https://www.jedec.org/standards-documents/docs/jep-106ab.

Finally, have fun with the JEP106 data! :)"""


def main():
    parser = argparse.ArgumentParser(
        description=__usage__,
        epilog='  At least one output must be provided: `-c/--csv` or `-j/--json`.',
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        '-i', '--pdf',
        metavar='<JEP106xx.pdf>',
        default='./JEP106/JEP106BN.pdf',
        help='Path to input JEP106 PDF file (default: ./JEP106/JEP106BN.pdf)')
    parser.add_argument(
        '-c', '--csv',
        metavar='<csv file>',
        default=None,
        help='Path to output CSV file')
    parser.add_argument(
        '-j', '--json',
        metavar='<json file>',
        default=None,
        help='Path to output JSON file')

    args = parser.parse_args()

    if not args.csv and not args.json:
        parser.error('at least one output option must be specified: -c/--csv or -j/--json')

    jep106_pdf_file = args.pdf
    jep106_csv_file = args.csv
    jep106_json_file = args.json

    # process the PDF and extract the JEP106 data
    jep106_data = process_jep106_pdf(jep106_pdf_file)

    if jep106_csv_file:
        write_jep106_csv(jep106_data, jep106_csv_file)

    if jep106_json_file:
        write_jep106_json(jep106_data, jep106_json_file)


if __name__ == '__main__':  # pragma: no cover
    main()
