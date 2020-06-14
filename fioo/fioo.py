#!/usr/bin/env python
# MIT License
# Copyright (c) 2020 Jialong Zhang
# d2hhdCBpdCB0YWtlIHRvIGJlIHN1Y2Nlc3NmdWwgaW4gbGlmZT8=
# c3RhcnQgd2l0aCBzbWFsbCBnb2Fs
# cHV0IG15IGZpcnN0IGdvYWwgaGVyZQ==
# a2VlcCBkZXZlbG9waW5nIG15IHBlcnNvbmFsIHB5dGhvbiBtb2R1bGUgZXZlbiBpZiBvbmx5IG15c2VsZiBpcyB1c2luZyBpdC4=

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# ===========================================================
# Custom File IO utility package for basic folder, file opetions.
# FIOO class usage:
# f = fioo.FIOO()
#
# functions:
#    is_empty_file(path) -> check if file is empty
#    format(path) -> get file format(window, unix, macintosh)
#    print_empty_files(folder) -> print files with details(True,False)
#    print_files(folder) -> print all files in a folder
#    size(path) -> get file size(byte)
#    ext(path) -> get file extension
#    compare(folder1, folder2) -> generate diff file in the folder2 location
#    deli(path) -> get file delimter, useful for csv file
# ===========================================================

# ====================update info============================
# 4/26/2020:
# FIOO class, methods rework, more condition check
# 5/20/2020:
# fioobase64 v1
# 6/03/2020:
# compare function
# fioo_v0.3 release
# 6/07/2020:
# docstring format(make it easier to read in visual studio)
# add deli function
# 6/13/2020:
# improve the compare function, display warning message for file not find in first folder,
# now the diff file generated csv file instead of txt, logic fixed for the compare function
# note: when compare, does not skip columns - will implement in the future update
# fioo_v0.4 release
# ===========================================================


import os
import math


# helper methods:
def _isdir(path):
    '''
    helper method within the file
    return True is the path is dir, otherwize False
    '''
    return os.path.isdir(path)

def _is_empty_file(path):
    '''
    Return True if the file is empty, otherwise return False
    '''
    if not _isdir(path):
        with open(path, 'rb') as f:
            return f.readlines() == []

# decorator, run function once only
def __run_once(m):
    def fun(*args, **kwargs):
        if not fun.has_run:
            fun.has_run = True
            return m(*args, **kwargs)
    fun.has_run = False
    return fun

# end helper methods


# ========================FIOO Class========================
class FIOO():
    def __init__(self, path='path undefine', *args, **kwargs):
        self.path = 'path undefine'
        self.__dict__.update(kwargs)

    def __str__(self):
        if self.path == 'path undefine':
            return '{} -> hint: set_file_path(path) to set file path'.format(self.path)
        else:
            return self.path

    def set_file_path(self, path):
        self.path = path

    def set_folder_path(self, folder):
        self.folder = folder

    @property
    def fformat(self):
        return fformat(self.path)

    @property
    def size(self):
        return size(self.path)

    @property
    def print_empty_files(self):
        return print_empty_files(self.path)

    @property
    def print_files(self):
        return print_files(self.path)

    @property
    def ext(self):
        return ext(self.path)

    @property
    def file_check(self):
        return file_check(self.path)

    def file_check(self, **kwargs):
        return file_check(self.path, **kwargs)

    @property
    def deli(self):
        return deli(self.path)
    
    def compare(self,path1, path2):
        compare(path1, path2)
    
# ========================END FIOO Class========================

# fformat method
def fformat(path, max_chunk=300000, check_all=False):
    '''
    Return corresponding file format for a file\n
    (loop through all the lines, get maximum matched dictionary key)\n
    Usage: fformat(file path)\n
    Keyword arguments:\n
    max_chunk -- size for read lines in the file\n
    check_all -- check entire file\n
    Return str:\n
    'Window'  -> (LF|CR) for Window MS(dos)\n
    'Linux' -> (LF) for Linux, MacOS\n
    'Macintosh' -> (CR) for Older version of MacOS\n
    'Unknown' -> Undefined format
    '''
    if _isdir(path):
        return 'detect folder path instead of file path'
    if _is_empty_file(path):
        return 'detect empty file'
    with open(path, 'rb') as f:
        chunk = f.readlines(max_chunk)
        carriage_dict = {
            'Unknown': 0, 'Window': 0,
            'Linux': 0, 'Macintosh': 0
            }
        for line in chunk:
            if b'\r\n' in line:
                carriage_dict['Window'] += 1
            elif b'\n' in line:
                carriage_dict['Linux'] += 1
            elif b'\r' in line:
                carriage_dict['Macintosh'] += 1
            else:
                carriage_dict['Unknown'] += 1
        result = max(carriage_dict, key=carriage_dict.get)
        if check_all:
            sum = 0
            for i in carriage_dict:
                sum += carriage_dict[i]
            if sum != carriage_dict[result]:
                result = 'Unknown' 
        return result

