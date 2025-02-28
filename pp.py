import cv2
import numpy as np

def remove_tables(image_path, output_path):
    # Загружаем изображение
    img = cv2.imread(image_path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # --- 1. Маска для розового (основной диапазон) ---
    lower_pink = np.array([135, 50, 50])  
    upper_pink = np.array([179, 255, 255])  
    mask_pink = cv2.inRange(hsv, lower_pink, upper_pink)

    # --- 2. Маска для черного ---
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 80])  
    mask_black = cv2.inRange(hsv, lower_black, upper_black)

    # --- 3. Итоговая маска ---
    mask = cv2.bitwise_or(mask_pink, mask_black)

    # --- 4. Морфологическая обработка ---
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # Увеличили ядро
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)  # Объединяем близкие области

    # --- 5. Поиск контуров ---
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # --- 6. Фильтр контуров и закрашивание таблиц белым ---
    min_size = 300  # Минимальная ширина и высота таблицы
    
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        
        if w > min_size and h > min_size:  # Проверяем размер
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), -1)  # Закрашиваем белым

    # --- 7. Сохраняем итоговое изображение ---
    cv2.imwrite(output_path, img)

# Пример использования
remove_tables("media/png_lists_without_lines/first/page_12.png", "i/output_image.png")
