from pdf2image import convert_from_path

from app.utils.get_file_name import(
    get_file_name,
)
from app.utils.process_dirs import(
    create_dir,
    get_full_path,
)
from app.utils.timer import(
    measure_time,
)
from tqdm import tqdm
import uuid


@measure_time
def pdf2img(pdf_file_path: str, png_dir_path: str) -> tuple:
    """
        Функция для преобразования файлов PDF в отдельные страницы в формате PNG
        Принимает в себя:
        - pdf_dir_path: str путь к директории с файлами pdf
        - png_dir_path: str путь к директории куда сохранятся изображения страниц
        
        Передаем в функцию путь к директории с файлами и путь к директории куда сохранять изображения
        Для каждого файла внутри директории с изображениями создастся директория с названием PDF файла
        В эту директорию сохранятся все страницы PDF в формате PNG с нумерацией
    """
    token = "".join(str(uuid.uuid4()).split('-'))
    pdf_file_name = get_file_name(pdf_file_path) # Получаем название файла без расширения(для создания директории под каждый файл)
    pdf_file_name = f'{pdf_file_name}__{token}'
    full_dir_img_path = get_full_path(png_dir_path, pdf_file_name) # Получаем путь к директории куда сохраним изображения для PDF файла
    create_dir(full_dir_img_path) # Создаем эту директорию
    
    pages = convert_from_path(pdf_file_path) # Получаем все страницы из PDF файла
    i = 1
    for page in tqdm(pages): # Получаем каждую страницу отдельно вместе с нумерацией
        page.save(f'{full_dir_img_path}/page{i}.png', 'PNG') # Сохраняем картинку в формате PNG с нумерацией по порядку
        i += 1
    i = 0
    
    return full_dir_img_path, pdf_file_name
