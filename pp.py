import cv2
import numpy as np

# Загружаем изображение
img = cv2.imread("media/png_lists/first/page_27.png")
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

# ---------- Поиск и выделение верхней линии ----------
top_line = None
for cnt in h_contours:
    x, y, w, h = cv2.boundingRect(cnt)
    if w >= 0.92 * width and y >= 0.05 * height:  # Линия не ниже 5% высоты
        if top_line is None or w < top_line[2]:  # Берём самую короткую линию
            top_line = (x, y, w, h)

if top_line:
    x, y, w, h = top_line
    cv2.rectangle(result, (x, y), (x + w, y + h), (0, 255, 0), 2)

# ---------- Поиск и выделение нижней линии ----------
bottom_line = None
for cnt in h_contours:
    x, y, w, h = cv2.boundingRect(cnt)
    if w >= 0.92 * width and y <= height - (0.05 * height):  # Линия не выше 5% от низа
        if bottom_line is None or w < bottom_line[2]:  # Берём самую короткую линию
            bottom_line = (x, y, w, h)

if bottom_line:
    x, y, w, h = bottom_line
    cv2.rectangle(result, (x, y), (x + w, y + h), (0, 255, 0), 2)

# ---------- Поиск и выделение левой линии ----------
left_line = None
for cnt in v_contours:
    x, y, w, h = cv2.boundingRect(cnt)
    if h >= 0.92 * height and x <= 0.05 * width:  # Линия не правее 5% от левого края
        if left_line is None or h < left_line[3]:  # Берём самую короткую линию
            left_line = (x, y, w, h)

if left_line:
    x, y, w, h = left_line
    cv2.rectangle(result, (x, y), (x + w, y + h), (0, 255, 0), 2)

# ---------- Поиск и выделение правой линии ----------
right_line = None
for cnt in v_contours:
    x, y, w, h = cv2.boundingRect(cnt)
    if h >= 0.92 * height and x >= width - (0.05 * width):  # Линия не левее 5% от правого края
        if right_line is None or h < right_line[3]:  # Берём самую короткую линию
            right_line = (x, y, w, h)

if right_line:
    x, y, w, h = right_line
    cv2.rectangle(result, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Сохраняем итоговый результат
cv2.imwrite("final_result.png", result)
