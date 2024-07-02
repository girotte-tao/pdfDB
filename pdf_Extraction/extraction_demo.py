import os
from extract_image import extract_elements_with_images_from_pdf, save_images_by_elements
from extract_table import extract_tables_from_tei, save_tables_to_xml

pdf_id = "1"
zoom_level = 4  # Adjust the zoom level to increase resolution

base_directory = "../files"

def process_files_in_directory(tei_directory, pdf_directory, output_directory, zoom=2):

    for file in os.listdir(tei_directory):
        tei_file = os.path.join(tei_directory, file)
        pdf_path = os.path.join(pdf_directory, file.replace(".tei.xml", ""))
        elements_with_images = extract_elements_with_images_from_pdf(tei_file, pdf_path)
        save_images_by_elements(elements_with_images, os.path.join(output_directory, file.replace(".pdf.tei.xml", "")))

        tables = extract_tables_from_tei(tei_file)
        output_file = os.path.join(output_directory, file.replace(".tei.xml", "_tables.xml"))
        save_tables_to_xml(tables, output_file)


if __name__ == "__main__":
    zoom_level = 4
    tei_directory = os.path.join(base_directory, "tei")
    pdf_directory = os.path.join(base_directory, "pdf")
    output_directory = "../files/output"

    process_files_in_directory(tei_directory, pdf_directory, output_directory, zoom_level)
