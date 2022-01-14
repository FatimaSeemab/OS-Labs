import os
import math

# !/usr/bin/python
global MAX_BLOCKS, BLOCK_SIZE, CURRENT_DIR
MAX_BLOCKS = 1024
BLOCK_SIZE = 16
CURRENT_DIR = []

dir_str = {}
openfile = {}
blocks = {}

for i in range(MAX_BLOCKS):
    blocks[i] = {"data": "", "next": "None", "occupied": False}


# Function to check wether the key belongs to the dictionary
def checkKey(dict, key):
    if key in dict.keys():
        return True
    return False


def goToCurrentDir():
    o = dir_str
    for dir in CURRENT_DIR:
        o = o[dir]
    return o


def create_file(name):
    f, e = os.path.splitext(name)
    if (e != ""):
        # use the first unoccupied block from the blocks dictionary
        unoccupied = [i for i in range(MAX_BLOCKS) if blocks[i]["occupied"] == False]
        if len(unoccupied) == 0:
            print("[-] Error! space not available.")
            return
        block_idx = unoccupied[0]

        # go to the current directory path
        o = dir_str
        for dir in CURRENT_DIR:
            o = o[dir]

        # update the bitMap and the memoryMap
        o[name] = {"start_block": block_idx}
        blocks[block_idx]["occupied"] = True
    else:
        print("[-] Error! enter name along with extension.")


def create_directory(name):
    o = dir_str
    chdir = checkKey(o, name)
    for dir in CURRENT_DIR:
        o = o[dir]
        chdir = checkKey(o, name)
        # if specified directory found, chdir becomes true
        if (chdir):
            break;

    if (chdir):
        print("Directory with the name '" + name + "' already exists")
    else:
        o[name] = {}


def change_directory(name):
    if (name == ".."):
        CURRENT_DIR.pop()
        return
    elif (name == "~"):
        CURRENT_DIR.clear()
        return

    # check inside current directory
    o = dir_str
    # chdir = checkKey(o, name)
    for dir in CURRENT_DIR:
        o = o[dir]
        # if specified directory found, chdir becomes true
        # if chdir:
        #     break
    chdir = checkKey(o, name)
    if chdir:
        CURRENT_DIR.append(name)
    else:
        print("[-] Error! no directory named '" + name + "' exists in the current directory '")


# def write_file(name,data):
#      o = dir_str
#      chdir = checkKey(o, name)


# if already open then???

def open(name, mode="r"):
    if (mode not in ["r", "w"]):
        print("[-] mode", mode, "not supported!\n")
    else:
        o = goToCurrentDir()
        chdir = checkKey(o, name)

        if chdir:
            wasOpen = False
            for key in list(openfile):
                if name == openfile[key]['filename'] and CURRENT_DIR == openfile[key]["path"]:
                    print("File is already open!")
                    return

            # issue in this line
            index = len(openfile.items())
            openfile[index] = {"filename": name, "mode": mode, "path": CURRENT_DIR}
        else:
            print("[-] Error! no file named '" + name + "' exists in the current directory '" + CURRENT_DIR[
                len(CURRENT_DIR) - 1] + "'")


# if multiple instances allowed??
# if not no need to worry
# or get path here
def close(name):
    # no need to check if file exists because if it didn't, it won't be open
    # also because an open file can not be deleted
    wasOpen = False
    for key in list(openfile):
        if name == openfile[key]['filename'] and CURRENT_DIR == openfile[key]["path"]:
            wasOpen = True
            openfile.pop(key)
    if (not wasOpen):
        print("file is already closed!")


def delete(name):
    # you first have to close a file before deleting
    print()


def write(name, data):
    wasOpen = False
    mode = ""
    for key in list(openfile):
        if name == openfile[key]['filename'] and CURRENT_DIR == openfile[key]["path"]:
            wasOpen = True
            if openfile[key]["mode"] == "w":
                mode = "write"
    if wasOpen and mode == "write":
        abc = goToCurrentDir()

        block_index = abc[name]['start_block']
        data_length = len(data)
        block_data_length = len(blocks[block_index]['data'])

        # All the data can bee placed in one block
        if (data_length + block_data_length) < 16:
            blocks[block_index]['data'] = blocks[block_index]['data'] + data
        # data in multiple blocks including starting index of the file
        else:
            if block_data_length == 16:
                next = blocks[block_index]['next']
                while next != "None":
                    next = blocks[next]['next']
                    block_data_length = blocks[next]['data']
                    block_index = next
            space_in_block = int(16 - block_data_length)
            blocks[block_index]['data'] = blocks[block_index]['data'] + data[0:space_in_block]
            data_left = data_length - space_in_block
            starting_idx = space_in_block
            prev_bloc_idx = block_index

            k = math.ceil(data_left / 16)
            for f in range(k):
                for j in range(MAX_BLOCKS):
                    if blocks[j]["occupied"]:
                        continue;
                    else:
                        blocks[j]["occupied"] = True
                        if data_left < 16:
                            blocks[j]['data'] = data[starting_idx:starting_idx + data_left]
                            blocks[prev_bloc_idx]['next'] = j
                            break;
                        else:
                            stop_idx = starting_idx + 16
                            blocks[j]['data'] = data[starting_idx:stop_idx]

                            blocks[prev_bloc_idx]['next'] = j
                            starting_idx = stop_idx
                            prev_bloc_idx = j
                            break;

    else:
        if not wasOpen:
            print("File is  not opened ")
        elif mode != "write":
            print('File is  not opened in write mode')


