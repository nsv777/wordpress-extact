import json
import sys
from datetime import datetime
from pathlib import Path

from classes.excel_file import ExcelFile
from classes.url_parse import UrlParse


def get_basic_dirpath(timestamp=None):
    if not timestamp:
        timestamp = str(datetime.now().strftime('%Y%m%d_%H%M%S'))
    basic_dirpath = Path(
        Path.home(),
        'Downloads',
        'wordpress-parse',
        timestamp
    )
    # if dirpath and dirpath.exists():
    #     shutil.rmtree(dirpath)
    #     dirpath.mkdir()
    if basic_dirpath:
        basic_dirpath.mkdir(parents=True, exist_ok=True)
    return basic_dirpath


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
    with open('config.json', 'r') as f:
        config = json.load(f)

    for url in url_list:
        url = url.strip()
        print(url)
        url_parse = UrlParse(url=url, basic_dirpath=basic_dirpath)
        url_parse.download_text()
        url_parse.download_images()
        row = url_parse.get_row(body_patterns=config.get("body_patterns"))
        if not is_header:
            excel_file.add_row(list(row.keys()))
            is_header = True
        excel_file.add_row(list(row.values()))
        # print(row)
    excel_file.save()


if __name__ == '__main__':
    main()
