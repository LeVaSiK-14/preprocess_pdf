import cv2
from app.utils.process_dirs import(
    get_dirs_from_dir,
    get_files_from_dir,
    create_dir,
    get_full_path,
)
from app.utils.get_file_name import(
    get_file_name,
)
from app.utils.timer import(
    measure_time,
)

@measure_time
def delete_lines(png_lists_dir_path: str, png_lists_without_lines_path: str):
    png_dirs = get_dirs_from_dir(png_lists_dir_path)
    for png_dir in png_dirs:
        png_dir_path = get_full_path(png_lists_dir_path, png_dir)
        png_lists = get_files_from_dir(png_dir_path)
        
        png_lists_without_lines_dir_path = get_full_path(png_lists_without_lines_path, png_dir)
        create_dir(png_lists_without_lines_dir_path)
        
        for png_list in png_lists:
            png_list_path = get_full_path(png_dir_path, png_list)
            
            
            # Загружаем изображение
            img = cv2.imread(png_list_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Бинаризация (инвертируем, чтобы чёрные линии стали белыми в маске)
            _, bin_img = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)

            height, width = bin_img.shape

            # ---------- Поиск горизонтальных линий ----------
            h_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 1))
            h_lines = cv2.morphologyEx(bin_img, cv2.MORPH_OPEN, h_kernel)
            h_contours, _ = cv2.findContours(h_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # ---------- Поиск вертикальных линий ----------
            v_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 50))
            v_lines = cv2.morphologyEx(bin_img, cv2.MORPH_OPEN, v_kernel)
            v_contours, _ = cv2.findContours(v_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Копируем оригинальное изображение для результата
            result = img.copy()

            # ---------- Поиск ВЕРХНЕЙ линии ----------
            top_line = None
            for cnt in h_contours:
                x, y, w, h = cv2.boundingRect(cnt)
                if w >= 0.92 * width and y <= 0.05 * height:  # Линия не ниже 5% высоты (должна быть сверху)
                    if top_line is None or w < top_line[2]:  # Берём самую короткую линию
                        top_line = (x, y, w, h)

            # ---------- Поиск НИЖНЕЙ линии ----------
            bottom_line = None
            for cnt in h_contours:
                x, y, w, h = cv2.boundingRect(cnt)
                if w >= 0.92 * width and y >= height - (0.05 * height):  # Линия не выше 5% от нижнего края (должна быть снизу)
                    if bottom_line is None or w < bottom_line[2]:  # Берём самую короткую линию
                        bottom_line = (x, y, w, h)

            # ---------- Поиск ЛЕВОЙ линии ----------
            left_line = None
            for cnt in v_contours:
                x, y, w, h = cv2.boundingRect(cnt)
                if h >= 0.92 * height and x <= 0.05 * width:  # Линия не правее 5% от левого края
                    if left_line is None or h < left_line[3]:  # Берём самую короткую линию
                        left_line = (x, y, w, h)

            # ---------- Поиск ПРАВОЙ линии ----------
            right_line = None
            for cnt in v_contours:
                x, y, w, h = cv2.boundingRect(cnt)
                if h >= 0.92 * height and x >= width - (0.05 * width):  # Линия не левее 5% от правого края
                    if right_line is None or h < right_line[3]:  # Берём самую короткую линию
                        right_line = (x, y, w, h)

            # Если какие-то линии не найдены, используем крайние значения
            top_y = top_line[1] if top_line else 0
            bottom_y = bottom_line[1] if bottom_line else height
            left_x = left_line[0] if left_line else 0
            right_x = right_line[0] if right_line else width

            # ---------- Закрашиваем ВСЁ за пределами рамки в белый цвет ----------
            if top_y > 0:
                result[0:top_y, :] = (255, 255, 255)  # Всё выше верхней линии
            if bottom_y < height:
                result[bottom_y:, :] = (255, 255, 255)  # Всё ниже нижней линии
            if left_x > 0:
                result[:, 0:left_x] = (255, 255, 255)  # Всё левее левой линии
            if right_x < width:
                result[:, right_x:] = (255, 255, 255)  # Всё правее правой линии

            # ---------- Закрашиваем сами линии в белый ----------
            if top_line:
                x, y, w, h = top_line
                result[y:y+h, :] = (255, 255, 255)
            if bottom_line:
                x, y, w, h = bottom_line
                result[y:y+h, :] = (255, 255, 255)
            if left_line:
                x, y, w, h = left_line
                result[:, x:x+w] = (255, 255, 255)
            if right_line:
                x, y, w, h = right_line
                result[:, x:x+w] = (255, 255, 255)

            png_list_without_lines_path = get_full_path(png_lists_without_lines_dir_path, png_list)
            cv2.imwrite(png_list_without_lines_path, result)
