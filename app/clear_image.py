import cv2
import numpy as np
from tqdm import tqdm
from app.utils.get_file_name import(
    get_file_name,
)
from app.utils.process_dirs import(
    create_dir,
    get_full_path,
    get_files_from_dir,
    get_dirs_from_dir,
)
from app.utils.timer import(
    measure_time,
)


@measure_time
def filter_colors(input_image_path: str, output_image_path: str) -> None:
    """
    Фильтрует изображение, оставляя только пиксели, принадлежащие к четырём цветовым диапазонам:
    синий, красный, розовый и чёрный. Все остальные пиксели заменяются на белый.
    
    :param input_image_path: путь к исходному изображению.
    :param output_image_path: путь для сохранения обработанного изображения.
    """
    
    png_dirs = get_dirs_from_dir(input_image_path)
    
    for png_dir in png_dirs:
        png_dir_path = get_full_path(input_image_path, png_dir)
        png_lists = get_files_from_dir(png_dir_path)
        
        result_dir_path = get_full_path(output_image_path, png_dir)
        create_dir(result_dir_path)
        
        for img in tqdm(png_lists):
            image_path = get_full_path(png_dir_path, img)
            image_name = get_file_name(image_path)
            image = cv2.imread(image_path)
            if image is None:
                print(f"Не удалось открыть изображение: {image_path}")
                return
            
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            lower_blue = np.array([100, 150, 150])
            upper_blue = np.array([140, 255, 255])
            
            lower_red1 = np.array([0, 150, 150])
            upper_red1 = np.array([10, 255, 255])
            lower_red2 = np.array([170, 150, 150])
            upper_red2 = np.array([180, 255, 255])
            
            lower_pink = np.array([135, 50, 50])
            upper_pink = np.array([179, 255, 255])
            
            lower_black = np.array([0, 0, 0])
            upper_black = np.array([180, 255, 50]) 
            
            mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
            
            mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
            mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
            mask_red = cv2.bitwise_or(mask_red1, mask_red2)
            
            mask_pink = cv2.inRange(hsv, lower_pink, upper_pink)
            
            mask_black = cv2.inRange(hsv, lower_black, upper_black)
            
            mask_combined = cv2.bitwise_or(mask_blue, mask_red)
            # mask_combined = cv2.bitwise_or(mask_combined, mask_pink)
            # mask_combined = cv2.bitwise_or(mask_combined, mask_black)
            
            result = cv2.bitwise_and(image, image, mask=mask_combined)
            result[mask_combined == 0] = [255, 255, 255]
            
            result_png_name_path = get_full_path(result_dir_path, image_name)
            cv2.imwrite(f'{result_png_name_path}.png', result)
