import math
import os

global MAX_BLOCKS, BLOCK_SIZE, CURRENT_DIR
MAX_BLOCKS = 32
BLOCK_SIZE = 16
CURRENT_DIR = []

dir_str = {}
blocks = {}
openfile = {}
for i in range(MAX_BLOCKS):
    blocks[i] = {"data": "", "next": None, "occupied": False}


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
        o[name] = {"start_block": block_idx, "size": 0}
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
        print("[-] Error! no directory named '" + name + "' exists in the current directory '" + CURRENT_DIR[
            len(CURRENT_DIR) - 1] + "'")


def mov_file(source, destination):
    source_array = source.split("/")
    destination_array = destination.split("/")
    print(source_array, destination_array)

    fileName = source_array[len(source_array) - 1]
    o = dir_str
    print("printing o on initialization", o)
    x = ""

    for dir in source_array:
        chdir = checkKey(o, dir)
        if chdir:
            if dir == fileName:
                x = o[fileName]
                o.pop(fileName)
            else:
                o = o[dir]

    o = dir_str
    for dir2 in destination_array:
        chdir = checkKey(o, dir2)
        if chdir:
            o = o[dir2]

    chdir = checkKey(o, fileName)
    if chdir:
        o[source_array[len(source_array) - 1] + "(1)"] = x
    else:
        o[source_array[len(source_array) - 1]] = x


def open(name, mode="r"):
    if (mode not in ["r", "w", "rw"]):
        print("[-] mode", mode, "not supported!\n")
    else:
        o = goToCurrentDir()
        chdir = checkKey(o, name)
        if chdir:
            for key in list(openfile):
                if name == openfile[key]['filename'] and CURRENT_DIR == openfile[key]["path"]:
                    print("File is already open!")
                    return

            # issue in this line
            # if not wasOpen:
            index = len(openfile.items())
            cur = CURRENT_DIR.copy()
            openfile[index] = {"filename": name, "mode": mode, "path": cur}
        else:
            print("[-] Error! no file named '" + name + "' exists in the current directory '" + CURRENT_DIR[
                len(CURRENT_DIR) - 1] + "'")


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


def write(name, data):
    wasOpen = False
    mode = ""
    for key in list(openfile):
        if name == openfile[key]['filename'] and CURRENT_DIR == openfile[key]["path"]:
            wasOpen = True
            if openfile[key]["mode"] in ["w", "rw"]:
                mode = "write"
    if wasOpen and mode == "write":
        abc = goToCurrentDir()

        block_index = abc[name]['start_block']
        data_length = len(data)
        block_data_length = len(blocks[block_index]['data'])
        # All the data can bee placed in one block
        if (data_length + block_data_length) < BLOCK_SIZE:
            blocks[block_index]['data'] = blocks[block_index]['data'] + data
            abc[name]['size'] = abc[name]['size'] + data_length
        # data in multiple blocks including starting index of the file
        else:
            if block_data_length == BLOCK_SIZE:
                next = blocks[block_index]['next']
                while next != None:
                    next = blocks[next]['next']
                    block_data_length = blocks[next]['data']
                    block_index = next

            space_in_block = int(BLOCK_SIZE - block_data_length)
            blocks[block_index]['data'] = blocks[block_index]['data'] + data[0:space_in_block]
            abc[name]['size'] = abc[name]['size'] + space_in_block
            data_left = data_length - space_in_block
            starting_idx = space_in_block
            prev_bloc_idx = block_index

            k = math.ceil(data_left / BLOCK_SIZE)
            print("k 0000", k)
            for f in range(k):
                for j in range(MAX_BLOCKS):
                    if blocks[j]["occupied"]:
                        continue
                    else:
                        blocks[j]["occupied"] = True
                        if data_left < BLOCK_SIZE:
                            blocks[j]['data'] = data[starting_idx:starting_idx + data_left]
                            abc[name]['size'] = abc[name]['size'] + data_left
                            blocks[prev_bloc_idx]['next'] = j
                            break
                        else:
                            stop_idx = starting_idx + BLOCK_SIZE
                            blocks[j]['data'] = data[starting_idx:stop_idx]
                            abc[name]['size'] = abc[name]['size'] + BLOCK_SIZE
                            blocks[prev_bloc_idx]['next'] = j
                            starting_idx = stop_idx
                            prev_bloc_idx = j
                            break

    else:
        if not wasOpen:
            print("File is not opened ")
        elif mode != "write":
            print('File is not opened in write mode')


