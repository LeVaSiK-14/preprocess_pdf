import cv2
import numpy as np
from app.utils.process_dirs import(
    get_full_path,
    get_files_from_dir,
    create_dir,
)
from app.utils.timer import(
    measure_time,
)
from tqdm import tqdm


@measure_time
def crop_white_borders(png_dir_name_path: str, dir_name: str, png_lists_croped_path: str, threshold: int = 250, margin: int = 20) -> tuple:

    png_lists_clear = get_files_from_dir(png_dir_name_path)
    
    png_croped_result_path = get_full_path(png_lists_croped_path, dir_name)
    create_dir(png_croped_result_path)
    
    for png_list_name in tqdm(png_lists_clear):
        
        png_list_name_full_path = get_full_path(png_dir_name_path, png_list_name)


        img = cv2.imread(png_list_name_full_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        mask = gray < threshold
        if not np.any(mask):
            continue

        coords = np.argwhere(mask)

        y_min, x_min = coords.min(axis=0)
        y_max, x_max = coords.max(axis=0) + 1

        y_min = max(y_min - margin, 0)
        x_min = max(x_min - margin, 0)
        y_max = min(y_max + margin, img.shape[0])
        x_max = min(x_max + margin, img.shape[1])
        cropped = img[y_min:y_max, x_min:x_max]
        if cropped.shape[0] < 500 or cropped.shape[1] < 500:
            continue
        cv2.imwrite(f'{png_croped_result_path}/{png_list_name}', cropped)
    
    return png_croped_result_path, dir_name
