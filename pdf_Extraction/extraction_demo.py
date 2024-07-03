import os
from tqdm import tqdm
from extract_image import extract_elements_with_images_from_pdf, save_images_by_elements
from extract_table import extract_tables_from_tei, save_tables_to_xml
import csv

pdf_id = "1"
zoom_level = 4  # Adjust the zoom level to increase resolution

base_directory = "../files"

def process_files_in_directory(tei_directory, pdf_directory, output_directory, zoom=2):
    id_file_dict = {}
    files = os.listdir(tei_directory)

    for i, file in enumerate(tqdm(files, desc="Processing files", unit="file")):
        print(f"Processing file {file}...")
        id_file_dict[i] = file.replace(".tei.xml", "")

        tei_file = os.path.join(tei_directory, file)
        pdf_path = os.path.join(pdf_directory, file.replace(".tei.xml", ""))
        filename = file.replace(".pdf.tei.xml", "")

        elements_with_images = extract_elements_with_images_from_pdf(tei_file, pdf_path)
        save_images_by_elements(elements_with_images, os.path.join(output_directory, filename, 'images'), pdf_id=i)

        tables = extract_tables_from_tei(tei_file)
        save_tables_to_xml(tables, os.path.join(output_directory, filename, 'tables'), pdf_id=i)

        print(f"Processed file {file}.")

    return id_file_dict




def save_dict_to_csv(data_dict, csv_filename):
    """
    将字典保存到CSV文件中，其中键作为一列，值作为另一列。

    参数:
    data_dict (dict): 要保存的字典。
    csv_filename (str): 输出的CSV文件名。
    """
    # 打开文件以写入
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['pdf_id', 'filename'])
        for key, value in data_dict.items():
            csv_writer.writerow([key, value])


if __name__ == "__main__":
    zoom_level = 4
    tei_directory = os.path.join(base_directory, "tei")
    pdf_directory = os.path.join(base_directory, "pdf")
    output_directory = "../files/output"

    id_file_dict = process_files_in_directory(tei_directory, pdf_directory, output_directory, zoom_level)

    # print(id_file_dict)
    # save_dict_to_csv(id_file_dict, 'pdf_id_name.csv')

