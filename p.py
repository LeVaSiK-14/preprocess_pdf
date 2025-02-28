from PIL import Image, ImageDraw
import pdfplumber

def annotate_image_with_coordinates(image_path, pdf_path, output_path):

    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    
    with pdfplumber.open(pdf_path) as pdf:
        page_index = 26
        pdf_page = pdf.pages[page_index]

        pdf_width = pdf_page.width
        pdf_height = pdf_page.height

        img_width, img_height = img.size


        scale_x = img_width / pdf_width
        scale_y = img_height / pdf_height

        offset = 2 

        text_boxes = pdf_page.extract_words()
        for box in text_boxes:
            
            x0, y0, x1, y1 = box['x0'], box['bottom'], box['x1'], box['top']

            x0_img = int(x0 * scale_x)
            x1_img = int(x1 * scale_x)
            
            y0_img = int(y0 * scale_y)
            y1_img = int(y1 * scale_y)

            underline_y = y0_img + offset

            draw.line([(x0_img, underline_y), (x1_img, underline_y)], fill="green", width=2)

    img.save(output_path, format="PNG")

annotate_image_with_coordinates(
    'media/png_lists/first/page_27.png',
    'media/pdf_files/first.pdf',
    'page_with_green_text.png'
)
