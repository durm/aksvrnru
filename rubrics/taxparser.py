#-*- coding: utf-8 -*-

from lxml import etree

def gen_indentation_level(row):
    row = row.replace("\t", "    ")
    i = 0
    while row[i] == " " :
        i += 1
    return int(i / 4)
    
def validate(rows):
    current_level = 0
    for row in rows :
        level = gen_indentation_level(row)
        if level - current_level > 1 : return False
        current_level = level
    return True
    
def get_path(elem):
    return "/".join([e.get("name", "") for e in elem.xpath("./ancestor::*")])
    
def parse_txt_tax(rows):
    assert validate(rows), "Wrong structure"
    tax = etree.Element("tax")
    current_root = None
    current_level = 0
    for k, row in enumerate(rows) :
        level = gen_indentation_level(row)
        elem = etree.Element("node")
        elem.set("name", row.strip())
        elem.set("num", str(k))
        if level == 0 :
            current_level = level
            tax.append(elem)
        elif level == current_level + 1 :
            current_root.append(elem)
            current_level = level
        else:
            step = current_level - level + 1
            while step > 0 :
                step -= 1
                current_root = current_root.getparent()
            current_root.append(elem)    
            current_level = level
        current_root = tax.xpath("//*[@num = '"+str(k)+"']")[0]
        current_root.set("path", get_path(current_root))
    return tax
    

