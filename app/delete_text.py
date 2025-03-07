import re
import pikepdf
from pikepdf import Pdf, Array, Stream


def remove_text_regex(content_bytes: bytes) -> bytes:
    pattern_bt = re.compile(br'BT[\s\S]*?ET', re.IGNORECASE)
    pattern_text = re.compile(br'(\(.*?\)|\[.*?\])\s*(Tj|TJ)', re.IGNORECASE)
    
    old_bytes = None
    new_bytes = content_bytes
    iteration = 0
    while old_bytes != new_bytes:
        old_bytes = new_bytes
        new_bytes = pattern_bt.sub(b'', old_bytes)
        new_bytes = pattern_text.sub(b'', new_bytes)
        iteration += 1
    return new_bytes


def process_stream(pdf: Pdf, stream_obj: Stream) -> bytes:
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


input_path = "media/pdf_files/first.pdf"
output_path = "output_no_text2.pdf"

remove_text_from_pdf(input_path, output_path)
