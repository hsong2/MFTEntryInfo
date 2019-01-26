# -*- coding: utf-8 -*-
import sys
import os

def test():
    print ("test module")

# Little Endian으로 되어있는 16진수 값을 10진수로 읽어 값을 반환해주는 함수
def LtoI(buf):
    val = 0
    for i in range(0, len(buf)):
        multi = 1
        for j in range(0, i):
            multi *= 256
        val += buf[i] * multi
    return val

# MFT Entry를 덤프한 후 Fixup 배열을 복구하는 함수
def GetMFTEntry(f, vbr, entry_num, entry_offset):
    root_dir_mft_off = entry_offset + (0x400 * entry_num) #루트 디렉토리의 경우 엔트리 번호가 5번이다. 루트 디렉터리의 오프셋 구함
#    print ("%d" % entry_num)
#    print ("%d" % entry_offset)
#    print ("%x" % root_dir_mft_off)
    f.seek(root_dir_mft_off) #루트 디렉터리의 MFT Entry Offset으로 이동
    mft_buf = bytearray(f.read(0x400)) #기본적으로 할당되는 MFT Entry Size = 1024(0x400)bytes, 그래서 0x400크기만큼 덤프
    return mft_buf

def FixupArrayRecovery(mft_buf):
    mft_fixup_off = LtoI(mft_buf[0x4:0x6]) # 루트 디렉터리 MFT Entry의 fixup 값 offset 획득
    mft_fixup_array_num = LtoI(mft_buf[0x6:0x8]) # fixup 배열의 길이 획득
    mft_fixup_array = mft_buf[mft_fixup_off+2:mft_fixup_off+2+(mft_fixup_array_num * 2)] #fixup 배열 획득 
    k = 0
    for j in range(1, mft_fixup_array_num):
        for i in range(0, 2):
            mft_buf[i+(j*0x200)-2] = mft_fixup_array[k]
            k += 1
    return mft_buf
    
    
# MFT Entry의 $INDEX_ROOT 속성과 $INDEX_ALLOCATION을 덤프하는 함수
def GetAttr(mft_buf, type_id):
    mft_first_attr_off = LtoI(mft_buf[0x14:0x16]) #루트 디렉토리의 MFT Entry의 첫 번째 attribute Offset
    mft_real_size = LtoI(mft_buf[0x18:0x1c]) #루트 디렉토리의 MFT Entry의 실제 Size
    attr_off = mft_buf[mft_first_attr_off:mft_real_size] # 루트 디렉토리의 MFT Entry 속성들만 덤프
    while True:
        attr_type = LtoI(attr_off[0x00:0x04]) #속성 type 읽음 보통 $SI(0x0010)부터 시작
        if attr_type == 0x0000 | attr_type == 0xffff: break
        if attr_type == type_id: #속성이 $INDEX_ROOT라면 수행
            try:
                attr_size = LtoI(attr_off[0x04:0x08])
                attr = attr_off[:attr_size]
                return attr
            except Exception, e:
                print '[-] Error : ', e

        attr_size = LtoI(attr_off[0x04:0x08])
        attr_off = attr_off[attr_size:]

# File Reference Address를 big endian으로 읽고 sequence number와 mft_entry_number를 구하는 함수
def LittleEndianFRA(little):
    big = []
    sequence_num = LtoI(little[6:])
    mft_entry_num = LtoI(little[:6])
    big.append(sequence_num)
    big.append(mft_entry_num)
    return big

def GetIndexAllocEntries(index_record):
    first_index_entry_off = LtoI(index_record[0x18:0x1c])
    total_size_index_entries = LtoI(index_record[0x1c:0x20])
    index_entries_size = 0
    
    all_index_entry = index_record[0x18+first_index_entry_off:]

    index_entries = []
    while True:
        index_entry_length = LtoI(all_index_entry[0x8:0xa])
        index_entries_size += index_entry_length
        index_entry_file_name_length = LtoI(all_index_entry[0xa:0xc])
        index_entry_flag = LtoI(all_index_entry[0xc:0x10])        
        if (index_entry_flag < 0x02):
            index_entries.append(all_index_entry[:index_entry_length])
            all_index_entry = all_index_entry[index_entry_length:]
        else:
            index_entries.append(all_index_entry[:index_entry_length])
            break
    return index_entries

