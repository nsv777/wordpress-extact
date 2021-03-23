import sys
from pathlib import Path

from common.excel_file import ExcelFile
from common.url_parse import UrlParse
from common.utils import get_basic_dirpath


def main():
    if len(sys.argv) < 1 or not Path(sys.argv[1]).resolve().exists():
        raise ValueError(
            """
            Usage: python zakaz_mebel.py <url list file>
            Example: python zakaz_mebel.py /tmp/list.txt
            """
        )

    url_list_file = open(sys.argv[1], 'r')
    url_list = url_list_file.readlines()
    url_list_file.close()

    basic_dirpath = get_basic_dirpath()
    excel_file = ExcelFile(filename="excel_file", path=basic_dirpath)
    is_header = False

    for url in url_list:
        url = url.strip()
        print(url)
        url_parse = UrlParse(url=url, basic_dirpath=basic_dirpath, item_div_class="gallery-block-top")
        url_parse.download_text()
        url_parse.download_images()
        row = url_parse.get_row(body_patterns=None)
        if not is_header:
            excel_file.add_row(list(row.keys()))
            is_header = True
        excel_file.add_row(list(row.values()))
        # print(row)
    excel_file.save()


if __name__ == '__main__':
    main()
