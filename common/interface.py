import csv

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path, PosixPath
from typing import Optional, List


class FileInterface:
    """ basic parameters of files interfaces"""

    def __init__(self,
                 file_dir: str,
                 file_pattern: str,
                 column_map: dict,
                 datetime_format: str=None
                 ) -> None:
        self.file_dir = file_dir
        self.file_pattern = file_pattern
        self.column_map = column_map
        self.datetime_format = datetime_format

    def parse(self):
        raise NotImplementedError


class CsvInterface(FileInterface):
    def parse(self) -> List[dict]:
        file_list = sorted(Path(self.file_dir).glob(self.file_pattern))
        return [
            {
                "file_path": file,
                "transactions": self._parse(file)
            } for file in file_list
        ]

    def _parse(self, file_path: PosixPath) -> List[dict]:
        transactions = []
        with file_path.open('r') as f:
            for row in csv.DictReader(f):
                transactions.append(
                    {
                        normalized_col: self._format(normalized_col, row[value])
                        for normalized_col, value in self.column_map.items()
                    }
                )
        return transactions

    def _format(self, normalized_column, value):
        if (normalized_column == 'date') and (self.datetime_format != None):
            return datetime.strptime(value, self.datetime_format)
        else:
            return value
        


class PdfInterface(FileInterface):
    pass
