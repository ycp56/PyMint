from dataclasses import dataclass
from typing import Optional


@dataclass
class FileInterface:
    """ basic parameters of files interfaces"""
    file_dir: str
    file_pattern: str
    column_map: dict

    def parse(self):
        raise NotImplementedError
     

class CsvInterface(FileInterface):
    pass 


class PdfInterface(FileInterface):
    pass