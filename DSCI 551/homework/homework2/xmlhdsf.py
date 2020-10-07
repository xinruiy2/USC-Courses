import datetime
from lxml import etree
import sys

if len(sys.argv) < 3 or len(sys.argv) > 3:
    print("Invalid form of input")
    exit()

file_name = sys.argv[1]
directory_whole = sys.argv[2]

if directory_whole[-1] == "/":
    directory_whole = directory_whole[:-1]

directory = directory_whole[1:].split("/")
f = open(file_name)
tree = etree.parse(f)

# First get to directory if exists
root_id = 0
# Get the root directory first
for element in tree.xpath('//inode[name=""]//id'):
    root_id = element.text

for dir in directory:
    isFound = False
    for element in tree.xpath('//directory[parent=%s]//child' % root_id):
        child_id = element.text
        if tree.xpath('//inode[id=%s]//name' % child_id)[0].text == dir:
            root_id = child_id
            isFound = True
            break
    if isFound == False:
        print("ls: %s': No such file or directory" % directory_whole)
        break

if isFound:
    ret = []
    permission_list = ["---", "--x", "-w-", "-wx", "r--", "r-x", "rw-", "rwx"]
    if tree.xpath('//inode[id=%s]//type' % root_id)[0].text == "DIRECTORY":
        child_list = []
        for element in tree.xpath('//directory[parent=%s]//child' % root_id):
            child_list.append(element.text)
        print("Found %d items" % len(child_list))
        for id in child_list:
            sm_list = []
            user_list = tree.xpath('//inode[id=%s]//permission' % id)[0].text.split(":")
            permission_bit = user_list[-1][1:]
            permission_string = ""
            for char in permission_bit:
                permission_string += permission_list[int(char)]
            if tree.xpath('//inode[id=%s]//type' % id)[0].text == "FILE":
                permission_string = "-" + permission_string
                sm_list.append(permission_string + "  " + tree.xpath('//inode[id=%s]//replication' % id)[0].text)
                total_size = 0
                for element in tree.xpath('//inode[id=%s]//blocks//numBytes' % id):
                    total_size += int(element.text)
                sm_list.append(user_list[0])
                sm_list.append(user_list[1])
                sm_list.append(str(total_size))
            elif tree.xpath('//inode[id=%s]//type' % id)[0].text == "DIRECTORY":
                permission_string = "d" + permission_string
                sm_list.append(permission_string + "  -")
                sm_list.append(user_list[0])
                sm_list.append(user_list[1])
                sm_list.append("0")
            modify_time = datetime.datetime.fromtimestamp(int(tree.xpath('//inode[id=%s]//mtime' % id)[0].text)/1e3).now().strftime('%Y-%m-%d %H:%M')
            sm_list.append(modify_time)
            sm_list.append(directory_whole + "/" + tree.xpath('//inode[id=%s]//name' % id)[0].text)
            ret.append(sm_list)
    elif tree.xpath('//inode[id=%s]//type' % root_id)[0].text == "FILE":
        id = root_id
        sm_list = []
        user_list = tree.xpath('//inode[id=%s]//permission' % id)[0].text.split(":")
        permission_bit = user_list[-1][1:]
        permission_string = "-"
        for char in permission_bit:
            permission_string += permission_list[int(char)]
        sm_list.append(permission_string + "  " + tree.xpath('//inode[id=%s]//replication' % id)[0].text)
        total_size = 0
        for element in tree.xpath('//inode[id=%s]//blocks//numBytes' % id):
            total_size += int(element.text)
        sm_list.append(user_list[0])
        sm_list.append(user_list[1])
        sm_list.append(str(total_size))
        modify_time = datetime.datetime.fromtimestamp(int(tree.xpath('//inode[id=%s]//mtime' % id)[0].text)/1e3).now().strftime('%Y-%m-%d %H:%M')
        sm_list.append(modify_time)
        sm_list.append(directory_whole)
        ret.append(sm_list)
    for row in ret:
        print("{: >8} {: >8} {: >8} {: >8} {: >8} {: >8} ".format(*row))
