import cv2
import numpy as np

def filter_colors(input_image_path, output_image_path):
    """
    Фильтрует изображение, оставляя только пиксели, принадлежащие к четырём цветовым диапазонам:
    синий, красный, розовый и чёрный. Все остальные пиксели заменяются на белый.
    
    :param input_image_path: путь к исходному изображению.
    :param output_image_path: путь для сохранения обработанного изображения.
    """
    # Загружаем изображение
    image = cv2.imread(input_image_path)
    if image is None:
        print(f"Не удалось открыть изображение: {input_image_path}")
        return
    
    # Переводим изображение в HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Определяем диапазоны для нужных цветов.
    # Синий
    lower_blue = np.array([100, 150, 150])
    upper_blue = np.array([140, 255, 255])
    
    # Красный (учитываем два диапазона)
    lower_red1 = np.array([0, 150, 150])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 150, 150])
    upper_red2 = np.array([180, 255, 255])
    
    # Розовый
    lower_pink = np.array([135, 50, 50])
    upper_pink = np.array([179, 255, 255])
    
    # Чёрный (настраиваем так, чтобы исключить серый)
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 50])  # яркость до 50
    
    # Создаём маски для каждого цвета
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    
    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)
    
    mask_pink = cv2.inRange(hsv, lower_pink, upper_pink)
    
    mask_black = cv2.inRange(hsv, lower_black, upper_black)
    
    # Объединяем маски в одну
    mask_combined = cv2.bitwise_or(mask_blue, mask_red)
    # mask_combined = cv2.bitwise_or(mask_combined, mask_pink)
    # mask_combined = cv2.bitwise_or(mask_combined, mask_black)
    
    # Применяем маску: оставляем только нужные пиксели
    result = cv2.bitwise_and(image, image, mask=mask_combined)
    # Остальные области делаем белыми
    result[mask_combined == 0] = [255, 255, 255]
    
    # Сохраняем результат
    cv2.imwrite(output_image_path, result)
    print(f"Сохранено отфильтрованное изображение в: {output_image_path}")


list_images = [
    "media/png_lists_without_tables/first/page_26.png",
    "media/png_lists_without_tables/first/page_27.png",
    "media/png_lists_without_tables/first/page_28.png",
    "media/png_lists_without_tables/first/page_29.png",
    "media/png_lists_without_tables/first/page_30.png",
    "media/png_lists_without_tables/first/page_31.png",
]
# Пример вызова:
for inx, el in enumerate(list_images):
    filter_colors(el, f"filtered_images/output_filtered_{inx}.png")
