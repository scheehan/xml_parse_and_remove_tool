import xml.etree.ElementTree as ET

tree = ET.parse('sample.xml')
my_root = tree.getroot()

a = my_root.find('a')
b = ET.SubElement(a, 'b')
c = ET.SubElement(b, 'c')
c.text = 'text3'

a.tail = '\n'
b.tail = '\n'
c.tail = '\n'

print (ET.tostring(my_root))

tree.write('sample.xml', encoding="utf-8", xml_declaration=True)