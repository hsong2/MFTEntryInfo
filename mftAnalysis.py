# -*- coding: utf-8 -*-
import sys
from datetime import datetime, timedelta
from getMFTEntry import convertName

def ChangeTime(binary_time):
    binary_us = int(binary_time, 16) / 10.
    binary_time_utc = datetime(1601, 1, 1) + timedelta(microseconds=binary_us)
    binary_time_utc = binary_time_utc + timedelta(hours=9)
    binary_time_utc = binary_time_utc.ctime()
    binary_time_utc += ' +0900'
    return binary_time_utc

def flagAnalyz(flags, attr_type):
    file_name_attr_dic = {1:'Directory', 2:'Index View'}
    forth_dic = {1:'Read Only', 2:'Hidden', 4:'System'}
    third_dic = {2:'Archive', 4:'Device', 8:'Normal'}
    second_dic = {1:'Temporary', 2:'Sparse file', 4:'Reparse Point', 8:'Compressed'}
    first_dic = {1:'Offline', 2:'Not indexed', 4:'Encrypted'}

    result = []
    fName_flag = 0x0
    if(attr_type == 0x30):
        fName_flag = flags / 0x10000000
        flags = flags % 0x10000000

    first_byte_flag = flags / 0x1000
    next_byte = flags % 0x1000
    second_byte_flag = next_byte / 0x100
    next_byte = next_byte % 0x100
    third_byte_flag = next_byte / 0x10
    forth_byte_flag = next_byte % 0x10

    if (attr_type == 0x30):
        keys = file_name_attr_dic.keys()
        keys.sort()
        for i in range(0, len(keys)):
            if (fName_flag >= keys[len(keys)-1-i]):
                fName_flag -= keys[len(keys)-1-i]
                result.append(file_name_attr_dic[keys[len(keys)-1-i]])

    keys = forth_dic.keys()
    keys.sort()
    for i in range(0, len(keys)):
        if (forth_byte_flag >= keys[len(keys)-1-i]):
            forth_byte_flag -= keys[len(keys)-1-i]
            result.append(forth_dic[keys[len(keys)-1-i]])

    keys = third_dic.keys()
    keys.sort()
    for i in range(0, len(keys)):
        if (third_byte_flag >= keys[len(keys)-1-i]):
            third_byte_flag -= keys[len(keys)-1-i]
            result.append(third_dic[keys[len(keys)-1-i]])

    keys = second_dic.keys()
    keys.sort()
    for i in range(0, len(keys)):
        if (second_byte_flag >= keys[len(keys)-1-i]):
            second_byte_flag -= keys[len(keys)-1-i]
            result.append(second_dic[keys[len(keys)-1-i]])

    keys = first_dic.keys()
    keys.sort()
    for i in range(0, len(keys)):
        if (first_byte_flag >= keys[len(keys)-1-i]):
            first_byte_flag -= keys[len(keys)-1-i]
            result.append(first_dic[keys[len(keys)-1-i]])
         
    return result

def LtoI(buf):
    val = 0
    for i in range(0, len(buf)):
        multi = 1
        for j in range(0, i):
            multi *= 256
        val += buf[i] * multi
    return val

def StandardInfo_parse(attr_off):
    result_str = ""
    create_time = ''
    modified_time = ''
    mft_modified_time = ''
    last_accessed_time = ''
    
    attr_type = LtoI(attr_off[0x00:0x04]) #0x10을 저장
    attr_size = LtoI(attr_off[0x04:0x08]) #속성의 길이
    si_off = attr_off[:attr_size] #$SI header+body
    #content_size = LtoI(attr_off[0x10:0x14]) #$SI의 body size
    content_off = LtoI(attr_off[0x14:0x16]) #$SI body offset
    #si_head_off = si_off[:content_off] #SI header
    si_body_off = si_off[content_off:] #$SI body
    create = si_body_off[0x00:0x08]
    modified = si_body_off[0x08:0x10]
    mft_modified = si_body_off[0x10:0x18]
    last_accessed = si_body_off[0x18:0x20]

    flags = LtoI(si_body_off[0x20:0x24])
    flag_result = flagAnalyz(flags, attr_type)
    #maximum_number_of_version = si_body_off[0x24-0x28]
    #version_number = si_body_off[0x28-0x2C]
    #class_id = si_body_off[0x2C-0x30]
    #owner_id = si_body_off[0x30-0x34]
    #security_id = si_body_off[0x34-0x38]
    #quota_charged = si_body_off[0x38-0x40]
    #update_sequence_number = si_body_off[0x40-0x48]

    for i in range(0, 8):
        create_time += '%02x' % create[7-i]
        modified_time += '%02x' % modified[7-i]
        mft_modified_time += '%02x' % mft_modified[7-i]
        last_accessed_time += '%02x' % last_accessed[7-i]
    
    create_time_utc = ChangeTime(create_time)
    modified_time_utc = ChangeTime(modified_time)
    mft_modified_time_utc = ChangeTime(mft_modified_time)
    last_accessed_time_utc = ChangeTime(last_accessed_time)

    result_str += ''
    result_str += '---------------[ $STANDART_INFORMATION ]---------------\n'
    #print '[+]Attribute type: 0x%x(%d)' % (attr_type, attr_type)
    #print '[+]Attribute size: 0x%04x(%dbytes)' % (attr_size, attr_size)
    result_str += '[+]Create time: %s\n' % create_time_utc
    result_str += '[+]Modified time: %s\n' % modified_time_utc
    result_str += '[+]MFT Modified time: %s\n' % mft_modified_time_utc
    result_str += '[+]Last Accessed time: %s\n' % last_accessed_time_utc
    result_str += '[+]File Attribute: ' + str(flag_result) + "\n"

    return result_str

