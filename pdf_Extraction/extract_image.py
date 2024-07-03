import os
import re
import fitz  # PyMuPDF
from PIL import Image
from extract_element_info import parse_xml_with_structure, extract_value


def extract_image_from_pdf_by_coord(pdf_path, coords_str, zoom=2):
    """
    Extracts an image from a PDF file based on given coordinates string and saves it with specified zoom level.

    Parameters:
    - pdf_path: Path to the PDF file
    - coords_str: String containing page number and coordinates (e.g., "4,308.58,208.67,248.12,127.18")
    - zoom: Zoom level for increasing the resolution (default is 2)
    """
    if not coords_str:
        return None
    # Parse the coordinates string
    coords_list = coords_str.split(',')
    page_number = int(coords_list[0]) - 1  # Convert to 0-based index
    coords = tuple(map(float, coords_list[1:]))

    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    # Select the page
    page = pdf_document.load_page(page_number)

    # Define the bounding box
    rect = fitz.Rect(coords[0], coords[1], coords[0] + coords[2], coords[1] + coords[3])

    # Set zoom matrix
    mat = fitz.Matrix(zoom, zoom)

    # Extract the image with zoom
    pix = page.get_pixmap(matrix=mat, clip=rect)

    # Convert to PIL image
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    return img


def save_image(image, output_image_path):
    """
    Saves the extracted image to the specified output path.

    Parameters:
    - image: PIL image object
    - output_image_path: Path to save the extracted image
    """
    image.save(output_image_path)


def save_images(images, output_dir):
    """
    Saves the extracted images to the specified output directory.

    Parameters:
    - images: List of PIL image objects
    - output_dir: Directory path to save the extracted images
    """
    os.makedirs(output_dir, exist_ok=True)

    for i, image in enumerate(images):
        image.save(os.path.join(output_dir, f"image_{i}.png"))


def save_images_by_elements(elements, output_dir, pdf_id=0):
    """
    Saves the extracted images to the specified output directory.

    Parameters:
    - images: List of PIL image objects
    - output_dir: Directory path to save the extracted images
    """
    os.makedirs(output_dir, exist_ok=True)

    for i, element in enumerate(elements):
        first_figure_identifier = extract_first_figure_identifier(element['head'])
        if first_figure_identifier:
            element['image'].save(os.path.join(output_dir, f"{pdf_id}_{first_figure_identifier}.jpg"))


def clean_text(text):
    # 去除空格、点等特殊符号，但保留字母和数字
    return re.sub(r'[\s\.\-]+', '', text)


def extract_first_figure_identifier(text):
    if not text:
        return None

    # 清理文本
    cleaned_text = clean_text(text)

    # 提取以 fig 或 figure 开头的第一个匹配项，忽略大小写
    match = re.search(r'(fig|figure)(\d+)', cleaned_text, re.IGNORECASE)

    if match:
        return match.group(0).lower()
    else:
        return None


def extract_images_from_pdf_by_coords(pdf_path, coords_list, zoom=2):
    """
    Extracts images from a PDF file based on given coordinates list and saves them with specified zoom level.

    Parameters:
    - pdf_path: Path to the PDF file
    - coords_list: List of coordinates strings (e.g., ["4,308.58,208.67,248.12,127.18", "6,126.65,390.28,341.21,97.90"])
    - zoom: Zoom level for increasing the resolution (default is 2)
    """
    extracted_images = [extract_image_from_pdf_by_coord(pdf_path, coords_str, zoom) for coords_str in coords_list]

    return [i for i in extracted_images if i]


def extract_images_from_pdf_by_elements(pdf_path, elements_data, zoom=2):
    """
    Extracts images from a PDF file based on elements data extracted from the TEI XML file.

    Parameters:
    - pdf_path: Path to the PDF file
    - elements_data: List of elements data containing image coordinates
    - zoom: Zoom level for increasing the resolution (default is 2)
    """

    for e in elements_data:
        e['image'] = extract_image_from_pdf_by_coord(pdf_path, e['coords'], zoom)

    return elements_data

def extract_elements_with_images_from_pdf(xml_file, pdf_path, structure_tag='figure', zoom=2):
    """
    Extracts images from a PDF file based on coordinates extracted from the TEI XML file.

    Parameters:
    - xml_file: Path to the TEI XML file
    - pdf_path: Path to the PDF file
    - structure_tag: Tag name for the structure containing image coordinates
    - zoom: Zoom level for increasing the resolution (default is 2)
    """
    # Parse the XML file to extract image coordinates
    raw_elements_data = parse_xml_with_structure(xml_file, structure_tag)

    elements_data = [
        {
            "figDesc": extract_value(element, 'figDesc'),
            "head": extract_value(element, 'figDesc'),
            "coords": extract_value(element, 'graphic', 'coords'),
            "label": extract_value(element, 'label'),
        } for element in raw_elements_data if extract_value(element, 'graphic', 'coords')]

    extracted_images = extract_images_from_pdf_by_elements(pdf_path, elements_data, zoom)

    return extracted_images





# Example usage
# tei_file = "../files/tei/2021 Zhang and Pan (AiC) MCDA for TCLP.pdf.tei.xml"
# pdf_path = "../files/pdf/2021 Zhang and Pan (AiC) MCDA for TCLP.pdf"
# coords_str = "10,37.59,526.80,514.12,43.44"
# output_image_path = "../files/extracted_image.png"
# zoom_level = 4  # Adjust the zoom level to increase resolution
#
# save_image(extract_image_from_pdf_by_coord(pdf_path, coords_str, zoom_level), output_image_path)
# elements_with_images = extract_elements_with_images_from_pdf(tei_file, pdf_path)
# save_images(images, "../files/extracted_images")

# save_images_by_elements(elements_with_images, "../files/extracted_images")