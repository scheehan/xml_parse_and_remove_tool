import xml.etree.ElementTree as ET

tree = ET.parse('ip_table.xml')
my_root = tree.getroot()

# HTML section

print ('Content-type:text/html\r\n\r\n')
print ('<html>')

print ('<head>')

print ('<style>')
print ('table, th, td { border: 1px solid black; }')
print ('</style>')

print ('</head>')

print ('<body>')

print ('<h2>IP Addresses table list</h2>')

print ('<table style="width:80%">')
print ('<tr>')
print ('<th>No</th>')
print ('<th>IP Address Range</th>')
print ('<th>Owner</th>')
print ('<th>Remarks</th>')
print ('</tr>')

for f in my_root.findall('ip_address'):
    my_no_d = f.find('no').text
    my_ssub = f.find('subnet_range').text
    my_owner = f.find('owner').text
    my_remark = f.find('remark').text

    # print(my_no_d, my_ssub, my_owner, my_remark)
    print ('<tr>')
    print ('<td>' + my_no_d + '</td>')
    print ('<td>' + my_ssub + '</td>')

    if my_owner is None: my_owner = ''

    if my_remark is None: my_remark = ''
    
    print ('<td>' + str(my_owner) + '</td>')
    print ('<td>' + str(my_remark) + '</td>')
    print ('</tr>')

print ('</table>')

print ('<table style="width:50%">')
print ('<tr>'  )  
print ('<td>ns1.time.net.my 203.121.16.85</td>')
print ('<th rowspan="6">Public DNS Server</th>')
print ('</tr>')
print ('<tr>')
print ('<td>ns2.time.net.my 203.121.16.120</td>')
print ('</tr>')
print ('<tr>')
print ('<td>ns3.time.net.my 203.121.65.39</td>')
print ('</tr>')
print ('<tr>')
print ('<td>ns4.time.net.my 203.121.65.30</td>')
print ('</tr>')
print ('<tr>')
print ('<td>TATA DNS: 66.198.145.145</td>')
print ('</tr>')
print ('<tr>')
print ('<td>192.168.242.15</td>')
print ('<th>Internal office Pri DNS Server</th>')
print ('</tr>')
print ('<tr>')
print ('<td>192.168.242.18</td>')
print ('<th>Internal office Sec DNS Server</th>')
print ('</tr>')
print ('</table>')


print ('</body>')
print ('</html>')