import csv

from dataclasses import dataclass
from pathlib import Path, PosixPath
from typing import Optional


class FileInterface:
    """ basic parameters of files interfaces"""

    def __init__(self,
                 file_dir: str,
                 file_pattern: str,
                 column_map: dict,
                 ) -> None:
        self.file_dir = file_dir
        self.file_pattern = file_pattern
        self.column_map = column_map

    def parse(self):
        raise NotImplementedError


class CsvInterface(FileInterface):
    def parse(self):
        file_list = sorted(Path(self.file_dir).glob(self.file_pattern))
        return [
            {
                "file_path": file,
                "transactions": self._parse(file)
            } for file in file_list
        ]

    def _parse(self, file_path: PosixPath):
        transactions = []
        with file_path.open('r') as f:
            for row in csv.DictReader(f):
                transactions.append(
                    {
                        key: row[value]
                        for key, value in self.column_map.items()
                    }
                )
        return transactions


class PdfInterface(FileInterface):
    pass
