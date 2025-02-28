from app.utils.configs import(
    PNG_LISTS,
    PNG_LISTS_WITHOUT_TABLES,
    PDF_FILES,
    PNG_LISTS_WITHOUT_LINES,
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
from app.utils.process_dirs import(
    delete_dir,
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
    delete_dir(PNG_LISTS, PNG_LISTS_WITHOUT_LINES)


if __name__ == "__main__":
    main()