def FileName_parse(attr_off):
    result_str = ""
    create_time = ''
    modified_time = ''
    mft_modified_time = ''
    last_accessed_time = ''
    flags_name = ''
    
    attr_type = LtoI(attr_off[0x00:0x04]) #0x10을 저장
    attr_size = LtoI(attr_off[0x04:0x08]) #속성의 길이

    fn_off = attr_off[0x00:attr_size] #$FN header+body

    content_size = LtoI(attr_off[0x10:0x14]) #$FN의 body size
    content_off = LtoI(attr_off[0x14:0x16]) #$FN body offset

    fn_head_off = fn_off[0x00:content_off] #FN header
    fn_body_off = fn_off[content_off:attr_size] #$FN body

    create = fn_body_off[0x08:0x10]
    
    modified = fn_body_off[0x10:0x18]
    mft_modified = fn_body_off[0x18:0x20]

    last_accessed = fn_body_off[0x20:0x28]
    allocated_size_file = fn_body_off[0x28:0x30]

    real_size_file = fn_body_off[0x30:0x38]
    flags = LtoI(fn_body_off[0x38:0x3c])
    flag_result = flagAnalyz(flags, attr_type)
    reparse_value = fn_body_off[0x3c:0x40]
    
    len_name = fn_body_off[0x40:0x41]
    name_space = fn_body_off[0x41:0x42]
    file_name = fn_body_off[0x42:]
    file_name = convertName(file_name)
    
        
    for i in range(0, 8):
        create_time += '%02x' % create[7-i]
        modified_time += '%02x' % modified[7-i]
        mft_modified_time += '%02x' % mft_modified[7-i]
        last_accessed_time += '%02x' % last_accessed[7-i]

    create_time_utc = ChangeTime(create_time)
    modified_time_utc = ChangeTime(modified_time)
    mft_modified_time_utc = ChangeTime(mft_modified_time)
    last_accessed_time_utc = ChangeTime(last_accessed_time)

    result_str += ''
    result_str += '---------------[ $File_Name ]---------------\n'
    #print '[+]Attribute type: 0x%x(%d)' % (attr_type, attr_type)
    #print '[+]Attribute size: 0x%04x(%dbytes)' % (attr_size, attr_size)
    result_str += '[+]Create time: %s\n' % create_time_utc
    result_str += '[+]Modified time: %s\n' % modified_time_utc
    result_str += '[+]MFT Modified time: %s\n' % mft_modified_time_utc
    result_str += '[+]Last Accessed time: %s\n' % last_accessed_time_utc
    #print '[+]Allocated size of file: %d' % LtoI(allocated_size_file) 
    #print '[+]Real size of file: %d' % LtoI(real_size_file)
    #print '[+]Flags: 0x%04x(%s)' % (flags, flags_name)
    #print '[+]Reparse value: %s' % LtoI(reparse_value)
    #print '[+]Length of name: %s' % LtoI(len_name)
    #print '[+]Name space: %s' % LtoI(name_space)
    result_str += '[+]File name : %s\n' % file_name
    result_str += '[+]File Attribute: ' + str(flag_result) + "\n"

    return result_str

  
def analysisMFTEntry(mft_buf):
    result_str = ""
    mft_number = LtoI(mft_buf[0x2C:0x30])
    mft_attribute_off = LtoI(mft_buf[0x14:0x16]) #Offset to File attribute
    mft_size = LtoI(mft_buf[0x18:0x1c]) #Real size of MFT Entry
    attr_off = mft_buf[mft_attribute_off:mft_size] #첫 속성이 시작하는 위치부터 Entry 끝 까지
    mft_flags = LtoI(mft_buf[0x16:0x18])
    mft_flags_str = ""
    if (mft_flags == 0x00):
        mft_flags_str = "Deleted file"
    elif (mft_flags == 0x01):
        mft_flags_str = "File"
    elif (mft_flags == 0x02):
        mft_flags_str = "Deleted directory"
    elif (mft_flags == 0x03):
        mft_flags_str = "Directory"
    else:
        mft_flags_str = "Not analyzed"
        
    result_str += '[+] MFT Entry attribute: %s\n' % mft_flags_str
    result_str += '[+] MFT Entry number: %d\n' % mft_number
    result_str += '[+] Used size of MFT Entry: %d bytes\n' % mft_size

    while True:
        attr_type = LtoI(attr_off[0x00:0x04]) #속성 type 읽음 보통 $SI(0x10)부터 시작
        if ((attr_type == 0x00) or (attr_type == 0xffffffff)): break
        elif (attr_type == 0x10): #속성이 $SI이라면 수행
            try:
                result_str += StandardInfo_parse(attr_off)
            except Exception, e:
                print '[-] Error : ', e
        elif (attr_type == 0x30):
            try:
                result_str += FileName_parse(attr_off)
            except Exception, e:
                print '[-] Error : ', e            

        attr_size = LtoI(attr_off[0x04:0x08])
        attr_off = attr_off[attr_size:]

    return result_str
