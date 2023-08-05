import datetime
from copy import deepcopy

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

def find_group(root, group_name):
    for group in root.findall('Group'):
        if group.find('Name').text == group_name:
            return group
    return None

def find_entry_by_title(group, title):
    for entry in group.findall('Entry'):
        if get_element_title(entry) == title:
            return entry
    return None

def get_element_title(entry):
    for s in entry.findall('String'):
        if s.find('Key').text == 'Title':
            return s.find('Value').text
    return None

def update_dst_entry(src_entry, dst_entry, dst_group):
    if dst_entry == None:
        dst_group.append(src_entry)
    else:
        src_last_mod = get_entry_last_modification(src_entry)
        dst_last_mod = get_entry_last_modification(dst_entry)
        if src_last_mod > dst_last_mod:
            # dst_entry = deepcopy(src_entry)
            dst_group.remove(dst_entry)
            dst_group.append(src_entry)

def update_dst_group(src_group, dst_parent):
    dst_parent.append(src_group)

def get_entry_last_modification(entry):
    last_mod_text = entry.find('Times').find('LastModificationTime').text
    last_mod_time = datetime.datetime.strptime(last_mod_text, DATETIME_FORMAT)
    return last_mod_time