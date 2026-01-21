import cv2
import numpy as np
import matplotlib.pyplot as plt


def correct_illumination(img):
    #CLAHE (adaptive histogram equalisation)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    return clahe.apdeply(img)


def denoise(img):
    #Median blur (salt and pepper noise removal)

    return cv2.medianBlur(img, ksize=3)


def grayscale_it(img):

    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def correct_perspective(img):

    #Canny edge detection + Hough transform

    # edges = cv2.Canny(img, 50, 160, apertureSize=3)

    # lines = cv2.HoughLinesP(edges, 1, np.pi/180,
    #                         threshold=50,
    #                         minLineLength=int(0.2*min(img.shape[:2])),
    #                         maxLineGap=60)
    # if lines is None:
    #     return img

    pass