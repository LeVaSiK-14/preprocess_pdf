import cv2
import math
import numpy as np
import os

def get_tile_starts(dim_size, tile_size, overlap):
    starts = []
    step = tile_size - overlap
    pos = 0
    while True:
        if pos > dim_size - tile_size:
            break
        starts.append(pos)
        pos += step
    last_pos = dim_size - tile_size
    if last_pos not in starts:
        if starts and starts[-1] < last_pos:
            starts.append(last_pos)
        elif not starts:
            starts.append(0)
    return starts


def split_image_into_tiles(
    image_path: str,
    tile_size: int = 3000,
    overlap: int = 1500,
    info_txt_name: str = "tiles_info.txt"
):
    output_dir = os.path.join('media', image_path.split('/')[-1].replace('.png', ''))
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Не удалось открыть изображение: {image_path}")

    orig_height, orig_width = img.shape[:2]

    new_width = math.ceil(orig_width / tile_size) * tile_size
    new_height = math.ceil(orig_height / tile_size) * tile_size

    canvas = np.full((new_height, new_width, 3), 255, dtype=np.uint8)
    canvas[:orig_height, :orig_width] = img

    x_starts = get_tile_starts(new_width, tile_size, overlap)
    y_starts = get_tile_starts(new_height, tile_size, overlap)

    os.makedirs(output_dir, exist_ok=True)

    info_path = os.path.join(output_dir, info_txt_name)
    with open(info_path, "w", encoding="utf-8") as f:
        tile_index = 0
        for y0 in y_starts:
            for x0 in x_starts:
                x1 = x0 + tile_size
                y1 = y0 + tile_size

                tile = canvas[y0:y1, x0:x1]

                tile_filename = f"tile_{tile_index}_{x0}_{y0}.png"
                tile_path = os.path.join(output_dir, tile_filename)
                cv2.imwrite(tile_path, tile)

                f.write(f"{tile_path}: {x0},{y0},{x1},{y1}\n")

                tile_index += 1

if __name__ == "__main__":
    input_image = "images/2600_2700.png"
    
    split_image_into_tiles(
        image_path=input_image
    )
