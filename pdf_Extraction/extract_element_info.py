from lxml import etree


def parse_element(element):
    # 提取元素的属性
    element_data = {
        "tag": etree.QName(element.tag).localname,
        "attrib": {etree.QName(k).localname: v for k, v in element.attrib.items()},
        "text": element.text.strip() if element.text else None,
        "children": []
    }

    # 提取直接子元素信息
    for child in element:
        child_data = {
            "tag": etree.QName(child.tag).localname,
            "attrib": {etree.QName(k).localname: v for k, v in child.attrib.items()},
            "text": child.text.strip() if child.text else None,
            "children": []  # 不再递归处理孙子元素
        }
        element_data["children"].append(child_data)

    return element_data


def parse_xml_with_structure(xml_file, structure_tag):
    # 解析XML文件
    tree = etree.parse(xml_file)
    root = tree.getroot()

    # 获取命名空间
    ns = {'tei': root.nsmap[None]}

    # 查找所有指定结构的标签
    elements = root.findall(f".//tei:{structure_tag}", namespaces=ns)

    # 使用解析函数处理所有的指定标签
    return [parse_element(element) for element in elements]

def extract_value(parsed_data, tag, attribute=None):
    for child in parsed_data['children']:
        if child['tag'] == tag:
            if attribute:
                return child['attrib'].get(attribute)
            else:
                return child['text']
    return None


# 示例调用
# xml_file = "../files/tei/2021 Zhang and Pan (AiC) MCDA for TCLP.pdf.tei.xml"
# structure_tag = "figure"  # 可以替换为任何你想处理的标签
# elements_data = parse_xml_with_structure(xml_file, structure_tag)
#
# for element in elements_data:
#     print(element)
    # print("Value of 'coords' tag:", extract_value(element, 'graphic', 'coords'))



