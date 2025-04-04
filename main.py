from app.utils.configs import(
    PNG_LISTS,
    PNG_LISTS_WITHOUT_LINES,
    PNG_LISTS_WITHOUT_TABLES,
    PNG_LISTS_CROPED,
    PNG_LISTS_WITHOUT_GRAY,
    PNG_LISTS_TILE,
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
    create_dir,
)
from app.crop_images import(
    crop_white_borders,
)
from app.tiled_images import(
    tiled_images,
)


@measure_time
def main(pdf_file_path: str) -> tuple:
    create_dir(PNG_LISTS)
    create_dir(PNG_LISTS_WITHOUT_LINES)
    create_dir(PNG_LISTS_WITHOUT_TABLES)
    create_dir(PNG_LISTS_WITHOUT_GRAY)
    create_dir(PNG_LISTS_CROPED)
    create_dir(PNG_LISTS_TILE)
    
    png_lists_dir_path, dir_name = pdf2img(
        pdf_file_path=pdf_file_path,
        png_dir_path=PNG_LISTS
    )
    png_lists_without_lines, dir_name = delete_lines(
        png_dir_path=png_lists_dir_path,
        dir_name=dir_name,
        png_lists_without_lines_path=PNG_LISTS_WITHOUT_LINES
    )
    png_lists_without_tables, dir_name = delete_tables(
        png_lists_witout_lines_dir_path=png_lists_without_lines,
        dir_name=dir_name,
        png_lists_without_tables_path=PNG_LISTS_WITHOUT_TABLES
    )
    png_lists_without_gray, dir_name = remove_gray(
        png_dir_path=png_lists_without_tables,
        dir_name=dir_name,
        output_image_path=PNG_LISTS_WITHOUT_GRAY
    )
    png_lists_without_borders, dir_name = crop_white_borders(
        png_dir_name_path=png_lists_without_gray,
        dir_name=dir_name,
        png_lists_croped_path=PNG_LISTS_CROPED
    )
    png_lists_by_tiled, dir_name, info_path = tiled_images(
        png_dir_name_path=png_lists_without_borders,
        dir_name=dir_name,
        output_dir_path=PNG_LISTS_TILE
    )
    delete_dir(
        png_lists_dir_path,
        png_lists_without_lines,
        png_lists_without_tables,
        png_lists_without_gray,
        png_lists_without_borders,
    )
    
    return png_lists_by_tiled, dir_name, info_path


if __name__ == "__main__":
    images, dir_name, info_path = main(
        pdf_file_path='media/pdf_files/second.pdf'
    )
    print(images, dir_name, info_path)
