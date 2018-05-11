#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 00:27:02 2018

@author: aidin
"""


import os
from xml.dom.minidom import parse



def create_backup(new_file_name):
    """ create a backup of original file """
    old_file_name = new_file_name + "~"
    os.rename(new_file_name, old_file_name)
    return old_file_name

def change_bytagname(doc, tag_name, value):
    """ change text value of 'author' """
    node = doc.getElementsByTagName(tag_name)
    node[0].firstChild.nodeValue = value

def save_changes(new_file_name, doc):
    """ persist changes to new file """
    xml_file = open(new_file_name, "w")
    doc.writexml(xml_file)
    xml_file.close()
    

path = "/home/aidin/yolo-keras-tf-py27/keras-yolo2/data/times/valid/annots"

fnames = sorted([f for f in os.listdir(path) if
                 os.path.isfile(os.path.join(path, f))])

tag = "name"
value = "times"

tag = "filename"

for i, fname in enumerate(fnames):
    ffname = os.path.join(path, fname)
    ffname_ = create_backup(ffname)
    print(ffname_)
    doc = parse(ffname_)
    
    change_bytagname(doc, tag, fname[:-4]+".jpg")
    save_changes(ffname, doc)
    
print(str(i+1) + " files updated.")
#    fname_backup = create_backup(os.path.join(path,fname))
    
    
    
    