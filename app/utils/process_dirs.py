import os
import shutil


def create_dir(dir_path: str) -> None:
    """
        Функция для создания новой директории
        Принимает в себя:
        - dir_path: str путь к директории которую нужно создать
    """
    os.makedirs(dir_path, exist_ok=True) # Создаем директорию если ее не существует


def delete_dir(*dir_paths: tuple) -> None:
    """
        Функция для удаления директории и всех ее вложеностей если такая директория существует
        Принимает в себя:
        - *dir_paths: tuple путь к директории которую нужно удалить
    """
    for dir_path in dir_paths:
        if os.path.exists(dir_path): # Проверяем если директория существует
            shutil.rmtree(dir_path) # Удаляем эту директорию


def get_full_path(dir_to: str, dir_path: str) -> str:
    """
        Функция для получения полного пути
        Принимает в себя 
        - dir_to: str в какую папку добавить
        - dir_path: str какую картинку или папку добавить
    """
    full_path = os.path.join(dir_to, dir_path) # Создаем путь
    return full_path


def get_files_from_dir(dir_path: str) -> list:
    """
        Функция для получения списка файлов из директории
        Принимает в себя:
        - dir_path: str путь к директории с файлами
        Возвращает список с названиями файлов
    """
    items: list = list() # Создаем массив для хранения названий
    for item in os.listdir(dir_path): # Получаем каждый элемент из директории
        if os.path.isfile(get_full_path(dir_path, item)): # Если элемент файл то добавляем его в массив файлов
            items.append(item) # Добавляем в массив файлов
    
    return items


def get_dirs_from_dir(dir_path: str) -> list:
    """
        Функция для получения списка директорий внутри другой директории
        Принимает в себя:
        - dir_path: str путь к директории
        Возвращает список директорий из первичной
    """
    folders = [item for item in os.listdir(dir_path) if os.path.isdir(get_full_path(dir_path, item))] 
    return folders