def GetIndexRootEntries(index_root_attr):
    index_root_content_size = LtoI(index_root_attr[0x10:0x14]) # $INDEX_ROOT 속성의 body size
    index_root_content_off = LtoI(index_root_attr[0x14:0x16]) # $INDEX_ROOT 속성의 body 시작 offset
    index_root_attr_body = index_root_attr[index_root_content_off:] # $INDEX_ROOT 속성의 body data
    # $INDEX_ROOT Attribute Header 부분을 추출하여 index_root_attr_header에 저장
    index_root_attr_header = index_root_attr[:index_root_content_off]
    # Index Root Header 부분을 추출하여 index_root_header에 저장
    index_root_header = index_root_attr_body[:0x10]
    # Index Node Header 부분을 추출하여 index_node_header에 저장
    index_node_header = index_root_attr_body[0x10:0x20]
    # Index Entries 부분을 추출하여 index_entries에 저장
    all_index_entry = index_root_attr_body[0x20:]
    # Index Node Header 분석
    first_index_entry_off = LtoI(index_node_header[:0x4])
    
    index_entries = [] 
    while True:
        index_entry_length = LtoI(all_index_entry[0x8:0xa]) # Length of this Index Entry
        index_entry_file_name_length = LtoI(all_index_entry[0xa:0xc]) # Length of $FILE_NAME
        if (index_entry_file_name_length != 0x00):
            index_entries.append(all_index_entry[:index_entry_length])
            all_index_entry = all_index_entry[index_entry_length:]
        else:
            index_entries.append(all_index_entry)
            break
        
    return index_entries

def convertName(filename):
    try:
        filename = filename.decode('utf-8')
        if any('\x00' in s for s in filename):
            filename = filename.replace('\x00', '')
        return filename
    except UnicodeDecodeError:
        filename = filename.decode('utf-16')
        return filename

def findFile_inNode(filename, index_entries, dir_flag):
    result = []
    filename = filename.upper()
    # 해당 index entries를 조사하면서 찾으려는 파일명과 일치하는 index entry가 있는지 조사
    for i in range(0, len(index_entries)):
        index_entry_flags = LtoI(index_entries[i][0xc:0x10])
        if (index_entry_flags < 0x02): # 마지막 인덱스 노드가 아닌 경우
            entry_file_flag = LtoI(index_entries[i][0x48:0x4c])
            '''
            if (dir_flag == 1):
                # 검색하는 filename이 디렉터리이면서 마지막노드가 아닌 경우
                if (entry_file_flag < 0x10000000):
                    # 해당 index entry가 가진 filename 속성이 디렉터리의 정보인 경우
                    continue
            else:
                # 검색하는 filename이 파일이면서 마지막노드가 아닌 경우
                if (entry_file_flag >= 0x10000000):
                    # 해당 index entry가 가진 filename 속성이 파일의 정보인 경우
                    continue
            '''
            entry_file_name_length = LtoI(index_entries[i][0x50:0x51])
            entry_file_name = index_entries[i][0x52:0x52+(entry_file_name_length * 2)]
            file_name = convertName(entry_file_name)
            file_name = file_name.upper()
            
            if (filename == file_name):
                # 일치하는 파일명이 존재
                result.append(1)
                index_entry_fra = LittleEndianFRA(index_entries[i][:0x8])
                result.append(index_entry_fra)
                return result
            elif (filename < file_name):
                # 파일명 비교 결과 찾으려는 파일명이 더 작은 경우 => 해당 index_entry의 자식 노드 탐색
                if (index_entry_flags == 0x01):
                    # 자식 노드가 있는 경우
                    result.append(2)
                    child_node_vcn = index_entries[i][-8:]
                    result.append(child_node_vcn)
                    return result
                else :
                    # 자식 노드가 없는 경우
                    result.append(3)
                    return result
            else:
                pass
                #continue
                
        else:
            if (index_entry_flags == 0x02):
                # 현재 index_entry가 마지막 노드이고 자식 노드가 존재하지 않는다면
                result.append(3)
                return result
            elif (index_entry_flags == 0x03):
                # 현재 index_entry가 마지막 노드이고 자식 노드가 존재한다면
                result.append(2)
                child_node_vcn = index_entries[i][-8:]
                result.append(child_node_vcn)
                return result
            
def getChildIndexNode(index_alloc_attr, child_index_entry_vcn):
    start_vcn = LtoI(index_alloc_attr[0x10:0x18])
    end_vcn = LtoI(index_alloc_attr[0x18:0x20])
    offset_to_runlist = LtoI(index_alloc_attr[0x20:0x22])
    index_alloc_attr_data_runs = index_alloc_attr[offset_to_runlist:]
    runlists = getRunList(index_alloc_attr_data_runs)
    child_vcn = child_index_entry_vcn + 1
    run_off = 0x00
    for i in range(0, len(runlists)):
        if(child_vcn <= runlists[i][0]):
            for runlistNum in range(0, i+1):
                run_off += runlists[runlistNum][1]
            break
        else:
            child_vcn -= runlists[i][0]
    
    index_record_off = (run_off * 0x1000) + ((child_vcn - 1) * 0x1000)
    
    return index_record_off

