import sys
from pathlib import Path

from common.excel_file import ExcelFile
from common.url_parse import UrlParse
from common.utils import get_basic_dirpath

BODY_PATTERNS = None


class MyUrlParse(UrlParse):
    def __init__(self, url, basic_dirpath, find_attrs, item_number):
        super().__init__(url, basic_dirpath, find_attrs, item_number)

    def get_images_list(self):
        img_list = list()
        # -------------------------------------------------
        elements = (
            ("div", {"class": "gallery_items"}),
        )
        for element in elements:
            item = self.div_item.find(name=element[0], attrs=element[1])
            for a in item.find_all(name="a"):
                a_href = a.get("href", None)
                if a_href:
                    img_list.append(a_href)
        # -------------------------------------------------
        checked_img_list = list()
        for img_src in img_list:
            img_src = self._get_full_img_url(img_src)
            checked_img_list.append(img_src)

        return checked_img_list


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
        url_parse = MyUrlParse(
            url=url,
            basic_dirpath=basic_dirpath,
            find_attrs={"id": "cnt_wrap"},
            item_number=0
        )
        url_parse.download_text()
        url_parse.download_images()
        row = url_parse.get_row(body_patterns=BODY_PATTERNS)
        if not is_header:
            excel_file.add_row(list(row.keys()))
            is_header = True
        excel_file.add_row(list(row.values()))
        # print(row)
    excel_file.save()


if __name__ == '__main__':
    main()
