#!/usr/bin/env python
# Copyright 2020 Created By Jialong Zhang. All Rights Reserved.
# Creation date: 03/08/2020
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import math


class CustomFileIO:
    '''
    Custom File IO utility class for basic folder, file opetions.
    The class contains functions:
        is_empty_file(path) -> check if file is empty
        file_format(path) -> get file format(window, unix, macintosh)
        print_empty_files(folder) -> print files with details(True,False)
        print_files(folder) -> print all files in a folder
        file_size(path) -> get file size(byte)
        file_size_convert(size) -> convert file size to KB,MB..
        file_extension(path) -> get file extension
    '''

    def __init__(
        self, folder_path=None, filename=None, filepath=None,
        carriage_return=None, **kwargs
    ):
        self._folder_path = folder_path
        self._carriage_return = carriage_return
        self._filename = filename
        self._filepath = filepath
        for key, value in kwargs:
            self.key = value

    def file_info_setup(self, path):
        '''
        This method is required to update the class details,
        or simply avoid using class instances (self.)
        usage: input(file path)
        '''
        self._folder_path = os.path.dirname(path)
        self._filename = os.path.basename(path)
        self._filepath = path

    def file_format(self, path):
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
        self.file_info_setup(path)
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
        self._carriage_return = max(carriage_dict, key=carriage_dict.get)
        self._carriage_detail = carriage_dict
        return self._carriage_return

    def is_empty_file(self, path):
        '''
        Return True if the file is empty, otherwise return False
        '''
        self.file_info_setup(path)
        with open(path, 'rb') as f:
            return f.readlines() == []

    def print_empty_files(self, folder):
        '''
        Print out all the files details in the folder
        usage: input(folder path)
        True -> file is empty
        False -> file is not empty
        '''
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            if file.endswith('.txt') and os.path.isfile(file_path):
                is_empty = self.is_empty_file(file_path)
                print('file: {} -> {}'.format(file, is_empty))

    def print_files(self, folder):
        '''
        Print out all the files in a folder
        usage: input(folder path)
        '''
        for file in os.listdir(folder):
            print(file)

    def file_size(self, path):
        '''
        Get file size for a file.
        usage: input(file path)
        '''
        size = os.stat(path).st_size
        return size

    def file_size_convert(self, size):
        '''
        Convert file size, from Byte to KB, MB, GB, TB
        usage(size)
        '''
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

    def file_extension(self, path):
        '''
        get file extension .txt, .csv...
        usage(path)
        '''
        file, file_extension = os.path.splitext(path)
        return file_extension
