import os
import shutil


def combine_files(input_dir: str, output_dir: str) -> None:

    # Создаем выходную директорию, если ее нет
    os.makedirs(output_dir, exist_ok=True)

    # Рекурсивно проходим по input_dir
    for root, dirs, files in os.walk(input_dir):
        # Получаем относительный путь от input_dir до текущей папки
        rel_path = os.path.relpath(root, input_dir)
        # Если мы в корне, rel_path будет '.'
        if rel_path == '.':
            folder_prefix = ''
        else:
            # Если вложенность более одного уровня, заменяем разделители на _
            folder_prefix = rel_path.replace(os.sep, '_') + '_'
        for file in files:
            # Обрабатываем только png-файлы (можно добавить другие расширения, если нужно)
            if file.lower().endswith('.png'):
                source_path = os.path.join(root, file)
                new_file_name = f"{folder_prefix}{file}"
                dest_path = os.path.join(output_dir, new_file_name)
                shutil.copy2(source_path, dest_path)

# Пример использования:
input_dir = "media/png_lists_tile"       # Путь к исходной директории с вложенными папками
output_dir = "media/combined_pngs"         # Путь, куда будут сохранены объединенные файлы
combine_files(input_dir, output_dir)
