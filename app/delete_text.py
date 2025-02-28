import cv2
import numpy as np
import pytesseract

# --- Настройки Tesseract OCR ---
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"  # Укажите путь, если требуется

def remove_large_text(image_path, output_path):
    # Загружаем изображение
    img = cv2.imread(image_path)

    # --- 1. Конвертируем в оттенки серого ---
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # --- 2. Применяем адаптивный порог ---
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY_INV, 25, 15)

    # --- 3. Распознаём текст с позицией ---
    custom_oem_psm_config = r'--oem 3 --psm 6'  # PSM 6: Разрешаем поиск отдельных блоков текста
    data = pytesseract.image_to_data(thresh, config=custom_oem_psm_config, output_type=pytesseract.Output.DICT)

    # --- 4. Фильтруем текст по размеру шрифта ---
    min_text_height = 10  # Минимальный размер шрифта (оставляем подписи)
    max_text_height = 50  # Максимальный размер шрифта (удаляем крупные надписи)

    for i in range(len(data['text'])):
        text = data['text'][i].strip()
        x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]

        if len(text) > 2 and min_text_height < h < max_text_height:  # Фильтр по размеру текста
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), -1)  # Закрашиваем белым

    # --- 5. Сохраняем итоговое изображение ---
    cv2.imwrite(output_path, img)

# Пример использования
remove_large_text("media/png_lists_without_tables/first/page_27.png", "i/text_removed.png")
