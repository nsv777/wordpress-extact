import os
import re
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


class UrlParse(object):
    def __init__(self, url, basic_dirpath):
        req_get = requests.Session().get(url=url)
        self.url = url
        self.base_url = self._get_base_url(url=url)
        soup = BeautifulSoup(req_get.content, "lxml")
        self.div_tovar = soup.find("div", {"class": "tovar"})
        self.dirpath = self._get_dirpath(url=url, basic_dirpath=basic_dirpath)

    @staticmethod
    def _get_base_url(url):
        parsed_url = urlparse(url)
        return "{}://{}".format(parsed_url.scheme, parsed_url.netloc)

    def get_images_list(self):
        img_list = list()
        for dt in self.div_tovar.find_all("dt", {"class": "gallery-icon"}):
            a_href = dt.find("a").attrs.get("href", None)
            if a_href:
                img_list.append(a_href)

        # for img in self.div_tovar.findAll("img"):
        #     img_src = img.attrs.get("src", None)
        #     if "/wp-content/" in img_src:
        #         img_list.append(img_src)
        #
        #     img_srcset = img.attrs.get("srcset", None)
        #     if img_srcset is not None:
        #         for srcset_item in re.findall(r'(https?://\S+)', img_srcset):
        #             img_list.append(srcset_item)

        for img in self.div_tovar.find_all("img", {"class": ["aligncenter", "size-full"]}):
            img_src = img.attrs.get("src", None)
            if "/wp-content/" in img_src:
                img_list.append(img_src)

        return img_list

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
        stripped_text = self.get_stripped_soup_text(self.div_tovar)
        with open(filename, 'w') as text_file:
            text_file.write(stripped_text)
        return stripped_text

    def download_images(self):
        img_list = self.get_images_list()
        for img_url in img_list:
            if self.base_url not in img_url:
                img_url = self.base_url + img_url
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
        body = self.get_stripped_soup_text(self.div_tovar)
        for line in body.splitlines():
            for body_pattern in body_patterns:
                if not row.get(body_pattern[0], None):
                    match = re.search(body_pattern[1], line, flags=re.IGNORECASE)
                    if match:
                        row[body_pattern[0]] = match.group(1)
                    else:
                        row[body_pattern[0]] = ""

        row["Картинки"] = "{}".format(",".join(self.get_images_list()[1:]))

        description = ""
        for line in self.div_tovar.find_all("p"):
            description += line.text
        row["Описание"] = self.get_stripped_text(multiline_text=description)

        return row
