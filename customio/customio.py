#!/usr/bin/env python
# MIT License
# Copyright (c) 2020 Jialong Zhang

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
# functions:
#    is_empty_file(path) -> check if file is empty
#    file_format(path) -> get file format(window, unix, macintosh)
#    print_empty_files(folder) -> print files with details(True,False)
#    print_files(folder) -> print all files in a folder
#    file_size(path) -> get file size(byte)
#    file_size_convert(size) -> convert file size to KB,MB..
#    file_extension(path) -> get file extension
# ===========================================================


import os
import math


def file_format(path):
    '''
    Return corresponding file format for a file
    (loop through all the lines, get maximum matched dictionary key)
    usage: input(file path)
    Format Usage with double equal  in control flow ==
    'Window(LF|CR)'  -> for Window MS(dos)
    'Unix/MacOS(LF)' -> for Linux, MacOS
    'Macintosh(CR)' -> for Older version of MacOS
    'Unknown' -> Undefined format
    '''
    with open(path, 'rb') as f:
        # lines = f.readlines() # type: list
        carriage_dict = {
            'Unknown': 0, 'Window(LF|CR)': 0,
            'Unix/MacOS(LF)': 0, 'Macintosh(CR)': 0
            }
        for index, line in enumerate(f, 1):
            if b'\r\n' in line:
                carriage_dict['Window(LF|CR)'] += 1
            elif b'\n' in line:
                carriage_dict['Unix/MacOS(LF)'] += 1
            elif b'\r' in line:
                carriage_dict['Macintosh(CR)'] += 1
            else:
                carriage_dict['Unknown'] += 1
        return max(carriage_dict, key=carriage_dict.get)


def is_empty_file(path):
    '''
    Return True if the file is empty, otherwise return False
    '''
    with open(path, 'rb') as f:
        return f.readlines() == []


def print_empty_files(folder):
    '''
    Print out all the files details in the folder
    usage: input(folder path)
    True -> file is empty
    False -> file is not empty
    '''
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        if file.endswith('.txt') and os.path.isfile(file_path):
            is_empty = is_empty_file(file_path)
            print('file: {} -> {}'.format(file, is_empty))


def print_files(folder):
    '''
    Print out all the files in a folder
    usage: input(folder path)
    '''
    for file in os.listdir(folder):
        print(file)


def file_size(path):
    '''
    Get file size for a file.
    Convert file size, from Byte to KB, MB, GB, TB
    usage(size)
    '''
    size = os.stat(path).st_size
    kb = 1024
    mb = pow(1024, 2)
    gb = pow(1024, 3)
    tb = pow(1024, 4)
    size_result = ''
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


def file_extension(path):
    '''
    get file extension .txt, .csv..
    usage(path)
    '''
    file, file_extension = os.path.splitext(path)
    return file_extension
