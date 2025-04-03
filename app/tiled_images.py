import cv2
import math
import numpy as np
from app.utils.get_tile_starts import(
    get_tile_starts,
)
from app.utils.process_dirs import(
    get_full_path,
    get_dirs_from_dir,
    get_files_from_dir,
)
from app.utils.timer import(
    measure_time,
)
from app.utils.get_file_name import get_file_name
from tqdm import tqdm


@measure_time
def tiled_images(
    image_path_dir: str,
    output_dir_path: str,
    tile_size: int = 3000,
    overlap: int = 1500,
    info_txt_name: str = "tiles_info.txt"
):
    png_dirs_names = get_dirs_from_dir(image_path_dir)
    for pnd_dir_name in png_dirs_names:
        png_dir_name_path = get_full_path(image_path_dir, pnd_dir_name)
        png_lists_clear = get_files_from_dir(png_dir_name_path)
        
        for png_list_name in tqdm(png_lists_clear):
            
            png_list_name_full_path = get_full_path(png_dir_name_path, png_list_name)
            
            img = cv2.imread(png_list_name_full_path)
            if img is None:
                raise FileNotFoundError(f"Не удалось открыть изображение: {png_list_name_full_path}")

            orig_height, orig_width = img.shape[:2]

            new_width = math.ceil(orig_width / tile_size) * tile_size
            new_height = math.ceil(orig_height / tile_size) * tile_size

            canvas = np.full((new_height, new_width, 3), 255, dtype=np.uint8)
            canvas[:orig_height, :orig_width] = img

            x_starts = get_tile_starts(new_width, tile_size, overlap)
            y_starts = get_tile_starts(new_height, tile_size, overlap)

            info_path = get_full_path(output_dir_path, info_txt_name)
            with open(info_path, "a", encoding="utf-8") as f:
                tile_index = 0
                for y0 in y_starts:
                    for x0 in x_starts:
                        x1 = x0 + tile_size
                        y1 = y0 + tile_size

                        tile = canvas[y0:y1, x0:x1]
                        list_num = get_file_name(png_list_name)
                        tile_filename = f"{pnd_dir_name}_{list_num}__{tile_index}___{x0}____{y0}_____{x1}______{y1}.png"
                        tile_path = get_full_path(output_dir_path, tile_filename)
                        cv2.imwrite(tile_path, tile)

                        f.write(f"{tile_path}: {x0},{y0},{x1},{y1}\n")

                        tile_index += 1
