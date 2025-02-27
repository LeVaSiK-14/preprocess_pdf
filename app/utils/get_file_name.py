

def get_file_name(file_path: str) -> str:
    """
        Функция для получения названия файла без расширения из полного пути к файлу 
        Принимает в себя:
        - file_path: str путь к файлу
        Возвращает название файла
    """
    full_name = file_path.split('/')[-1] # Обрезаем весь путь к файлу
    name = full_name.split('.')[0] # Убираем расширение файла
    return name 
