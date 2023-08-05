import sys
print(sys.path)
import xml.etree.ElementTree as ET
import merge_kdbx.clparser
import merge_kdbx.kdbx_xml_util
import datetime
from copy import deepcopy

def retrieve_and_update_entries(src_elem, dst_elem):
    # start with root.Root
    for src_child_entry in src_elem.findall('Entry'):
        entry_title = merge_kdbx.kdbx_xml_util.get_element_title(src_child_entry)
        dst_child_entry = merge_kdbx.kdbx_xml_util.find_entry_by_title(dst_elem, entry_title)
        merge_kdbx.kdbx_xml_util.update_dst_entry(src_child_entry, dst_child_entry, dst_elem)
    
    for src_child_group in src_elem.findall('Group'):
        group_name = src_child_group.find('Name').text
        dst_child_group = merge_kdbx.kdbx_xml_util.find_group(dst_elem, group_name)
        if dst_child_group == None:
            merge_kdbx.kdbx_xml_util.update_dst_group(src_child_group, dst_elem)
        else:
            # dst and src have the same group. retrieve the child group
            retrieve_and_update_entries(src_child_group, dst_child_group)

def main():
    try:
        args = merge_kdbx.clparser.parse()
    except ValueError as e:
        print(str(e))
        sys.exit(1)
    
    src_xml_trees = [ET.parse(x) for x in args.srcs]
    src_xml_roots = [x.getroot() for x in src_xml_trees]
    dst_tree = ET.parse(args.srcs[0])
    dst = dst_tree.getroot()

    # root.Root.Group.Entry.{Times.LastModificationTime, String.Password, String.Title}
    for target_xml_root in [x.find('Root') for x in src_xml_roots[1:]]:
        retrieve_and_update_entries(target_xml_root, dst.find('Root'))

    
    dst_tree.write(args.dst)

if __name__ == '__main__':
    main()