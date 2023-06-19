from device_client import Device
import cv2
import pytesseract
from pytesseract import Output
import numpy as np
import logging


def get_letters(img):
    img = img.copy()
    start_row = int(2 * img.shape[0] / 3)
    sides_width = int(img.shape[1]/6)


    img[:start_row, :] = [0, 0, 0] # Make the top 2/3 of the image black
    img[:, :sides_width] = [0, 0, 0] # Make the sides of the image black
    img[:, -sides_width:] = [0, 0, 0] # Make the sides of the image black

    white_pixels = np.all(img[start_row:, :] == [255, 255, 255], axis=-1)
    img[start_row:, :][~white_pixels] = [0, 0, 0]
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    letters = dict()

    for contour in contours:
        # Get bounding box for each contour
        x, y, w, h = cv2.boundingRect(contour)

        # Extract each character using the bounding rectangle
        character = img[y-30:y + h + 30, x-30:x + w+30]
        character = 255-character
        #cv2.imshow('char', character)
        #cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Use Tesseract to decode the character
        config = ("--psm 13, -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        text = pytesseract.image_to_string(character, config=config).strip()

        if len(text) > 1:
            logging.warning(f'Length of character was greater than 1 for: {text}')
        char = text[0]
        if char not in letters:
            letters[char] = []
        letters[char].append((x+h/2, y+w/2)) # divide width/height by 2 to get center of characters
    return letters

def get_word_lengths(img):
    img = img.copy()

    start_row = int(img.shape[0] / 10)
    end_row = int(6.5 * img.shape[0] / 10)

    img[:start_row, :] = [0, 0, 0]  # Make the top 1/10 of the image black
    img[end_row:, :] = [0, 0, 0]  # Make the bottom 35% of the image black

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgblur = cv2.medianBlur(img, 5)

    _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    img = cv2.resize(img, (500, 900))


    contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)



    cells = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        #print(x, y, w, h)
        if 50 < w*h < 40000 and 0.8 <  w / h < 1.2:
            cells.append((x, y, w, h))
    cell_width = sum([d[2] for d in cells]) / len(cells)
    cell_height = sum([d[3] for d in cells]) / len(cells)

    positions = []
    for cell in cells:
        x = round(cell[0] / cell_width)
        y = round(cell[1] / cell_height)
        positions.append((x, y))
        #pos_dict[(x, y)] = cell
    #positions.sort(key=lambda x: (x[0], x[1]))

    word_lengths = {}

    def find_run_lengths(positions):

        visited = set()
        for position in positions:
            if position not in visited:
                visited.add(position)
                x = position[0]
                bottom_y = top_y = position[1]
                while True:
                    if (x, bottom_y-1) in positions:
                        bottom_y -= 1
                        visited.add((x, bottom_y))
                    elif (x, top_y+1) in positions:
                        top_y += 1
                        visited.add((x, top_y))
                    else:
                        break
                length = abs(bottom_y-top_y)+1

                if length > 2:
                    if length not in word_lengths:
                        word_lengths[length] = 0
                    word_lengths[length] += 1

    find_run_lengths(positions)
    find_run_lengths([(pos[1], pos[0]) for pos in positions]) # reverse x and y to find runs on other axis

    return word_lengths