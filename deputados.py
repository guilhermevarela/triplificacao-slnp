# -*- coding:utf-8 -*-
import xml.etree.ElementTree as ET
import glob
import uuid

if __name__ == '__main__':
    xml_files = glob.glob('./dados_deputados' + '/*.xml')
    xml_element_tree = None

    for xml_file in xml_files:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        data = root.find('dados')
        guid = str(uuid.uuid4())

        for child in data:
            child.set('guid', guid)
        tree.write(xml_file)
