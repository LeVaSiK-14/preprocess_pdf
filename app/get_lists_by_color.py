import cv2
import numpy as np
from app.utils.process_dirs import(
    get_dirs_from_dir,
    get_files_from_dir,
    get_full_path,
)
from app.utils.timer import(
    measure_time,
)
from app.utils.utils import(
    create_dirs_by_color,
)
from app.utils.configs import(
    BLUE, RED, PINK,
    ORANGE, GREEN,
)

@measure_time
def get_lists_by_color(png_lists_without_tables_dir_path: str, png_lists_by_color_path: str, colors: list) -> None:
    png_dirs = get_dirs_from_dir(png_lists_without_tables_dir_path)

    for png_dir in png_dirs:
        png_dir_path = get_full_path(png_lists_without_tables_dir_path, png_dir)
        png_lists = get_files_from_dir(png_dir_path)


        color_folders = create_dirs_by_color(
            png_lists_by_color_dir_path=png_lists_by_color_path,
            folder_name=png_dir,
            colors=colors
        )

        for i, png_list in enumerate(png_lists):
            png_list_path = get_full_path(png_dir_path, png_list)

            image = cv2.imread(png_list_path)

            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            lower_blue = np.array([100, 150, 150])
            upper_blue = np.array([140, 255, 255])


            lower_red1 = np.array([0, 150, 150])
            upper_red1 = np.array([10, 255, 255])
            lower_red2 = np.array([170, 150, 150])
            upper_red2 = np.array([180, 255, 255])


            lower_pink = np.array([135, 50, 50])  
            upper_pink = np.array([179, 255, 255])


            mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
            mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)

            mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
            mask_red = cv2.bitwise_or(mask_red1, mask_red2)
            mask_pink = cv2.inRange(hsv, lower_pink, upper_pink)


            result_blue = cv2.bitwise_and(image, image, mask=mask_blue)
            result_red = cv2.bitwise_and(image, image, mask=mask_red)
            result_pink = cv2.bitwise_and(image, image, mask=mask_pink)


            result_blue[mask_blue == 0] = [255, 255, 255]
            result_red[mask_red == 0] = [255, 255, 255]
            result_pink[mask_pink == 0] = [255, 255, 255]

            for color, dir_path in color_folders.items():
                if color == BLUE:
                    cv2.imwrite(f'{dir_path}/{color}_{png_list}', result_blue)
                elif color == RED:
                    cv2.imwrite(f'{dir_path}/{color}_{png_list}', result_red)
                elif color == PINK:
                    cv2.imwrite(f'{dir_path}/{color}_{png_list}', result_pink)
