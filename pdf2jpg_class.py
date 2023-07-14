import fitz
import os
from typing import List


class Pdf2Jpg:
    """
        Класс предназначен для извлечения картинки из pdf,
        если pdf файл  является просто сканом листа.
    """
    def __init__(self, filepath: str, outpath: str = None):
        self._filepath = filepath
        self._outpath = outpath

    # Получает на вход путь и тип файла, по умолчанию pdf
    def __get_files(self, filepath: str, typeoffile='pdf') -> List:
        file_list = []
        try:
            file_list = [i for i in os.listdir(filepath) if i.endswith(typeoffile)]
        except FileNotFoundError as error:
            print(f'{error}')
        return file_list

    def convert(self, typeoffile='pdf'):
        file_list = self.__get_files(self._filepath, typeoffile)
        if file_list:
            for file in file_list:
                file = self._filepath + file
                print(f'{file}')
                with fitz.open(file) as doc:
                    # page_count = 0  TODO Удалить, если не вспомню заачем ее хотел использовать.
                    p = doc.get_page_images(0)
                    pix = fitz.Pixmap(doc, p[0][0])
                    pix1 = fitz.Pixmap(fitz.csRGB, pix)
                    pix1.pil_save(file.replace('pdf', 'jpg'))