def write_to_file(name, pos, data):
    wasOpen = False
    mode = ""
    k = 0
    data_length = len(data)
    for key in list(openfile):
        if name == openfile[key]['filename'] and CURRENT_DIR == openfile[key]["path"]:
            wasOpen = True
            if openfile[key]["mode"] == "w":
                mode = "write"
    if (wasOpen and mode == "write"):
        # print("file is open")
        abc = goToCurrentDir()
        file_found = False

        starting_idx = 0
        for i in abc:
            if i == name:
                file_found = True
        if file_found:
            block_index = (abc[name]['start_block'])

        if pos > 16:
                k = pos / 16
                k = int((k))
        starting_address = block_index
        for f in range(k):
            starting_address = blocks[starting_address]["next"]
        offset = pos - k * 16
        data_to_be_filled = data_length
        limit = 16 - offset

        no_of_blocks_replaced = math.ceil(((16 - pos) + data_length) / 16)
        print("block to be replaced",no_of_blocks_replaced)
        for f in range(no_of_blocks_replaced):
            written_data = blocks[starting_address]['data']
            if data_to_be_filled > 16:
                    data_to_be_filled = data_to_be_filled - limit
                    end = 16
            else:
                end = data_to_be_filled
                limit = limit + end

            already_placed = written_data[offset:end]
            # print("already placed",already_placed)
            newdata = data[starting_idx:limit]
            # print("new placed",newdata)
            correct_data = written_data.replace(already_placed, newdata)
            blocks[starting_address]['data'] = correct_data
            # print("correct data",correct_data)
            # print("datalength >>>>>>>",len(blocks[starting_address]['data']))
            starting_address = blocks[starting_address]['next']

            starting_idx = starting_idx + (end - offset)
            offset = 0

            limit = limit + end
    else:
        if not wasOpen:
            print("File is  not opened")
        elif mode != "write":
            print("File is  not opened in write mode")


def read(filename):
    wasOpen = False
    mode = ""
    buffer = ""
    for key in list(openfile):
        if filename == openfile[key]['filename'] and CURRENT_DIR == openfile[key]["path"]:
            wasOpen = True
            if openfile[key]["mode"] == "r":
                mode = "read"
    if (wasOpen and mode == "read"):
        abc = goToCurrentDir()
        block_idx = abc[filename]['start_block']
        while block_idx != "None":
            data = blocks[block_idx]['data']
            buffer = buffer + data
            block_idx = blocks[block_idx]['next']
        print(buffer)
    else:
        if not wasOpen:
            print("File is  not opened")
        elif mode != "read":
            print("File is  not opened in write mode")


def read_size(filename, start,size):
    wasOpen = False
    mode = ""
    count = 0
    datapos=0

    for key in list(openfile):
        if filename == openfile[key]['filename'] and CURRENT_DIR == openfile[key]["path"]:
            wasOpen = True
            if openfile[key]["mode"] == "r":
                mode = "read"
    if (wasOpen and mode == "read"):
        abc = goToCurrentDir()
        block_idx = abc[filename]['start_block']
        buffer = ""
        while block_idx != "None":
            if count > size:
                break;
            else:
                for i in range(len(blocks[block_idx]['data'])):
                    data = blocks[block_idx]['data']
                    datapos=datapos+1
                    if(datapos >= start):
                        buffer = buffer + data[i]
                        count = count + 1
                    if count > size:
                        break;
                block_idx = blocks[block_idx]['next']
        print(buffer)
    else:
        if not wasOpen:
            print("File is  not opened")
        elif mode != "read":
            print("File is  not opened in write mode")

# def truncate(file,size):


# def truncate(file,size):
#     count=0
#     abc = goToCurrentDir()
#     file_found = False
#     for i in abc:
#         if i == filename:
#             file_found = True
#         if file_found:
#             block_idx=abc[filename]['start_block']
#             buffer=""
#             while block_idx != "None" :
#                 if count>size:
#
#                     break;
#                 else:
#                     for i in range(len(blocks[block_idx]['data'])):
#                         data=blocks[block_idx]['data']
#                         buffer=buffer+data[i]
#                         count=count+1;
#                         if count>size:
#                             data[i:16]=""
#                             blocks[block_idx]['data']=data
#
#
#
#                     block_idx = blocks[block_idx]['next']
#             print(buffer)
#     else:
#         if not wasOpen:
#             print("File is  not opened")
#         elif mode != "read":
#             print("File is  not opened in write mode")
# create_file("file.txt")
create_directory("name")
change_directory("name")
create_directory("my")
change_directory("my")
change_directory("..")
create_file("file.txt")
# print(CURRENT_DIR)
# print(dir_str)
# print occupied blocks
# print([blocks[i] for i in range(MAX_BLOCKS) if blocks[i]["occupied"] == True])

# change_directory("my")
# change_directory("~")
# print(CURRENT_DIR)
# create_file("file.txt")
# create_directory("name")
# change_directory("name")
# change_directory("my")
# change_directory("~")

# open("file.txt", "r")
open("file.txt", "w")

print("open files:")
print(openfile)
write("file.txt", "An operating system (OS) is system software that manages computer hardware, software resources, ")
write_to_file("file.txt",5,"Hi i am fatima seemab")
close("file.txt")
open("file.txt", "r")
# write("file.txt",
#       "and provides common services for computer programs. ... Operating systems are found on many devices that contain a computer – from cellular phones and video game consoles to web servers and supercomputers.")
# write_to_file("file.txt", 5, "My name is fatima seemab")
# read("file.txt")
read_size("file.txt",2,5)
close("file.txt")
# change_directory("name")

# open("file.txt", "r")
# print("open files:")
# print(openfile)
# change_directory("my")
# print("open files:")
# print(openfile)
# print("open files dictionary after closing:")
# print(CURRENT_DIR)
#
# # print occupied blocks
print([blocks[i] for i in range(MAX_BLOCKS) if blocks[i]["occupied"] == True])
# print(dir_str)
