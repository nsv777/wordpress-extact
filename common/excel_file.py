from datetime import datetime
from pathlib import Path

from openpyxl import Workbook


class ExcelFile(object):
    def __init__(self, path, filename=None):
        self.book = Workbook()
        self.sheet = self.book.worksheets[0]
        self.filename = self.get_filename(filename, path)
        self.save()

    def save(self):
        self.book.save(filename=self.filename)

    @staticmethod
    def get_filename(filename, path):
        timestamp = (str(datetime.now().strftime('%Y%m%d_%H%M%S')))
        ext = "xlsx"
        if filename is not None:
            return Path.joinpath(
                path,
                "{}_{}.{}".format(Path(filename).stem, timestamp, ext)
            )
        return Path.joinpath(path, "data_{}.{}".format(timestamp, ext))

    def add_row(self, row):
        self.sheet.append(row)