def write_to_file(name, pos, data):
    wasOpen = False
    mode = ""
    k = 0
    data_length = len(data)
    for key in list(openfile):
        if name == openfile[key]['filename'] and CURRENT_DIR == openfile[key]["path"]:
            wasOpen = True
            if openfile[key]["mode"] in ["w", "rw"]:
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

        if pos > BLOCK_SIZE:
            k = pos / BLOCK_SIZE
            k = int(k)
            print("k = ",k)
        starting_address = block_index
        # print("startkjhkhu",starting_address)
        for f in range(k):
            starting_address = blocks[starting_address]["next"]

        offset = pos - k * BLOCK_SIZE
        data_to_be_filled = data_length
        limit = BLOCK_SIZE - offset

        no_of_blocks_replaced = int(((BLOCK_SIZE - pos) + data_length) / BLOCK_SIZE)

        # hi, i am fatima seemab not writing correctly
        for f in range(no_of_blocks_replaced-1):
            written_data = blocks[starting_address]['data']

            if data_to_be_filled > BLOCK_SIZE:
                data_to_be_filled = data_to_be_filled - BLOCK_SIZE
                end = BLOCK_SIZE
            else:
                end = data_to_be_filled
                limit = limit + end

            already_placed = written_data[offset:end]
            newdata = data[starting_idx:limit]
            correct_data = written_data.replace(already_placed, newdata)
            blocks[starting_address]['data'] = correct_data
            print("datalength >>>>>>>",len(blocks[starting_address]['data']))
            starting_address = blocks[starting_address]['next']

            starting_idx = starting_idx + (end - offset)
            offset = 0
            limit = limit + end
    else:
        if not wasOpen:
            print("File is not opened")
        elif mode != "write":
            print("File is not opened in write mode")


def read(filename):
    wasOpen = False
    mode = ""
    buffer = ""
    for key in list(openfile):
        if filename == openfile[key]['filename'] and CURRENT_DIR == openfile[key]["path"]:
            wasOpen = True
            if openfile[key]["mode"] in ["r", "rw"]:
                mode = "read"
    if (wasOpen and mode == "read"):
        abc = goToCurrentDir()
        block_idx = abc[filename]['start_block']
        print("Reading the contents of file: " + filename)
        while block_idx != None:
            data = blocks[block_idx]['data']
            buffer = buffer + data
            block_idx = blocks[block_idx]['next']
        print(buffer)
        print("lenght of buffer in read", len(buffer))
        return buffer
    else:
        if not wasOpen:
            print("File is not opened")
        elif mode != "read":
            print("File is not opened in read mode")


def read_size(filename, start, size):
    wasOpen = False
    mode = ""
    count = 0
    datapos = 0
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
                    datapos = datapos + 1
                    if (datapos >= start):
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


def mov_within_file(filename, start, to, size):
    buffer = read(filename)
    print(buffer)
    text = buffer[start:start + size]
    buffer = buffer[0:to] + text + buffer[to:start] + buffer[start + size:len(buffer)]
    print(buffer)
    print(len(buffer))
    write_to_file("file.txt", 0, buffer)

def memorymap():
    First_Level = []
    print(dir_str)
    i=0
    # key: object
    for key,value in (dir_str.items()):
        print("The files and directory of level 1 are")
        if
        First_Level.append(key)
        i = i+1
        # for i in list(value):
        #     if i!="start_block" and i !="size":
        #         print("The directories inside",value," are",i)
        #     else:
        #         print("The files inside",value," are" ,i)
    print("The directories of first level are: ")
    k=0
    for j in list(First_Level):
        if k<i:
            print(First_Level[k])
            k=k+1
        # dir=(dir_str[i])
        # print("The main directory is ",dir)
        # for j in list(dir_str[i]):
        #     file=dir_str[i][j]
        #     print(file)




# An opHi i am fatima seemabOS) is system software that manages computer hardware, software resources,
# software resources, An opHi i am fatima seemabOS) is system software that manages computer hardware,


# create_file("file.txt")
create_directory("name")
change_directory("name")
create_directory("my")
change_directory("my")
change_directory("..")
change_directory("..")
create_file("file.txt")
memorymap()
# print(CURRENT_DIR)
# print("dir", dir_str)

# # mov_file("file.txt", "name")
# # mov_file("name/file.txt", "name/my")
# mov_file("name/my/file.txt", "name")

# change_directory("my")
# change_directory("~")
# print(CURRENT_DIR)
# create_file("file.txt")
# create_directory("name")
# change_directory("name")
# change_directory("my")
# change_directory("~")
# open("file.txt", "w")
# print("open files:")
# print(openfile)
#
# change_directory("name")
# open("file.txt", "r")
# print("2. open files:")
# print(openfile)
#
# change_directory("name")
# # change_directory("my")
# close("file.txt")
# print("open files after closing:")
# print(openfile)
# # print(CURRENT_DIR)
# change_directory("~")
#
# write("file.txt", "An operating system (OS) is system software that manages computer hardware, software resources, ")
# print([blocks[i] for i in range(MAX_BLOCKS) if blocks[i]["occupied"] == True])
#
# write_to_file("file.txt", 5, "Hi i am fatima seemab")
# print([blocks[i] for i in range(MAX_BLOCKS) if blocks[i]["occupied"] == True])
# close("file.txt")
#
# open("file.txt", "rw")
# read("file.txt")
#
# mov_within_file("file.txt", 80, 0, 21)
#
# print([blocks[i] for i in range(MAX_BLOCKS) if blocks[i]["occupied"] == True])
#
# read("file.txt")
