import cv2
import pytesseract
from pytesseract import Output
import os
from ocr import preprocess_image as pi


def preprocess(image):
    gray = pi.get_grayscale(image)
    thresh = pi.thresholding(gray)
    opening = pi.opening(gray)
    canny = pi.canny(gray)
    return gray, thresh, opening, canny


def get_image_data(image):
    return pytesseract.image_to_data(image, output_type=Output.DICT)


def plot_box_for_words(image, word_dict):
    n_boxes = len(word_dict['text'])
    for i in range(n_boxes):
        text = word_dict['text'][i]
        if int(word_dict['conf'][i]) > 60:
            text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
            (x, y, w, h) = (word_dict['left'][i], word_dict['top'][i], word_dict['width'][i], word_dict['height'][i])
            image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 200), 2)
    return image


if __name__ == "__main__":
    image_path = os.path.join("data", "Image-1.jpg")
    img = cv2.imread(image_path)

    word_coordinate = get_image_data(img)
    print(word_coordinate)
    img = plot_box_for_words(img, word_coordinate)
    cv2.imshow('original_image', img)
    cv2.waitKey(5000)
