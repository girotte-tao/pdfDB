import os
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


def save_tables_to_xml(tables, output_file):
    root = etree.Element("tables")
    for table in tables:
        root.append(table)

    tree = etree.ElementTree(root)
    tree.write(output_file, pretty_print=True, xml_declaration=True, encoding="UTF-8")


def process_files_in_directory(base_directory):
    tei_directory = os.path.join(base_directory, "tei")
    output_directory = os.path.join(base_directory, "extracted_tables_xml")

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for tei_filename in os.listdir(tei_directory):
        if tei_filename.endswith(".tei.xml"):
            tei_file = os.path.join(tei_directory, tei_filename)
            tables = extract_tables_from_tei(tei_file)
            output_file = os.path.join(output_directory, tei_filename.replace(".tei.xml", "_tables.xml"))
            save_tables_to_xml(tables, output_file)


# 示例调用
base_directory = "../files"
process_files_in_directory(base_directory)
