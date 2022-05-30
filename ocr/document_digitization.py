import cv2
import pytesseract
from pytesseract import Output
import os
from ocr import preprocess_image as pi
from _helper import text


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


def image_to_text(image):
    return pytesseract.image_to_string(image, config='-c preserve_interword_spaces=1x1 --psm 1 --oem 3')


if __name__ == "__main__":
    sel_file = "1.png"
    image_path = os.path.join("data", f"{sel_file}")
    img = cv2.imread(image_path)
    img = pi.get_grayscale(img)

    word_coordinate = get_image_data(img)
    # print(word_coordinate)
    process_img = plot_box_for_words(img, word_coordinate)
    cv2.imshow(f'{sel_file}_image', process_img)
    cv2.waitKey(5000)

    # Reading image again for image to doc conversion
    img = cv2.imread(image_path)
    text_data = image_to_text(img)
    text.write_text_file(text_data, f"{sel_file}.txt")

    # gray, thresh, _, _ = preprocess(img)
    # word_coordinate = get_image_data(gray)
    # print(word_coordinate)
    # img = plot_box_for_words(gray, word_coordinate)
    # cv2.imshow('gray_image', img)
    # cv2.waitKey(5000)
    #
    # word_coordinate = get_image_data(thresh)
    # print(word_coordinate)
    # img = plot_box_for_words(thresh, word_coordinate)
    # cv2.imshow('thresh_image', img)
    # cv2.waitKey(5000)
