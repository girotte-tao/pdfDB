import fitz  # PyMuPDF
from PIL import Image


def extract_image_from_pdf_by_id(pdf_path, coords_str, zoom=2):
    """
    Extracts an image from a PDF file based on given coordinates string and saves it with specified zoom level.

    Parameters:
    - pdf_path: Path to the PDF file
    - coords_str: String containing page number and coordinates (e.g., "4,308.58,208.67,248.12,127.18")
    - zoom: Zoom level for increasing the resolution (default is 2)
    """
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

# # Example usage
# pdf_path = "../files/2021 Zhang and Pan (AiC) MCDA for TCLP.pdf"
# coords_str = "4,308.58,208.67,248.12,127.18"
# output_image_path = "../files/extracted_image.png"
# zoom_level = 4  # Adjust the zoom level to increase resolution
#
# save_image(extract_image_from_pdf_by_id(pdf_path, coords_str, output_image_path, zoom_level), output_image_path)