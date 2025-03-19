from app.utils.process_dirs import(
    delete_dir,
    create_dir,
)
from app.utils.configs import(
    PNG_LISTS,
    PNG_LISTS_WITHOUT_LINES,
    PNG_LISTS_WITHOUT_TABLES,
    PNG_LISTS_CROPED,
    PNG_LISTS_CLEAR,
    PNG_LISTS_TILE,
)


def clear_media():
    delete_dir(
        PNG_LISTS,
        PNG_LISTS_WITHOUT_LINES,
        PNG_LISTS_WITHOUT_TABLES,
        PNG_LISTS_CROPED,
        PNG_LISTS_CLEAR,
        PNG_LISTS_TILE,
    )
    create_dir(PNG_LISTS)
    create_dir(PNG_LISTS_WITHOUT_LINES)
    create_dir(PNG_LISTS_WITHOUT_TABLES)
    create_dir(PNG_LISTS_CROPED)
    create_dir(PNG_LISTS_CLEAR)
    create_dir(PNG_LISTS_TILE)


def create_dirs_by_color(png_lists_by_color_dir_path: str, folder_name: str, colors: list) -> dict:
    folders: dict = dict()
    
    for color in colors:
        full_path = f'{png_lists_by_color_dir_path}/{folder_name}/{color}'
        create_dir(full_path)
        folders[color] = full_path
    
    return folders
