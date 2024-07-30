from lxml import etree

import re, sys

def main():
    
    # get user input argument and parameter  
    args = sys.argv[1:]
    
    # return friendly usage explaination about how to search keyword and delete XML element record
    if not args:
        print('''
              2 features provides by this tool; search for existing element text and remove element.
              'usage: [--filename "xml filename"][--check keyword]'
              'usage: [--filename "xml filename"][--remove <idx no>]'
              ''')
        sys.exit(1)
        
    # check if filename and check option provided
    if args[0] == '--filename' and args[2] == '--check':
        
        if len(sys.argv) > 2:
            
            # simple check for file extension
            if args[1].endswith('.xml'):
                
                filename = args[1]
                
                mytree = etree.parse(filename, parser=etree.XMLParser())
                myroot = mytree.getroot()
        
        # get root level element string
        subelementtag = myroot[0].tag
            
        
        if len(sys.argv) > 4:

            keyword = args[3]
            
            # check if XML or RSS schema
            if myroot == 'rss':
                elementlist = mytree.xpath(".//item")
            else:
                elementlist = mytree.findall(subelementtag)
            
            # setup list for matched element item
            myitems = []
            
            # setup list record and enumeration idx number
            for h, i in enumerate(elementlist):

                if keyword in etree.tostring(i).decode("utf-8"):
                    
                    myitems.append(h)
                    myitems.append(etree.tostring(i))
            
            # if list record not empty, return matching message
            if len(myitems) >= 1:
                for e, f in zip(myitems[::2], myitems[1::2]):
                    print(f'Idx: {e} \nChildElement: \n    {f.decode("utf-8")}')
            
            # if list record empty, return no matching message
            elif len(myitems) == 0:
                print('no matching keyword')

                    
        else:
            # return message if no argument parameter provided        
            print('support XML file format and a search keyword')

            sys.exit(1)
    
    # check if filename and remove option provided            
    if args[0] == '--filename' and args[2] == '--remove':
        
        if len(sys.argv) > 2:
            if args[1].endswith('.xml'):
                filename = args[1]
                
                mytree = etree.parse(filename, etree.XMLParser())
                myroot = mytree.getroot()
        
        match myroot.tag:
            case 'rss':
                subelementtag = 'item'
            case _:
                subelementtag = myroot[0].tag
        
        if len(sys.argv) > 4:
            
            myidx = int(args[3])
            
            
            if subelementtag == 'item':
                elementlist = mytree.xpath(".//item")
                
            else:
                elementlist = mytree.findall(subelementtag)
        
        while True:
            try:
                myroot.remove(elementlist[myidx])
                
                # open file ready to be write as byte. close when its finished
                with open(f'removal_{filename}', 'wb') as f:
                    mytree.write(f, pretty_print=False, encoding="utf-8", xml_declaration=True)
                
                break
            except IndexError:
                print("Oops! No such index. Try again ...")
                break


if __name__ == "__main__":
  main()