def size(path):
    '''
    Get file size for a file or folder(also the sub diretory).\n
    Convert file size, from Byte to KB, MB, GB, TB(whole number)\n
    Usage: size(folderpath) or size(filepath)\n
    Return str:\n
    1KB, 1MB, 1GB
    '''
    size = os.stat(path).st_size
    kb = 1024
    mb = pow(1024, 2)
    gb = pow(1024, 3)
    tb = pow(1024, 4)
    size_result = ''
    if _isdir(path):
        total = 0
        for folder, dirnames, files in os.walk(path):
            for file in files:
                filepath = os.path.join(folder, file)
                if not os.path.islink(filepath):
                    total += os.path.getsize(filepath)
        size = total
    if size < 1024:
        return '{}B'.format(size)
    if size >= tb:
        size_result = math.ceil(size / tb)
        return '{}TB'.format(size_result)
    elif size >= gb:
        size_result = math.ceil(size / gb)
        return '{}GB'.format(size_result)
    elif size >= mb:
        size_result = math.ceil(size / mb)
        return '{}MB'.format(size_result)
    else:
        size_result = math.ceil(size / kb)
        return '{}KB'.format(size_result)
    return size_result

def ext(path, dot=False):
    '''
    get file extension .txt, .csv...\n
    Keyword arguments:\n
    dot -- if this is true, will output dot in front of the extension\n
    Usage: file_(path)\n
    Return str:\n
    .txt or txt
    '''
    if _isdir(path):
        return 'detect folder path instead of file path'
    if not os.path.exists(path):
        raise FileNotFoundError
    file, file_extension = os.path.splitext(path)
    if dot:
        return file_extension
    else:
        return file_extension.strip('.')

def file_check(path, f_line=True, l_line=True, all_lines=False, contain='', __valid=True, __print=True):
    '''
    check if the file contain spaces at the begining, at the end, or in between.\n
    Usage:\n
    file_sapce(path)\n
    Keyword arguments:\n
    f_line -- first line check, set to False if ignore\n
    l_line -- last line check, set to False if ignore\n
    all_lines -- will check spaces for entire file, default: False\n
    __print -- print all blank lines in the file, default: True\n
    Return str:\n
    'first line is blank'\n
    '!file is good, no blank lines for all lines'\n
    ...
    '''
    if _isdir(path):
        return 'detect folder path instead of file path'
    if _is_empty_file(path):
        return 'detect empty file'
    with open(path, 'rb') as f:
        data = list(f)
        first_line = data[0]
        last_line = data[-1]
        message = ""
        if all_lines:
            for lineno, line in enumerate(data, 1):
                if line == b'\r\n':
                    ___valid = False
                    if __print:
                        print('[line{}] -> blank line'.format(lineno))
        if not f_line and not l_line:
            message = 'nothing to check, both first and last line condition is false'
        elif all_lines and __valid:
            message = 'detect blank lines with the file'
        elif f_line and l_line and first_line == b'\r\n' and last_line == b'\r\n':
            message = 'first and last line are both blank line'
        elif f_line and l_line and first_line == b'\r\n' and last_line != b'\r\n':
            message = 'first line is blank'
        elif f_line and l_line and first_line != b'\r\n' and last_line == b'\r\n':
            message = 'last line is blank'
        elif f_line and not l_line and first_line == b'\r\n' and last_line == b'\r\n':
            message = 'first line is blank'
        elif not f_line and l_line and first_line == b'\r\n' and last_line == b'\r\n':
            message = 'last line is blank'
        elif not all_lines and f_line and l_line and first_line != b'\r\n' and last_line != b'\r\n':
            message = 'file is good, no blank lines'
        elif all_lines and __valid and f_line and l_line and first_line != b'\r\n' and last_line != b'\r\n':
            message = '!file is good, no blank lines for all lines'
        else:
            message = 'unhandle condition'
        print(message)
        return message
