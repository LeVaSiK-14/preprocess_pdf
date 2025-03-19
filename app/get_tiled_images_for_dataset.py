import os
import cv2
import numpy as np
from tqdm import tqdm

def split_image_into_tiles(image, tile_size=640):
    """
    Разбивает изображение на плитки размером tile_size x tile_size.
    Если плитка меньше tile_size, дополняет белым фоном.
    Возвращает список плиток.
    """
    h, w = image.shape[:2]
    tiles = []
    for y in range(0, h, tile_size):
        for x in range(0, w, tile_size):
            tile = image[y:y+tile_size, x:x+tile_size]
            tile_h, tile_w = tile.shape[:2]
            if tile_h < tile_size or tile_w < tile_size:
                # Создаем белый фон и вставляем плитку в верхний левый угол
                padded_tile = np.ones((tile_size, tile_size, 3), dtype=image.dtype) * 255
                padded_tile[:tile_h, :tile_w] = tile
                tile = padded_tile
            tiles.append(tile)
    return tiles

def process_directory(input_dir_path: str, output_dir_path: str, tile_size=640) -> None:
    """
    Обходит входную директорию рекурсивно, находит PNG файлы,
    разбивает каждое изображение на плитки и сохраняет их в соответствующую выходную папку.
    Выходная структура папок сохраняется, а файлы именуются так: originalname_1.png, originalname_2.png, ...
    Если плитка полностью белая, она не сохраняется.
    """
    for root, dirs, files in os.walk(input_dir_path):
        rel_path = os.path.relpath(root, input_dir_path)
        out_folder = os.path.join(output_dir_path, rel_path)
        os.makedirs(out_folder, exist_ok=True)
        
        for file in tqdm(files):
            if file.lower().endswith(".png"):
                in_file_path = os.path.join(root, file)
                image = cv2.imread(in_file_path)
                if image is None:
                    print(f"Не удалось загрузить {in_file_path}")
                    continue
                
                tiles = split_image_into_tiles(image, tile_size)
                base_name, _ = os.path.splitext(file)
                for idx, tile in enumerate(tiles, start=1):
                    # Проверяем, является ли плитка полностью белой
                    if np.all(tile == 255):
                        continue
                    out_file_name = f"{base_name}_{idx}.png"
                    out_file_path = os.path.join(out_folder, out_file_name)
                    cv2.imwrite(out_file_path, tile)

# Пример использования:
input_dir = "media/png_lists_croped"   # Путь к входной директории
output_dir = "media/png_lists_tile"      # Путь к выходной директории
process_directory(input_dir, output_dir, tile_size=640)
