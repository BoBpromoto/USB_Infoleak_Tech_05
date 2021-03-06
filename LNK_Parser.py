#!/usr/bin/python
# -* encoding : utf-8 *-
# _* encoding : cp949 *-

# https://github.com/gold1029/pylnker/blob/master/pylnker.py

import sys, datetime, binascii
import os
from struct import *
import datetime

# Hash for Volume types, Lnk_parser result value
vol_type = {"0":"[DRIVE_UNKNOWN]", "1":"[DRIVE_NO_ROOT_DIR]", "2":"[DRIVE_REMOVABLE]","3":"[DRIVE_FIXED]",
"4":"[DRIVE_REMOTE]", "5":"[DRIVE_CDROM]", "6":"[DRIVE_RAMDISK]"}

def reverse_hex(HEXDATE):
    hexVals = [HEXDATE[i:i + 2] for i in range(0, 16, 2)]
    reversedHexVals = hexVals[::-1]
    return ''.join(reversedHexVals)


def assert_lnk_signature(f):
    f.seek(0)
    sig = f.read(4)
    # print (sig)
    guid = f.read(16)
    if sig != b'L\x00\x00\x00':
        raise Exception("This is not a .lnk file.")
    if guid != b'\x01\x14\x02\x00\x00\x00\x00\x00\xc0\x00\x00\x00\x00\x00\x00F':
        raise Exception("Cannot read this kind of .lnk file.")


# read COUNT bytes at LOC and unpack into binary
def read_unpack_bin(f, loc, count):
    # jump to the specified location
    f.seek(loc)

    raw = f.read(count)
    result = ""
    # print (("{0:08b}".format(ord(raw)))[::-1])
    for b in raw:
        result += ("{0:08b}".format(ord(raw)))[::-1]
    return result


# read COUNT bytes at LOC and unpack into ascii
def read_unpack_ascii(f,loc,count):
    # jump to the specified location
    f.seek(loc)

    # should interpret as ascii automagically
    return f.read(count)


# read COUNT bytes at LOC
def read_unpack(f, loc, count): 
    # jump to the specified location
    f.seek(loc)

    raw = f.read(count)

    result = ""
    result += binascii.hexlify(raw).decode("utf-8")

    return result

# Read a null terminated string from the specified location.
def read_null_term(f, loc):
    result = b""
    f.seek(loc)
    string = f.read(1)
    while string != b"\x00":
        result += (string)
        string = f.read(1)
    return result.decode("euc-kr")

# adapted from pylink.py
def ms_time_to_unix_str(windows_time):
    time_str = ''
    try:
        unix_time = windows_time / 10000000.0 - 11644473600
        time_str = str(datetime.datetime.fromtimestamp(unix_time))
    except:
        pass
    return time_str

def add_info(f,loc):

    tmp_len_hex = reverse_hex(read_unpack(f,loc,2))
    tmp_len = 2 * int(tmp_len_hex, 16)

    loc += 2

    if (tmp_len != 0):
        tmp_string = read_unpack_ascii(f, loc, tmp_len)
        now_loc = f.tell()
        return (tmp_string, now_loc)
    else:
        now_loc = f.tell()
        return (None, now_loc)


