import os
import re
from lxml import etree


def extract_tables_from_tei(tei_file):
    tree = etree.parse(tei_file)
    root = tree.getroot()

    # 获取命名空间
    ns = {'tei': root.nsmap[None]}

    # 查找所有表格
    tables = []
    for figure in root.findall(f".//tei:figure[@type='table']", namespaces=ns):
        tables.append(figure)
    return tables


def save_tables_to_xml(tables, output_dir, pdf_id=0):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for table in tables:
        root = etree.Element("table")
        root.append(table)
        tree = etree.ElementTree(root)

        table_identifier = extract_table_identifier(table)
        output_file = os.path.join(output_dir, f"{pdf_id}_{table_identifier}.xml")
        tree.write(output_file, pretty_print=True, xml_declaration=True, encoding="UTF-8")


def clean_text(text):
    # 去除空格、点等特殊符号
    return re.sub(r'[\s\.\-]+', '', text)


def extract_table_identifier(element):
    # 查找<head>标签
    head_element = element.find(".//{http://www.tei-c.org/ns/1.0}head")
    if head_element is not None:
        head_text = head_element.text

        # 清理文本并提取Table标识符
        cleaned_text = clean_text(head_text)

        # 提取Table标识符
        match = re.search(r'(table)(\d+)', cleaned_text, re.IGNORECASE)

        if match:
            return match.group(0).lower()
    return None


# def process_files_in_directory(base_directory):
#     tei_directory = os.path.join(base_directory, "tei")
#     output_directory = os.path.join(base_directory, "extracted_tables_xml")
#
#     if not os.path.exists(output_directory):
#         os.makedirs(output_directory)
#
#     for tei_filename in os.listdir(tei_directory):
#         if tei_filename.endswith(".tei.xml"):
#             tei_file = os.path.join(tei_directory, tei_filename)
#             tables = extract_tables_from_tei(tei_file)
#             output_dir = os.path.join(output_directory, tei_filename.replace(".pdf.tei.xml", ""))
#             save_tables_to_xml(tables, output_dir)



# pdf_id = 0
# # 示例调用
# base_directory = "../files"
# tei_filename = "2021 Zhang and Pan (AiC) MCDA for TCLP.pdf.tei.xml"
#
# # process_files_in_directory(base_directory)
#
# output_directory = "../files/output/extracted_tables_xml"
#
# output_dir = os.path.join(output_directory, tei_filename.replace("pdf.tei.xml", ""))
# tei_filepath = os.path.join(base_directory, "tei", tei_filename)
#
# tables = extract_tables_from_tei(tei_filepath)
#
# save_tables_to_xml(tables, output_dir)


