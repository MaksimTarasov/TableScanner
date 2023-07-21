"""

"""
import os
from typing import List
from imutils import contours
import numpy as np
import cv2 as cv


class GetTextArea:
    """
     Класс получает координаты ячеек в картинке, для дальнейшего определения текста
    """
    def __init__(self):
        # self.__filepath = filepath
        pass
    # олучает на вход путь и тип файла, по умолчанию jpg
    # возвращает список файлов

    def __get_files(self, filepath: str, typeoffile='jpg') -> List:
        file_list = []
        try:
            file_list = [i for i in os.listdir(filepath + '/input') if i.endswith(typeoffile)]
            #TODO Продумать как передавать путь с подкаталогами каталогами,
            # так как сейчас подкаталаги загрузки и выгрузки забиты жестко
        except FileNotFoundError as error:
            print(f'{error}')
        return file_list

    def _load_img_new(self, filepath: str):
        # Поиск контуров с помощью алгоритма Canny
        filelist = self.__get_files(filepath=filepath)
        print(filelist)
        # out_count = filepath + 'out_cont/' + ifile
        # print(out_count)
        coords_dict = dict()
        # Чтение файла
        for ifile in filelist:
            img = cv.imread(cv.samples.findFile(filepath + 'input/' + ifile))
            out_mini = filepath + 'out_mini/' + ifile
            print(out_mini)
            # Подготовка изображения,  размытие, перевод в серый, первеод в Ч/Б
            img = cv.blur(img, (5, 5))
            img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            ret, img = cv.threshold(img, 170, 255, 0)
            cv.imwrite(f'{out_mini}', img)#Сохранение обработанного файла

            ## изменение размера
            # w = img3.shape[0]
            # new_w = 1620
            # k = new_w / w
            # new_size = (new_w, int(img3.shape[1] * k))
            # img3 = cv.resize(img3, new_size, interpolation = cv.INTER_AREA)
            # Определение границ алгоритмом Canny
            e = cv.Canny(img, 10, 600, L2gradient=False)

            # Поиск контуров
            my_contours, hierarchy = cv.findContours(e, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            # сортировки контуров, my_contours - массив контуров,
            # f - прямоугольники построенные по контурам
            (my_contours, f) = contours.sort_contours(my_contours)#, method="top-to-bottom")
            # (my_contours, f) = contours.sort_contours(my_contours, method="left-to-right")

            # ---======= Поиск нужных контуров====----------
            img = cv.cvtColor(img, cv.COLOR_GRAY2RGB)
            mask = np.zeros(img.shape)

            # Отбор нужных контуров по размеру прямоугольников полного изображения
            f2 = list(set(filter(lambda k: k[2] * k[3] > 11000 and k[2] * k[3] < 1196980, f)))
            f2 = sorted(f2, key=lambda x: x[0])
            # Отбор нужных контуров по размеру прямоугольников уменьшенного изображения
            # f2 = list(filter(lambda k: k[2]*k[3]>2200 and k[2]*k[3]< 1196980, f))
            # сохраняем контура в словаре
            coords_dict[out_mini] = f2[:]

            # Прорисовка контуров для контроля
            for i, i_cnt in enumerate(f2):
                l, t, w, h = i_cnt
                cv.putText(img, f'{i}', (l+5, t+20), cv.FONT_HERSHEY_TRIPLEX, 1, (255, 100, 0))
                cv.rectangle(img, (l, t), (l+w, t+h), (0, 0, 255), 2)
                cv.putText(mask, f'W:{w} x H:{h}',
                           (l+5, t+20),
                           cv.FONT_HERSHEY_TRIPLEX,
                           0.5, (255, 100, 0))
                cv.putText(mask, f'L:{l} x T:{t}',
                           (l+5, t+60),
                           cv.FONT_HERSHEY_TRIPLEX,
                           0.5, (255, 100, 0))
                cv.rectangle(mask, (l, t), (l+w, t+h), (0, 0, 255), 2)
                # Сохранение изображения с контурами
                cv.imwrite(f'{out_mini}_cont.jpg', img)
                cv.imwrite(f'{out_mini}_cont_mask.jpg', mask)
        return coords_dict