def parse_lnk(filename):
    #read the file in binary module
    lnk_info = {}
    f = open(filename, 'rb')
    flags = reverse_hex(read_unpack(f,20,4))

    try:
        assert_lnk_signature(f)
    except Exception as e:
        return "[!] Exception: "+ str(e)

    # Create time 8bytes @ 1ch = 28

    create_time = reverse_hex(read_unpack(f,28,8))
    c_time = ms_time_to_unix_str(int(create_time, 16)).split(".")[0]

    # Access time 8 bytes@ 0x24 = 36D
    access_time = reverse_hex(read_unpack(f,36,8))
    a_time = ms_time_to_unix_str(int(access_time, 16)).split(".")[0]

    # Modified Time8b @ 0x2C = 44D
    modified_time = reverse_hex(read_unpack(f,44,8))
    m_time = ms_time_to_unix_str(int(modified_time, 16)).split(".")[0]

    #------------------------------------------------------------------------
    # End of Flag parsing
    #------------------------------------------------------------------------

    # get the number of items
    if flags[-1] in ("b") : #https://msdn.microsoft.com/en-us/library/dd871305.aspx - [MS-SHLLINK].pdf
        items_hex = reverse_hex(read_unpack(f,76,2))
        items = int(items_hex, 16)

        list_end = 78 + items

        struct_start = list_end
        vol_flags_off = struct_start + 8
        local_vol_off = struct_start + 12
        base_path_off = struct_start + 16

        vol_flags = read_unpack_bin(f,vol_flags_off,1)

        lnk_time = os.stat(filename)
        # lnk_created_time = datetime.datetime.fromtimestamp(os.path.getctime(filename)).strftime('%Y-%m-%d %H:%M:%S')
        lnk_modified_time = datetime.datetime.fromtimestamp(lnk_time.st_mtime).strftime('%Y-%m-%d %H:%M:%S')  

        if vol_flags[:2] == '10' :
            # Local volume table
            # Random garbage if bit0 is clear in volume flags
        # This is the offset of the local volume table within the 
        # File Info Location Structure
            loc_vol_tab_off_hex = reverse_hex(read_unpack(f,local_vol_off,4))
            loc_vol_tab_off = int(loc_vol_tab_off_hex, 16)

            # This is the asolute start location of the local volume table
            loc_vol_tab_start = loc_vol_tab_off + struct_start

            # This is the length of the local volume table
            local_vol_len_hex = reverse_hex(read_unpack(f,loc_vol_tab_off+struct_start,4))
            local_vol_len = int(local_vol_len_hex, 16)

            # We now have enough info to
            # Calculate the end of the local volume table.
            local_vol_tab_end = loc_vol_tab_start + local_vol_len

            # This is the volume type
            curr_tab_offset = loc_vol_tab_off + struct_start + 4
            vol_type_hex = reverse_hex(read_unpack(f,curr_tab_offset,4))
            vol_type_value = int(vol_type_hex, 16)
            # vol_type_value = int(reverse_hex(read_unpack(f,struct_start + local_vol_off+4,4)),16)
            vol_type_value = vol_type[str(vol_type_value)]
            # output += "Volume Type: "+str(vol_type_hash[vol_type]) + "\n"

            # Volume Serial Number
            curr_tab_offset = loc_vol_tab_off + struct_start + 8
            vol_serial = reverse_hex(read_unpack(f,curr_tab_offset,4))
            # print (str(vol_serial))
            # output += "Volume Serial: "+str(vol_serial) + "\n"

            # Get the location, and length of the volume label 
            vol_label_loc = loc_vol_tab_off + struct_start + 16
            vol_label_len = local_vol_tab_end - vol_label_loc
            vol_label = read_unpack_ascii(f,vol_label_loc,vol_label_len);
            # print(str(vol_label))
            # output += "Vol Label: "+str(vol_label) + "\n"

        local_vol_off = int(reverse_hex(read_unpack(f,local_vol_off,4)),16)
        base_path_off = int(reverse_hex(read_unpack(f,base_path_off,4)),16)

        vol_type_value = int(reverse_hex(read_unpack(f,struct_start + local_vol_off+4,4)),16)
        local_based_path = read_null_term(f,struct_start + base_path_off)

        vol_type_value = vol_type[str(vol_type_value)]
    else:
        vol_type_value = None
        local_based_path = None


    try :
        lnk_info = {"Filename" : filename, "Lnk_Modified_Time" : lnk_modified_time, "Create_Time" : c_time, "Access_Time" : a_time, "Modified_Time" : m_time,
        "Volume Serial" : str(vol_serial), "Volume ID" : vol_type_value, "Local_Based_Path" : local_based_path}
    except :
        lnk_info = {"Filename" : filename, "Create_Time" : c_time, "Access_Time" : a_time, "Modified_Time" : m_time,
        "Volume ID" : vol_type_value, "Local_Based_Path" : local_based_path}
        pass
    # if ink_info["Volume ID"] in "TEMP"
    f.close()

    return lnk_info

    
