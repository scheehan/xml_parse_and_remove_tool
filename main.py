import xml.etree.ElementTree as ET

tree = ET.parse('sample.xml')
my_root = tree.getroot()

for k in my_root:
    my_list = [] 
    for v in k.attrib.values():
        my_list.insert(-1, v)
    print(my_list[0] + " " + my_list[1])
