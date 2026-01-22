import cv2
import glob
import json
import easyocr
import numpy as np

from preprocess import preprocess_image


FOLDER_PATH = ".\\marksheets"


def load_marksheets(PATH):
    #Loading all image files in the PATH folder

    image_list = glob.glob(PATH + "\\*.webp")

    images = []

    for image_path in image_list:
        image = cv2.imread(image_path)

        if image is not None:
            images.append(image)
    

    return images

def perform_ocr(images):
    #Performing ocr

    reader = easyocr.Reader(['en', 'hi'])
    ocr_results = []

    for image in images:
        image_text = reader.readtext(image)

        if image_text is not None:
            ocr_results.append(image_text)

    return ocr_results

def preprocess(images):
    #Preprocessing all images

    processed_images = []

    for image in images:
        processed_images.append(preprocess_image(image))

    return processed_images    


def main():

    images = preprocess(load_marksheets(FOLDER_PATH))

    ocr_result = perform_ocr(images)

    print(ocr_result)

    return


if __name__ == "__main__":
    main()