import cv2
import numpy as np
from tqdm import tqdm

from app.utils.get_file_name import get_file_name
from app.utils.process_dirs import create_dir, get_full_path, get_files_from_dir, get_dirs_from_dir
from app.utils.timer import measure_time


@measure_time
def remove_gray(input_image_path: str, output_image_path: str) -> None:
    """
    Затирает белым только светло‑серые пиксели: S < saturation_threshold и V >= value_threshold.
    """
    png_dirs = get_dirs_from_dir(input_image_path)
    for png_dir in png_dirs:
        png_dir_path = get_full_path(input_image_path, png_dir)
        png_lists = get_files_from_dir(png_dir_path)
        result_dir_path = get_full_path(output_image_path, png_dir)
        create_dir(result_dir_path)

        for img_name in tqdm(png_lists):
            image_path = get_full_path(png_dir_path, img_name)
            img = cv2.imread(image_path) 

            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            lower_gray = np.array([0, 0, 80])
            upper_gray = np.array([179, 60, 220])

            mask = cv2.inRange(hsv, lower_gray, upper_gray)

            mask_inv = cv2.bitwise_not(mask)

            result = cv2.bitwise_and(img, img, mask=mask_inv)
            white_background = np.full(img.shape, 255, dtype=np.uint8)
            final = cv2.bitwise_or(result, cv2.bitwise_and(white_background, white_background, mask=mask))

            out_path = get_full_path(result_dir_path, get_file_name(image_path)) + '.png'
            cv2.imwrite(out_path, final)
