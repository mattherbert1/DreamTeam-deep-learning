import xml.etree.ElementTree as ET
import os


xml_files = [f for f in os.listdir('.') if f.endswith('.xml')]

for x in xml_files:

    tree = ET.parse(x)
    root = tree.getroot()
    
    #removing all the unnecessary outer tags
    rem = []  
    for child in root:
        if(child.tag != 'object' and child.tag != 'size'):
            rem.append(child)
    for r in rem:
        root.remove(r)
        
    #removing all the unnecessary objects
    objects = root.findall('object')
    for o in objects:

        if(o[0].text != 'traffic_light' and o[0].text != 'traffic_sign'):
            root.remove(o)
            
            
    #removing all the unnecessary inter tags in objects
    objects = root.findall('object')
    for o in objects:
        rem =[]
        for a in o:
            if(a.tag != 'name' and a.tag != 'bndbox'):
                rem.append(a)
        for r in rem:
            o.remove(r)
        extra = ET.Element('extra')
        extra.text = 'Unspecified'
        o.append(extra)
                

    

    tree.write(x)