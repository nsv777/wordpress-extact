import json
import os
import re
from pathlib import Path
from urllib.parse import urlparse, urljoin

import requests
from bs4 import BeautifulSoup


class UrlParse(object):
    def __init__(self, url: str, basic_dirpath: str, find_attrs: json, item_number=0):
        self.url = url
        self.base_url = self._get_base_url(url=url)
        self.div_item = self._get_div_item(find_attrs=find_attrs, item_number=item_number)
        self.dirpath = self._get_dirpath(url=url, basic_dirpath=basic_dirpath)

    def _get_div_item(self, find_attrs: json, item_number: int):
        req_get = requests.Session().get(url=self.url)
        soup = BeautifulSoup(req_get.content, "lxml")
        return soup.find_all(name="div", attrs=find_attrs)[item_number]

    @staticmethod
    def _get_base_url(url):
        parsed_url = urlparse(url)
        return "{}://{}".format(parsed_url.scheme, parsed_url.netloc)

    def _get_full_img_url(self, img_url):
        if self.base_url not in img_url:
            img_url = urljoin(self.base_url, img_url)
        return img_url

    def get_images_list(self):
        img_list = list()

        # -------------------------------------------------
        # Replace with your own logic
        for img in self.div_item.find_all(name="img"):
            img_src = img.attrs.get("src", None)
            if img_src:
                img_list.append(img_src)
        # -------------------------------------------------

        checked_img_list = list()
        for img_src in img_list:
            img_src = self._get_full_img_url(img_src)
            checked_img_list.append(img_src)

        return checked_img_list

    @staticmethod
    def get_stripped_text(multiline_text):
        stripped_text = ""
        for line in multiline_text.splitlines():
            line.strip()
            if line != "" and not re.match(r'^\s+$', line):
                stripped_text += "{}\n".format(line)
        return stripped_text

    def get_stripped_soup_text(self, soup):
        return self.get_stripped_text(soup.text)

    def download_text(self):
        filename = Path.joinpath(self.dirpath, "text.txt")
        # print("Saving text to {}".format(filename))
        stripped_text = self.get_stripped_soup_text(self.div_item)
        with open(filename, 'w') as text_file:
            text_file.write(stripped_text)
        return stripped_text

    def download_images(self):
        img_list = self.get_images_list()
        for img_url in img_list:
            self.download_image(image_url=img_url, dirpath=self.dirpath)

    @staticmethod
    def download_image(image_url, dirpath):
        filename = os.path.basename(urlparse(image_url).path)
        with requests.get(image_url, stream=True) as r:
            r.raise_for_status()
            with open(Path.joinpath(dirpath, filename), 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
        return filename

    @staticmethod
    def _get_dirpath(url, basic_dirpath):
        parsed_url = urlparse(url)
        dirpath = Path(basic_dirpath, parsed_url.netloc, parsed_url.path.replace('/', '_'))
        # if dirpath and dirpath.exists():
        #     shutil.rmtree(dirpath)
        #     dirpath.mkdir()
        if dirpath:
            dirpath.mkdir(parents=True, exist_ok=True)
        return dirpath

    def get_row(self, body_patterns):
        row = dict()
        row["url"] = self.url
        body = self.get_stripped_soup_text(self.div_item)
        for line in body.splitlines():
            try:
                for body_pattern in body_patterns:
                    if not row.get(body_pattern[0], None):
                        match = re.search(body_pattern[1], line, flags=re.IGNORECASE)
                        if match:
                            row[body_pattern[0]] = match.group(1).strip()
                        else:
                            row[body_pattern[0]] = ""
            except TypeError:  # no body patterns
                pass
        row["Картинки"] = "{}".format(",".join(self.get_images_list()[1:]))

        description = ""
        for line in self.div_item.find_all("p"):
            description += line.text
        row["Описание"] = self.get_stripped_text(multiline_text=description)

        return row
