import cv2
import numpy as np

# Загружаем изображение
img = cv2.imread("media/png_lists/first/page_27.png")  # <-- подставьте свой путь к файлу
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Бинаризация (инвертируем, чтобы чёрные линии стали белыми в маске)
_, bin_img = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)

height, width = bin_img.shape

# ---------- Поиск горизонтальных линий ----------
# Создаём горизонтальное ядро (шириной 50 пикселей)
h_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 1))
# Применяем морфологическую операцию "Открытие" (Open), чтобы выделить длинные горизонтальные линии
h_lines = cv2.morphologyEx(bin_img, cv2.MORPH_OPEN, h_kernel)

# Находим контуры
contours, _ = cv2.findContours(h_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    # Проверяем: ширина контура >= 92% ширины всего изображения, а высота маленькая (линия)
    if w >= 0.92 * width and h < 10:  # подберите порог высоты
        # Обводим зелёным
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

# ---------- Поиск вертикальных линий ----------
# Создаём вертикальное ядро (высотой 50 пикселей)
v_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 50))
# Аналогично, выделяем длинные вертикальные линии
v_lines = cv2.morphologyEx(bin_img, cv2.MORPH_OPEN, v_kernel)

contours, _ = cv2.findContours(v_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    # Проверяем: высота >= 92% высоты всего изображения, а ширина маленькая (линия)
    if h >= 0.92 * height and w < 10:  # подберите порог ширины
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Сохраняем итог
cv2.imwrite("lines_detected.png", img)
