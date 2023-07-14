from typing import List
import os
import fitz
from typing import List, Dict
import cv2 as cv
import numpy as np
from imutils import contours
from typing import List
import os
import easyocr
from pdf2jpg_class import Pdf2Jpg

if __name__ == '__main__':
    p2j = Pdf2Jpg('data/input/')
    p2j.convert()