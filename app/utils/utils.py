from app.utils.process_dirs import(
    delete_dir,
    create_dir,
)
from app.utils.configs import(
    PNG_LISTS,
    PNG_CLEAR_LISTS,
    PNG_LISTS_WITHOUT_LINES,
)


def clear_media():
    delete_dir(
        PNG_LISTS,
        PNG_CLEAR_LISTS,
        PNG_LISTS_WITHOUT_LINES,
    )
    create_dir(PNG_LISTS)
    create_dir(PNG_CLEAR_LISTS)
    create_dir(PNG_LISTS_WITHOUT_LINES)
