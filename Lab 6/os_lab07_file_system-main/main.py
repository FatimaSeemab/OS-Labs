import math
import os
import json

global MAX_BLOCKS, BLOCK_SIZE, CURRENT_DIR
MAX_BLOCKS = 32
BLOCK_SIZE = 16
CURRENT_DIR = []

dir_str = {}
blocks = {}
openfile = {}

# "occupied" has same role as a bit for each block in bitMap
for i in range(MAX_BLOCKS):
    blocks[i] = {"data": "", "next": None, "occupied": False}


# Prints the present working directory
def pwd():
    # root/ to show that we are in main dictionary
    path = "/root"
    for dir in CURRENT_DIR:
        path = path + "/" + dir
    print("pwd->", path)


# Function to check wether the key belongs to the dictionary
def checkKey(dict, key):
    if key in dict.keys():
        return True
    return False


# To access the content of particular directory
def goToDir(directory=CURRENT_DIR):
    o = dir_str
    for dir in directory:
        o = o[dir]
    return o


# To add file to directory structure and assign it the starting block
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
        o = goToDir()

        # update the "occupied" bit and the memory map
        o[name] = {"start_block": block_idx, "size": 0}
        blocks[block_idx]["occupied"] = True
        print(f"File '{name}' created successfully")
    else:
        print("[-] Error! enter name along with extension.")


# Create directory in current path, if there is no other directory of same name
def create_directory(name):
    o = dir_str
    for dir in CURRENT_DIR:
        o = o[dir]
    chdir = checkKey(o, name)
    if (chdir):
        print("Directory with the name '" + name + "' already exists")
    else:
        o[name] = {}


def change_directory(name):
    # go back to prev directory
    if (name == ".."):
        CURRENT_DIR.pop()
        return
    # return to root
    elif (name == "~"):
        CURRENT_DIR.clear()
        return

    # check inside current directory
    o = goToDir()
    chdir = checkKey(o, name)
    if chdir:
        CURRENT_DIR.append(name)
        pwd()
    else:
        print("[-] Error! no directory named '" + name + "' exists in the current directory '" + CURRENT_DIR[
            len(CURRENT_DIR) - 1] + "'")


# function to mov file from one location to another
def mov_file(source, destination):
    # splitting the source and destination path into separate string so that it can be transversed in the directory structure
    source_array = source.split("/")
    destination_array = destination.split("/")
    # storing file name in a variable to check the condition
    fileName = source_array[len(source_array) - 1]
    # accessing the directory structure
    o = dir_str
    # variable to store the information of the file that has been found
    x = ""

    # finding the source file in directory structure
    for dir in source_array:
        # if file is found then its data is stored in variable "x"
        chdir = checkKey(o, dir)
        if chdir:
            if dir == fileName:
                x = o[fileName]
                o.pop(fileName)
            else:
                o = o[dir]

    # finding the destination where the file is to be placed
    o = dir_str
    for dir2 in destination_array:
        chdir = checkKey(o, dir2)
        if chdir:
            o = o[dir2]

    new_name = ""
    # if the same name file exists then the user is prompted to enter the new name for the file
    chdir = checkKey(o, fileName)
    if chdir:
        # if already exists, ask user to rename
        while (chdir):
            new_name = input("Rename file as file with same name already exixts: ")
            chdir = checkKey(o, fileName)
    else:
        new_name = source_array[len(source_array) - 1]
    o[new_name] = x


# function to open the file according to the mode
def open_file(name, mode="r"):
    # file can be opened in three modes read,write and read write
    if (mode not in ["r", "w", "rw"]):
        print("[-] mode", mode, "not supported!\n")
    else:
        o = goToDir()
        # checking the file in the directory
        chdir = checkKey(o, name)
        if chdir:
            for key in list(openfile):
                # condition if a file is already opened
                if name == openfile[key]['filename'] and CURRENT_DIR == openfile[key]["path"]:
                    print("File is already open!")
                    return

            # if not wasOpen, add file to openfile list:
            index = len(openfile.items())
            cur = CURRENT_DIR.copy()
            openfile[index] = {"filename": name, "mode": mode, "path": cur}
        else:
            print("[-] Error! no file named '" + name + "' exists in the current directory '" + CURRENT_DIR[
                len(CURRENT_DIR) - 1] + "'")


# This function will close the file so no read,write function can be performed on file
def close(name):
    wasOpen = False
    for key in list(openfile):
        if name == openfile[key]['filename'] and CURRENT_DIR == openfile[key]["path"]:
            wasOpen = True
            openfile.pop(key)
    if (not wasOpen):
        print("file is already closed!")