def print_empty_files(path):
    '''
    Print out all the files details in the folder\n
    Usage: input(folder path)
    '''
    if not _isdir(path):
        print('detect file path instead of folder path')
        return
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if file.endswith('.txt') and os.path.isfile(file_path):
            is_empty = _is_empty_file(file_path)
            print('file: {} -> {}'.format(file, is_empty))

def print_files(path):
    '''
    print out all the files in a folder\n
    Usage: input(folderpath)
    '''
    if not _isdir(path):
        return 'detect file path instead of folder path'
    for file in os.listdir(path):
        print(file)
        
def deli(path):
    '''
    determine delimeter for a file by using csv module\n
    method will not able to detemrine if file contains more than 1 delimeter\n
    read 1024 byte from the file\n
    Return str:\n
    ',' or '|' or ';' or '|' or '{}' or '/\'
    '''
    sniff_size = 1024
    if _isdir(path):
        return 'detect folder path instead of file path'
    with open(path, 'rt') as f:
        sn = csv.Sniffer()
        try:
            sniff = sn.sniff(f.read(sniff_size))
            if sniff.delimiter == ' ':
                return 'space'
            else:
                return sniff.delimiter
        except Exception as e:
            print('{}, more than 1 delimter found in the file'.format(e))
       

# file compare seciton:

# def __sort_any_file_with_keys(file, sortkeys=[]):
#     with open(r'{}'.format(file)) as f:
#         lines = f.read().splitlines()[1:]

#         sorted_lines = sorted(lines, key= lambda k: k[0])
#         print(b)
#         print(sorted_lines)



def _gen_diff_file(filename1, filename2, folder1, folder2):
    with open(
        r'{}\{}'.format(folder1, filename1), 'rt', newline='') as f, open(
        r'{}\{}'.format(folder2, filename2), 'rt', newline=''
        ) as f2:
        mismatch_count = 0
        # lines1 = f.readlines() # realines is list, but contain \n
        # lines2 = f2.readlines() # should avoid using realines
        # sorted both files the same way
        f1_header = next(f)
        f2_header = next(f2)
        lines1 = sorted(f.read().replace(" ",'').splitlines())
        lines2 = sorted(f2.read().replace(" ",'').splitlines())
        #print(lines1)
        #print(lines2)

        lines2_moredata = [d for d in lines2 if d not in lines1]
        lines1_moredata = [d for d in lines1 if d not in lines2]
        print('compare base:{} with actual: {}'.format(filename1, filename2))
    f_ext = ext(r'{}\{}'.format(folder2, filename1),dot=True) # .txt
    base_file_name = os.path.basename(os.path.join(folder2, filename1)).rstrip(f_ext)

    with open('{}\diff_{}.csv'.format(folder2, base_file_name), 'wt', newline='') as wf:
        filter_matched = sorted(list(set(lines1) - set(lines2)))
        wf.write('{}'.format(f2_header))
        for lineno, line2 in enumerate(lines2_moredata, 1):
                try:
                    if line2 not in lines1:
                        mismatch_count += 1
                        wf.write(
                            'base:   {} \nactual: {}\n \n'
                            .format(
                                filter_matched[lineno-1],
                                line2
                                )
                            )
                except IndexError as e:
                    pass

        if len(lines1) != len(lines2):
            for line1 in lines1_moredata:
                    wf.write(
                        'missing -> {}\n'
                        .format(line1))
        if len(lines1) != len(lines2):
            for line2 in lines2_moredata:
                if line2 not in lines1:
                    wf.write(
                        'additional: -> {}\n'
                        .format(line2))
        if len(lines1) == len(lines2):
            wf.write(
                'final <-> records count are matched!!\n'
                )    
        if len(lines1) == len(lines2) and mismatch_count == 0:
            wf.write(
                'final <-> !! All records are perfectly matched!!\n'
                )


def _missing_file_message(file2):
    info_message = 'warning!! unable to find {} not in first folder'.format(file2)
    print(info_message)

def compare(folder1, folder2):
    '''
    compare files in folder1 with folder2, the files name should be the same.\n
    result will be generated to folder2 path\n
    folder1: path, folder2: path\n
    Usage:compare(folder1path, folder2path)
    '''
    for file1 in os.listdir(folder1):
        for file2 in os.listdir(folder2):
            info_message = ""
            try:
                if file1 == file2:
                    _gen_diff_file(file1, file2, folder1, folder2)
                elif not file2.startswith('diff_') and file2 not in os.listdir(folder1):
                    _missing_file_message(file2)
            except IndexError as e:
                print('{} -> {}'.format(e, file2))
