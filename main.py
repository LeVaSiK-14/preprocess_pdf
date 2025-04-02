from app.utils.configs import(
    PNG_LISTS,
    PDF_FILES,
    PNG_LISTS_WITHOUT_LINES,
    PNG_LISTS_WITHOUT_TABLES,
    PNG_LISTS_CROPED,
    PNG_LISTS_CLEAR,
    PNG_LISTS_TILE,
)
from app.utils.utils import(
    clear_media,
)
from app.utils.timer import(
    measure_time,
)
from app.pdf2img import(
    pdf2img,
)
from app.delete_lines import(
    delete_lines,
)
from app.delete_tables import(
    delete_tables,
)
from app.clear_image import(
    remove_gray,
)
from app.utils.process_dirs import(
    delete_dir,
)
from app.crop_images import(
    crop_white_borders,
)


@measure_time
def main():
    clear_media()
    pdf2img(
        pdf_dir_path=PDF_FILES,
        png_dir_path=PNG_LISTS
    )
    delete_lines(
        png_lists_dir_path=PNG_LISTS,
        png_lists_without_lines_path=PNG_LISTS_WITHOUT_LINES
    )
    delete_tables(
        png_lists_witout_lines_dir_path=PNG_LISTS_WITHOUT_LINES,
        png_lists_without_tables_path=PNG_LISTS_WITHOUT_TABLES
    )
    remove_gray(
        PNG_LISTS_WITHOUT_TABLES,
        PNG_LISTS_CLEAR
    )
    crop_white_borders(
        png_lists_clear_dir_path=PNG_LISTS_CLEAR,
        png_lists_croped_path=PNG_LISTS_CROPED,
        threshold=250,
        margin=20
    )
    delete_dir(
        PNG_LISTS,
        PNG_LISTS_WITHOUT_TABLES,
        PNG_LISTS_WITHOUT_LINES,
        PNG_LISTS_CLEAR,
        PNG_LISTS_TILE,
    )


if __name__ == "__main__":
    main()
