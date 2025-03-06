import os
import re
import logging
import pikepdf
from pikepdf import Pdf, Array, Stream

# Настроим логирование для отладки
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

def dump_content_streams(pdf_path, output_dir):
    """
    Сохраняет содержимое контент-стримов каждой страницы в отдельные файлы для анализа.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    with pikepdf.Pdf.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            contents = page.Contents
            all_text = ""
            if contents:
                if isinstance(contents, Array):
                    for idx, item in enumerate(contents):
                        if isinstance(item, Stream):
                            try:
                                # Декодируем содержимое, используя latin-1 для сохранения байтов 1:1
                                stream_text = item.read_bytes().decode('latin-1', errors='replace')
                            except Exception as e:
                                stream_text = f"<<Ошибка декодирования: {e}>>"
                            all_text += f"--- Stream {idx+1} ---\n" + stream_text + "\n\n"
                elif isinstance(contents, Stream):
                    try:
                        all_text = contents.read_bytes().decode('latin-1', errors='replace')
                    except Exception as e:
                        all_text = f"<<Ошибка декодирования: {e}>>"
            
            output_file = os.path.join(output_dir, f"page_{page_num}_content.txt")
            with open(output_file, "w", encoding="latin-1") as f:
                f.write(all_text)
            logging.info(f"Содержимое страницы {page_num} сохранено в {output_file}")

def remove_text_regex(content_bytes: bytes) -> bytes:
    """
    Удаляет все текстовые блоки и операторы из содержимого.
    Здесь добавлены несколько регулярных выражений:
      1. Удаление блоков от BT до ET.
      2. Удаление конструкций (текст) Tj.
      3. Удаление конструкций [ ... ] TJ.
    """
    # Удаляем блоки от BT до ET
    new_bytes = re.sub(br'\s*BT\s+.*?\s+ET\s*', b'', content_bytes,
                       flags=re.DOTALL | re.IGNORECASE)
    # Удаляем конструкции типа (текст) Tj
    new_bytes = re.sub(br'\s*\(.*?\)\s*Tj', b'', new_bytes,
                       flags=re.DOTALL | re.IGNORECASE)
    # Удаляем конструкции типа [ ... ] TJ
    new_bytes = re.sub(br'\s*\[.*?\]\s*TJ', b'', new_bytes,
                       flags=re.DOTALL | re.IGNORECASE)
    return new_bytes

def process_stream(pdf: Pdf, stream_obj: Stream) -> bytes:
    """
    Читает байты из потока и удаляет текстовые блоки.
    """
    content_bytes = stream_obj.read_bytes()
    new_bytes = remove_text_regex(content_bytes)
    return new_bytes

def process_stream_recursive(pdf: Pdf, stream_obj: Stream, visited: set) -> Stream:
    if id(stream_obj) in visited:
        return stream_obj
    visited.add(id(stream_obj))
    
    new_bytes = process_stream(pdf, stream_obj)
    
    if '/Resources' in stream_obj:
        resources = stream_obj['/Resources']
        process_resources(pdf, resources, visited)
    
    new_stream = Stream(pdf, new_bytes)
    for key, value in stream_obj.items():
        if key not in ['/Length', '/Filter', '/DecodeParms', '/Resources']:
            new_stream[key] = value
    if '/Resources' in stream_obj:
        new_stream['/Resources'] = stream_obj['/Resources']
    
    return new_stream

def process_resources(pdf: Pdf, resources, visited: set):
    if not resources:
        return
    xobj_dict = resources.get('/XObject', None)
    if xobj_dict and isinstance(xobj_dict, dict):
        for xobj_name, xobj in list(xobj_dict.items()):
            if isinstance(xobj, Stream):
                if xobj.get('/Subtype', None) == '/Form':
                    new_obj = process_stream_recursive(pdf, xobj, visited)
                    xobj_dict[xobj_name] = new_obj

def process_page(pdf: Pdf, page, visited: set):
    contents = page.Contents
    if contents:
        if isinstance(contents, Array):
            new_array = []
            for item in contents:
                if isinstance(item, Stream):
                    new_array.append(process_stream_recursive(pdf, item, visited))
                else:
                    new_array.append(item)
            page.Contents = Array(new_array)
        elif isinstance(contents, Stream):
            page.Contents = process_stream_recursive(pdf, contents, visited)
    
    if '/Resources' in page:
        process_resources(pdf, page['/Resources'], visited)
    
    if '/Annots' in page:
        page['/Annots'] = Array()

def remove_text_from_pdf(input_pdf_path, output_pdf_path):
    with pikepdf.Pdf.open(input_pdf_path) as pdf:
        visited = set()
        if '/AcroForm' in pdf.Root:
            pdf.Root.AcroForm.clear()
        
        for page in pdf.pages:
            process_page(pdf, page, visited)
        
        pdf.save(output_pdf_path)

# Пример использования:
input_path = "media/pdf_files/first.pdf"
output_path = "output_no_text.pdf"

# Сначала сохраняем оригинальное содержимое потоков для анализа
dump_dir = "dump_streams"
dump_content_streams(input_path, dump_dir)

# Затем пытаемся удалить текст
remove_text_from_pdf(input_path, output_path)