# Write function will write the data to file blocks
def write(name, data):
    wasOpen = False
    mode = ""
    # checking if the file is open or not
    for key in list(openfile):
        if name == openfile[key]['filename'] and CURRENT_DIR == openfile[key]["path"]:
            wasOpen = True
            if openfile[key]["mode"] in ["w", "rw"]:
                mode = "write"
    if wasOpen and mode == "write":
        abc = goToDir()

        block_index = abc[name]['start_block']
        data_length = len(data)
        block_data_length = len(blocks[block_index]['data'])
        # All the data can bee placed in one block
        if (data_length + block_data_length) < BLOCK_SIZE:
            blocks[block_index]['data'] = blocks[block_index]['data'] + data
            abc[name]['size'] = abc[name]['size'] + data_length
        # data in multiple blocks including starting index of the file
        else:
            # if blocks are already filled, it will search the next bblock until one is found which have some space
            if block_data_length == BLOCK_SIZE:
                next = blocks[block_index]['next']
                while next != None:
                    block_data_length = len(blocks[block_index]['data'])
                    block_index = next
                    next = blocks[next]['next']

            space_in_block = int(BLOCK_SIZE - block_data_length)
            blocks[block_index]['data'] = blocks[block_index]['data'] + data[0:space_in_block]
            abc[name]['size'] = abc[name]['size'] + space_in_block
            data_left = data_length - space_in_block
            starting_idx = space_in_block
            prev_bloc_idx = block_index

            # Loop for assigning the number of blocks needed for data entered
            k = math.ceil(data_left / BLOCK_SIZE)
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
                            data_left=data_left-BLOCK_SIZE
                            blocks[prev_bloc_idx]['next'] = j
                            starting_idx = stop_idx
                            prev_bloc_idx = j
                            break

    else:
        if not wasOpen:
            print("File is not opened ")
        elif mode != "write":
            print('File is not opened in write mode')


# This function will write to a file at certain pos
def write_to_file(name, pos, data):
    wasOpen = False
    mode = ""
    k = 0
    blocks_replaced=0
    data_length = len(data)

    # checking for the file is either opened or not and also its mode
    for key in list(openfile):
        if name == openfile[key]['filename'] and CURRENT_DIR.copy() == openfile[key]["path"]:
            wasOpen = True
            if openfile[key]["mode"] in ["w", "rw"]:
                mode = "write"
    if (wasOpen and mode == "write"):
        abc = goToDir()
        starting_idx = 0
        block_index = abc[name]['start_block']
        # if file is already empty
        if abc[name]['size'] == 0 and pos == 0:
            write(name, data)
            return

        # condition for file size less than pos
        if pos > abc[name]['size']:
            print("Invalid position, out of bound of file size.")
            return
        if pos +data_length >abc[name]['size']:
            data=data[:abc[name]['size']-pos]
            data_length = len(data)


        if pos >= BLOCK_SIZE:
            k = pos / BLOCK_SIZE
            k = int(k)
        starting_address = block_index
        for f in range(k):
            starting_address = blocks[starting_address]["next"]
        offset = pos - k * BLOCK_SIZE
        data_to_be_filled = data_length
        limit = BLOCK_SIZE - offset
        blocks_replaced= math.ceil(((BLOCK_SIZE - offset) + data_length) / BLOCK_SIZE)

        if offset == 0:
           blocks_replaced= math.ceil(data_length / BLOCK_SIZE)

        # Loop for assigning the number of blocks needed for data overwrite
        for f in range(blocks_replaced):
            written_data = blocks[starting_address]['data']
            # for setting the variables for slicing of data and file data where it is overwritten
            if data_to_be_filled > BLOCK_SIZE:
                data_to_be_filled = data_length - limit
                end = BLOCK_SIZE
            else:
                end = offset + data_to_be_filled
                if (end > BLOCK_SIZE):
                    end = data_to_be_filled
                limit = limit + end

            already_placed = written_data[offset:end]

            newdata = data[starting_idx:limit]

            correct_data = written_data.replace(already_placed, newdata)
            blocks[starting_address]['data'] = correct_data

            starting_address = blocks[starting_address]['next']
            if (not starting_address):
                print("Further blocks not assigned yet")
                return
            # setting the variables for next iteration
            starting_idx = starting_idx + (end - offset)
            offset = 0
            limit = limit + end
    else:
        if not wasOpen:
            print("File is not opened")
        elif mode != "write":
            print("File is not opened in write mode")


# This function will read the data from the file name specified.
def read(filename):
    wasOpen = False
    mode = ""
    buffer = ""
    # Check for either file is opened or not
    for key in list(openfile):
        if filename == openfile[key]['filename'] and CURRENT_DIR == openfile[key]["path"]:
            wasOpen = True
            if openfile[key]["mode"] in ["r", "rw"]:
                mode = "read"
    if (wasOpen and mode == "read"):
        abc = goToDir()
        block_idx = abc[filename]['start_block']
        print("Reading the contents of file: " + filename)
        # For storing data of all blocks in a buffer
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