def getRunList(data_runs):
    runlists = []
    while True:
        if (data_runs[0] == 0x0):
            break
        runlist = []
        offset = data_runs[0x0] / 0x10
        length = data_runs[0x0] % 0x10
        next_run_list = offset + length + 1
        run_length = LtoI(data_runs[0x1:0x1+length])
        run_off = LtoI(data_runs[0x1+length:0x1+offset+length])
        runlist.append(run_length)
        runlist.append(run_off)
        runlists.append(runlist)
        data_runs = data_runs[next_run_list:]
    return runlists
    
def getFileMFTEntry(path, selected): # "C:\\Users\\S0NG2\\Desktop\\과제\\캡스톤디자인\\ntfsdoc.pdf" 의 MFT Entry를 찾는 방법

    split_path = path.split("\\")
    while True:
        if '' in split_path:
            split_path.remove('')
        else:
            break

    volume_device = "\\\\.\\" + split_path[0] #선택한 파일의 볼륨 이름을 volume_device에 저장
    # 1. C: 이름을 가진 볼륨 디바이스의 핸들을 얻는다. -> f
    f=open(volume_device, 'rb') #선택한 파일의 볼륨 디바이스에 접근
    f.seek(0)
    vbr = bytearray(f.read(0x200)) #선택한 파일의 볼륨 디바이스의 VBR 획득

    # 2. f 값을 가지고 루트 디렉토리 메타 데이터 파일의 MFT Entry를 구한다. -> root_dir_mft_entry
    # File reference to base record는 mft_entry의 [0x2c:0x30]
    root_dir_mft_entry = GetMFTEntry(f, vbr, 5, 0x4000)

    base_mft_entry = GetMFTEntry(f, vbr, 0, 0x4000)
    data_attr = GetAttr(base_mft_entry, 0x80)
    offset_to_runlist = LtoI(data_attr[0x20:0x22])
    index_alloc_attr_data_runs = data_attr[offset_to_runlist:]
    runlists = getRunList(index_alloc_attr_data_runs)


    # 3. 얻은 root_dir_mft_entry(MFT Entry)에서 fixup 배열 복구를 해준다.
    mft_entry = FixupArrayRecovery(root_dir_mft_entry)

    # 4. 루트 디렉토리의 mft에서 $INDEX_ROOT 속성을 구한다.
    index_root_attr = GetAttr(mft_entry, 0x90)

    # 4-1. $INDEX_ROOT 속성의 index_entry들만 추출
    index_entries = []
    index_entries = GetIndexRootEntries(index_root_attr)

    dir_flag = 1
    file_path_index = 1
    while True:
        # 5. findFile_inNode 함수로 USERS 이름과 index_entries를 넘겨준다.
        if (len(split_path)-1 == file_path_index):
            if (selected == "File"): dir_flag = 0
            else: dir_flag = 1
        result = findFile_inNode(split_path[file_path_index], index_entries, dir_flag)
        if(result == None):
            return "No result"
        else:
            if (result[0] == 1):
                runlist_offset = 0
                entry_range = []
                entry_range.append(0)
                start_range = 0x0
                end_range = 0x0
                # 일치하는 파일명 존재
                file_path_index += 1
                index_entry_num = result[1][1]
                for i in range(0, len(runlists)):
                    mft_entry_num = (runlists[i][0] * 0x1000) / 0x400
                    entry_range.append(mft_entry_num)
                
                for j in range(0, len(runlists)):
                    runlist_offset += runlists[j][1] * 0x1000
                    start_range += entry_range[j]
                    end_range += entry_range[j+1]
                    if (index_entry_num >= start_range and index_entry_num <= end_range-1):
                        index_entry_num -= start_range
                        break
                    else:
                        continue        
                mft_entry = GetMFTEntry(f, vbr, index_entry_num, runlist_offset)
                mft_entry = FixupArrayRecovery(mft_entry)
                if (len(split_path) == file_path_index):
                    break
                index_root_attr = GetAttr(mft_entry, 0x90)
                index_entries = GetIndexRootEntries(index_root_attr)
            elif (result[0] == 2):
                # 일치하는 파일명은 없지만 자식노드가 존재
                index_alloc_attr = GetAttr(mft_entry, 0xa0)
                child_index_entry_vcn = LtoI(result[1])
                ##수정
                index_record_off = getChildIndexNode(index_alloc_attr, child_index_entry_vcn)
                ##수정
                f.seek(index_record_off)
                index_record = bytearray(f.read(0x1000))
                index_record = FixupArrayRecovery(index_record)
                index_entries = GetIndexAllocEntries(index_record)
            else:
                # 일치하는 파일명도 없고 이동해야 하는 자식노드가 존재하지 않음
                break

    return mft_entry
