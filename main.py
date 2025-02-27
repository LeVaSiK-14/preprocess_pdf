from app.utils.configs import(
    PNG_LISTS,
    PNG_CLEAR_LISTS,
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



if __name__ == "__main__":
    main()
