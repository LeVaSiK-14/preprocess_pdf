import cv2
import numpy as np
from tqdm import tqdm

from app.utils.get_file_name import get_file_name
from app.utils.process_dirs import create_dir, get_full_path, get_files_from_dir, get_dirs_from_dir
from app.utils.timer import measure_time

@measure_time
def remove_gray(input_image_path: str, output_image_path: str, saturation_threshold=30) -> None:
    """
    Удаляет (заменяет на белый) все пиксели, у которых низкая насыщенность (S) в HSV,
    то есть они близки к серому цвету. Остальные цвета сохраняет.
    
    :param input_image_path: путь к директории с входными изображениями (с подпапками).
    :param output_image_path: путь к директории, куда сохранять результат (с той же структурой подпапок).
    :param saturation_threshold: порог, ниже которого пиксели считаются "серым" (0..255).
    """

    # Получаем список подпапок
    png_dirs = get_dirs_from_dir(input_image_path)
    
    for png_dir in png_dirs:
        png_dir_path = get_full_path(input_image_path, png_dir)
        png_lists = get_files_from_dir(png_dir_path)
        
        # Создаем выходную директорию аналогичной структуры
        result_dir_path = get_full_path(output_image_path, png_dir)
        create_dir(result_dir_path)
        
        for img in tqdm(png_lists):
            image_path = get_full_path(png_dir_path, img)
            image_name = get_file_name(image_path)
            image = cv2.imread(image_path)
            if image is None:
                print(f"Не удалось открыть изображение: {image_path}")
                continue  # пропускаем неудавшийся файл, но не выходим из функции
            
            # Переходим в HSV
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            # Маска "серых" пикселей: насыщенность S < saturation_threshold
            # H в [0..180], S в [0..255], V в [0..255] в OpenCV
            lower_gray = np.array([0, 0, 0])
            upper_gray = np.array([180, saturation_threshold, 255])
            
            # Получаем маску для "серых" (низкая насыщенность)
            mask_gray = cv2.inRange(hsv, lower_gray, upper_gray)
            
            # Копируем изображение для результата
            result = image.copy()
            # Все пиксели, попавшие в mask_gray, красим в белый
            result[mask_gray == 255] = [255, 255, 255]
            
            # Сохраняем результат
            result_png_name_path = get_full_path(result_dir_path, image_name)
            cv2.imwrite(f'{result_png_name_path}.png', result)