# Function for reading the size of data from the specified starting point
def read_size(filename, start, size):
    wasOpen = False
    mode = ""
    count = 0
    datapos = 0
    # check for a file is either open or not
    for key in list(openfile):
        if filename == openfile[key]['filename'] and CURRENT_DIR == openfile[key]["path"]:
            wasOpen = True
            if openfile[key]["mode"] in ["r", "rw"]:
                mode = "read"
    if (wasOpen and mode == "read"):
        abc = goToDir()
        block_idx = abc[filename]['start_block']
        buffer = ""
        # For iterating over all the data blocks 
        while block_idx != None:
            # condition for buffer size less than specified size
            if count > size:
                break;
            else:
                for i in range(len(blocks[block_idx]['data'])):
                    data = blocks[block_idx]['data']
                    datapos = datapos + 1
                    # data is added to buffer if its position is after the specified starting point.
                    if (datapos >= start):
                        buffer = buffer + data[i]
                        count = count + 1
                    if count > size:
                        break;
                block_idx = blocks[block_idx]['next']
        if (count < size):
            print(f"Only {count} bytes in the file.")
        print(buffer)
    else:
        if not wasOpen:
            print("File is  not opened")
        elif mode != "read":
            print("File is  not opened in read mode")


# moving the data within file
def mov_within_file(filename, start, to, size):
    # reads the data from the file which is to edited
    buffer = read(filename)
    # the text which is to be moved
    text = buffer[start:start + size]
    # storing the data where it is specified by the user
    if (start >= to):
        buffer = buffer[0:to] + text + buffer[to:start] + buffer[start + size:len(buffer)]
    else:
        buffer = buffer[0:start] + buffer[start + size:to] + text + buffer[to:len(buffer)]
    print(buffer)
    # writing the data back to file
    write_to_file(filename, 0, buffer)


def truncate(filename, path_to_file, size):
    if (type(path_to_file) is str) and path_to_file != "":
        o = goToDir(path_to_file.split("/"))
    else:
        # in case file_path is []
        o = dir_str

    # in case we want to truncate to size 0
    last_block_to_keep = block_idx = o[filename]['start_block']

    print("Truncating the contents of file: " + filename)
    original_blocks = math.ceil(o[filename]['size'] / BLOCK_SIZE)
    new_blocks = math.ceil(size / BLOCK_SIZE)
    bytes_in_last_block = size % BLOCK_SIZE
    if (size != 0 and bytes_in_last_block == 0):
        bytes_in_last_block = BLOCK_SIZE
    blocks_to_truncate = original_blocks - new_blocks

    # Delete the blocks which are to be completely truncated
    # Update the "occupied" status of these block and set next to None
    # Also update the file size
    i = original_blocks
    while (i > 0):
        if (i <= blocks_to_truncate):
            blocks[block_idx]['occupied'] = False
            blocks[block_idx]['data'] = ""
            new_idx = blocks[block_idx]['next']
            blocks[block_idx]['next'] = None
            block_idx = new_idx
            o[filename]['size'] -= BLOCK_SIZE
        else:
            last_block_to_keep = block_idx
            block_idx = blocks[block_idx]['next']
        i -= 1

    # Update the size of file
    if (o[filename]['start_block'] == last_block_to_keep):
        o[filename]['size'] = bytes_in_last_block
    else:
        o[filename]['size'] = o[filename]['size'] - BLOCK_SIZE + bytes_in_last_block
    # Truncate the content in the last block and set its "next" to None
    blocks[last_block_to_keep]['next'] = None
    blocks[last_block_to_keep]['data'] = blocks[last_block_to_keep]['data'][:bytes_in_last_block]


def delete(filename, path_to_file):
    if (type(path_to_file) is str) and path_to_file != "":
        o = goToDir(path_to_file.split("/"))
    else:
        # in case file_path is []
        o = dir_str
    for key in list(openfile):
        if filename == openfile[key]['filename'] and path_to_file == openfile[key]["path"]:
            print("File must be closed before deleting!")
            return
    block_idx = o[filename]['start_block']
    # Loop over the blocks of file and delete file content
    # Also update the "next" and "occupied" keys of blocks
    while (block_idx != None):
        blocks[block_idx]['occupied'] = False
        blocks[block_idx]['data'] = ""
        new_idx = blocks[block_idx]['next']
        blocks[block_idx]['next'] = None
        block_idx = new_idx
    # remove file from directory structure
    o.pop(filename)


