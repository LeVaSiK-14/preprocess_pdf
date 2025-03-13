import cv2
import numpy as np
from app.utils.process_dirs import(
    get_full_path,
    get_dirs_from_dir,
    get_files_from_dir,
    create_dir,
)
from app.utils.timer import(
    measure_time,
)
from tqdm import tqdm


@measure_time
def crop_white_borders(png_lists_clear_dir_path: str, png_lists_croped_path: str, threshold: int = 250, margin: int = 20) -> None:
    """
    Обрезает белые поля вокруг содержимого на изображении, оставляя отступ margin пикселей от краёв.
    
    :param image_path: Путь к исходному изображению.
    :param output_path: Путь для сохранения обрезанного изображения.
    :param threshold: Порог яркости для определения «белого» (0..255).
    :param margin: Количество пикселей отступа, которое нужно оставить вокруг содержимого.
    """
    
    png_dirs_names = get_dirs_from_dir(png_lists_clear_dir_path)
    for pnd_dir_name in png_dirs_names:
        png_dir_name_path = get_full_path(png_lists_clear_dir_path, pnd_dir_name)
        png_lists_clear = get_files_from_dir(png_dir_name_path)
        
        png_croped_result_path = get_full_path(png_lists_croped_path, pnd_dir_name)
        create_dir(png_croped_result_path)
        
        for png_list_name in tqdm(png_lists_clear):
            
            png_list_name_full_path = get_full_path(png_dir_name_path, png_list_name)


            img = cv2.imread(png_list_name_full_path)
            
            # Переводим в градации серого
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Создаем маску: все пиксели с интенсивностью ниже порога считаются не-белыми
            mask = gray < threshold

            # Если все пиксели белые, обрезка не требуется
            if not np.any(mask):
                continue

            # Находим координаты всех не-белых пикселей
            coords = np.argwhere(mask)

            # Определяем минимальные и максимальные координаты
            y_min, x_min = coords.min(axis=0)
            y_max, x_max = coords.max(axis=0) + 1  # +1, чтобы включить край

            # Добавляем отступ, не выходя за границы изображения
            y_min = max(y_min - margin, 0)
            x_min = max(x_min - margin, 0)
            y_max = min(y_max + margin, img.shape[0])
            x_max = min(x_max + margin, img.shape[1])

            # Вырезаем обрезанную область
            cropped = img[y_min:y_max, x_min:x_max]
            
            # Пропускаем изображение, если его размеры меньше 500x500 пикселей
            if cropped.shape[0] < 500 or cropped.shape[1] < 500:
                continue

            # Сохраняем результат
            cv2.imwrite(f'{png_croped_result_path}/{png_list_name}', cropped)