# function to store data into the sample.dat file
def store_data():
    # data array to hold both directory and block structure
    data = []
    data.append(dir_str)
    data.append(blocks)
    # storing into the file
    with open("sample.dat", "w") as fp:
        json.dump(data, fp)


# function to load data into the sample.dat file
def load_data():
    # accessing the global variables
    global dir_str
    global blocks
    # loading data from the sample.dat file when the program runs
    with open('sample.dat', 'r') as fp:
        data = json.load(fp)

    dir_str = data[0]
    blocks = data[1]
    # making key of blocks integer
    blocks = {int(k): v for k, v in blocks.items()}


# function to print memory map on the console
def memory_map(directory_structure, spacing=0):
    # accessing the directory structure
    o = directory_structure
    # looping through all the directory structure
    for dir in directory_structure:
        # getting the extension if "dir" is a file
        f, e = os.path.splitext(dir)
        # if its a directory
        if e == "":
            # printing dir name
            print("\t" * spacing, "Directory: ", dir, sep="\t")
            memory_map(o[dir], spacing + 1)
        else:
            # if its a file
            blocks_of_file = []
            block_num = o[dir]["start_block"]
            starting_address = hex(id(o[dir]["start_block"]))
            blocks_of_file.append(block_num)
            # reading the block numbers which are occupied by the file
            while block_num is not None:
                block_num = blocks[block_num]['next']
                if block_num is not None:
                    blocks_of_file.append(block_num)
            # printing file information
            print("\t" * spacing, "File: ", dir, blocks_of_file, "File Size: ", str(o[dir]["size"]) + " bytes",
                  "Starting Address: " + str(starting_address), sep="\t")


def menu():
    print("**************Menu**************")
    print("0. Print working directory")
    print("1. Create a file")
    print("2. Delete a file")
    print("3. Make directory")
    print("4. Change directory")
    print("5. Move a file")
    print("6. Open a file")
    print("7. Close a file")
    print("8. Write in a file")
    print("9. Write in a file at specific position")
    print("10. Read a file")
    print("11. Read a file from specific position")
    print("12. Move text in a file")
    print("13. Truncate text in a file")
    print("14. Show memory map")
    print("15. Show Directory Structure")
    print("16. Show filled Blocks")
    print("17. Show Opened Files List")
    print("18. Exit")
    print("********************************")


load_data()
while 1:
    menu()
    choice = int(input("Enter your choice: "))
    if choice == 0:
        pwd()

    elif choice == 1:
        file_name = input("Enter a file name: ")
        create_file(file_name)

    elif choice == 2:
        path_name = input("Enter path to file: ")
        file_name = input("Enter a file name: ")
        delete(file_name, path_name)

    elif choice == 3:
        dir_name = input("Enter the directory name: ")
        create_directory(dir_name)

    elif choice == 4:
        dir_name = input("Enter the directory name: ")
        change_directory(dir_name)

    elif choice == 5:
        source = input("Enter source file path: ")
        destination = input("Enter destination path: ")
        mov_file(source, destination)

    elif choice == 6:
        file_name = input("Enter a file name: ")
        mode = input("Enter the mode [ r, w, rw ]: ")
        open_file(file_name, mode)

    elif choice == 7:
        file_name = input("Enter a file name: ")
        close(file_name)

    elif choice == 8:
        file_name = input("Enter a file name: ")
        text = input("Enter the text: ")
        write(file_name, text)

    elif choice == 9:
        file_name = input("Enter a file name: ")
        pos = input("Enter position to write text: ")
        text = input("Enter the text: ")
        write_to_file(file_name, int(pos), text)

    elif choice == 10:
        file_name = input("Enter a file name: ")
        read(file_name)

    elif choice == 11:
        file_name = input("Enter a file name: ")
        start = input("Enter start location:")
        size = input("Enter a size of data to be read: ")
        read_size(file_name, int(start), int(size))

    elif choice == 12:
        file_name = input("Enter a file name: ")
        start = input("Enter start location: ")
        size = input("Enter a size of data to be read: ")
        to = input("Enter location where to write text: ")
        mov_within_file(file_name, int(start), int(to), int(size))

    elif choice == 13:
        file_name = input("Enter a file name: ")
        path_name = input("Enter path to file: ")
        size = input("Enter a size of data to be kept: ")
        truncate(file_name, path_name, int(size))

    elif choice == 14:
        memory_map(dir_str)

    elif choice == 15:
        print(dir_str)

    elif choice == BLOCK_SIZE:
        print([blocks[i] for i in range(MAX_BLOCKS) if blocks[i]["occupied"] == True])

    elif choice == 17:
        print(openfile)

    elif choice == 18:
        store_data()
        exit()
