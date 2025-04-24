import json
import math
import string
import re
import random
import sys
import traceback
import functools
from collections import OrderedDict
from typing import List

import numpy
import sortedcontainers
from datetime import datetime

def is_alive(upload_timestamp: str, get_timestamp: str, ttl: int) -> bool:
    return (datetime.strptime(get_timestamp, "%Y-%m-%dT%H:%M:%S") - datetime.strptime(upload_timestamp, "%Y-%m-%dT%H:%M:%S")).total_seconds() < ttl

class Folder():
    def __init__(self, folder_name: str, parent: None, children: None = None, folder_path: str | None = None):
        self.parent: Folder | None = parent
        self.children: List[Folder | File] | None = children
        self.folder_name: str = folder_name
        self.folder_path: str = folder_path

class File():
    def __init__(self, file_name: str, size: str, folder: Folder | None = None, timestamp: str = None, ttl: int = None):
        self.folder: Folder | None = folder
        self.file_name: str = file_name
        self.size_str: str = size
        self.size: int = int(size[:-2])
        self.size_unit: str = size[-2:]
        self.timestamp: str = timestamp
        self.ttl: int = ttl if ttl is not None else numpy.inf
class Server(): 
    def __init__(self, files: List[Folder | File] | None = None):
        self.files: List[Folder | File] = files if files is not None else []

class FileManagementSystem():
    def __init__(self, server: Server):
        self.server: Server = server
    
    def file_upload(self, file_name: str, size: str) -> str:
        for file in self.server.files:
            if isinstance(file, File) and file.file_name == file_name:
                raise RuntimeError(f"file {file_name} already exists")
            if isinstance(file, Folder) and file.children:
                for child in file.children:
                    if child.file_name == file_name:
                        raise RuntimeError(f"file {file_name} already exists")
        self.server.files.append(File(file_name, size))
        return f"uploaded {file_name}"
    
    def file_get(self, file_name: str) -> tuple[File, str] | None:
        for file in self.server.files:
            if isinstance(file, File) and file.file_name == file_name:
                return file, f"got {file_name}"
            if isinstance(file, Folder) and file.children:
                for child in file.children:
                    if child.file_name == file_name:
                        return child, f"got {file_name}"
        return None
    
    def file_copy(self, source: str, dest: str) -> str:
        # check if source and dest exsist
        source_file_size = self.file_get(source)[0].size_str
        if source_file_size is None:
            raise RuntimeError(f"file {source} not found")
        dest_file_size = self.file_get(dest)
        if dest_file_size is not None:
            raise RuntimeError(f"file {dest} already exists")
        self.file_upload(file_name=dest, size=source_file_size)
        return f"copied {source} to {dest}"
    
    def file_search(self, prefix: str) -> str:
        found_files = []
        for file in self.server.files:
            if isinstance(file, File) and file.file_name.startswith(prefix):
                found_files.append((file.file_name, file.size))
        found_files.sort(key=lambda x: x[1], reverse=True)
        file_names = [file[0] for file in found_files]
        return f"found [{', '.join(file_names)}]"
    
    def file_upload_at(self, timestamp: str, file_name: str, size: str, ttl: int | None = None) -> str:
        for file in self.server.files:
            if isinstance(file, File) and file.file_name == file_name:
                raise RuntimeError(f"file {file_name} already exists")
            if isinstance(file, Folder) and file.children:
                for child in file.children:
                    if child.file_name == file_name:
                        raise RuntimeError(f"file {file_name} already exists")
        self.server.files.append(File(file_name, size, timestamp=timestamp, ttl=ttl))
        return f"uploaded at {file_name}"

    def file_get_at(self, timestamp: str, file_name: str) -> tuple[File | None, str]:
        for file in self.server.files:
            if isinstance(file, File) and file.file_name == file_name:
                if is_alive(file.timestamp, timestamp, file.ttl):
                    return file, f"got at {file_name}"
                else:
                    return None, "file not found"
            if isinstance(file, Folder) and file.children:
                for child in file.children:
                    if child.file_name == file_name:
                        if is_alive(child.timestamp, timestamp, child.ttl):
                            return child, f"got at {file_name}"
                        else:
                            return None, "file not found"
        return None, "file not found"

    def file_copy_at(self, timestamp: str, source: str, dest: str) -> str:
        # check if source and dest exsist
        source_file = self.file_get_at(timestamp, source)[0]
        if source_file is None:
            raise RuntimeError(f"file {source} not found")
        dest_file = self.file_get_at(timestamp, dest)[0]
        if dest_file is not None:
            raise RuntimeError(f"file {dest} already exists")
        self.file_upload_at(timestamp, dest, source_file.size_str)
        return f"copied at {source} to {dest}"
    
    def file_search_at(self, timestamp: str, prefix: str) -> str:
        found_files = []
        for file in self.server.files:
            if isinstance(file, File) and file.file_name.startswith(prefix):
                if is_alive(file.timestamp, timestamp, file.ttl):
                    found_files.append((file.file_name, file.size))
        found_files.sort(key=lambda x: x[1], reverse=True)
        file_names = [file[0] for file in found_files]
        return f"found at [{', '.join(file_names)}]"
    


def simulate_coding_framework(list_of_lists):
    """
    Simulates a coding framework operation on a list of lists of strings.

    Parameters:
    list_of_lists (List[List[str]]): A list of lists containing strings.
    """

    # create server
    server = Server()

    # create file management system
    file_management_system = FileManagementSystem(server)

    output = []
    for action in list_of_lists:
        if action[0] == "FILE_UPLOAD":
            output.append(file_management_system.file_upload(file_name=action[1], size=action[2]))
        elif action[0] == "FILE_GET":
            output.append(file_management_system.file_get(file_name=action[1])[1])
        elif action[0] == "FILE_COPY":
            output.append(file_management_system.file_copy(source=action[1], dest=action[2]))
        elif action[0] == "FILE_SEARCH":
            output.append(file_management_system.file_search(prefix=action[1]))
        elif action[0] == "FILE_UPLOAD_AT":
            if len(action) == 4:
                output.append(file_management_system.file_upload_at(timestamp=action[1], file_name=action[2], size=action[3]))
            else:
                output.append(file_management_system.file_upload_at(timestamp=action[1], file_name=action[2], size=action[3], ttl=action[4]))
        elif action[0] == "FILE_GET_AT":
            output.append(file_management_system.file_get_at(timestamp=action[1], file_name=action[2])[1])
        elif action[0] == "FILE_COPY_AT":
            output.append(file_management_system.file_copy_at(timestamp=action[1], source=action[2], dest=action[3]))
        elif action[0] == "FILE_SEARCH_AT":
            output.append(file_management_system.file_search_at(timestamp=action[1], prefix=action[2]))
    return output
    

if __name__ == "__main__":
    test_data_1 = [["FILE_UPLOAD", "Cars.txt", "200kb"], 
                              ["FILE_GET", "Cars.txt"], 
                              ["FILE_COPY", "Cars.txt", "Cars2.txt"], 
                              ["FILE_GET", "Cars2.txt"] ]
    test_output_1 = ["uploaded Cars.txt", "got Cars.txt", "copied Cars.txt to Cars2.txt", "got Cars2.txt"]
    test_pass_1 = simulate_coding_framework(test_data_1) == test_output_1
    print(f"Test 1 passed: {test_pass_1}")

    test_data_2 = [["FILE_UPLOAD", "Foo.txt", "100kb"], 
                            ["FILE_UPLOAD", "Bar.csv", "200kb"], 
                            ["FILE_UPLOAD", "Baz.pdf", "300kb"],
                            ["FILE_SEARCH", "Ba"]]
    test_output_2 = ["uploaded Foo.txt", "uploaded Bar.csv", "uploaded Baz.pdf", "found [Baz.pdf, Bar.csv]"]
    test_pass_2 = simulate_coding_framework(test_data_2) == test_output_2
    print(f"Test 2 passed: {test_pass_2}")

    test_data_3 = [
            ["FILE_UPLOAD_AT", "2021-07-01T12:00:00", "Python.txt", "150kb"], 
            ["FILE_UPLOAD_AT", "2021-07-01T12:00:00", "CodeSignal.txt", "150kb", 3600], 
            ["FILE_GET_AT", "2021-07-01T13:00:01", "Python.txt"], 
            ["FILE_COPY_AT", "2021-07-01T12:00:00", "Python.txt", "PythonCopy.txt"], 
            ["FILE_SEARCH_AT", "2021-07-01T12:00:00", "Py"],
            ["FILE_UPLOAD_AT", "2021-07-01T12:00:00", "Expired.txt", "100kb", 1], 
            ["FILE_GET_AT", "2021-07-01T12:00:02", "Expired.txt"], 
            ["FILE_COPY_AT", "2021-07-01T12:00:00", "CodeSignal.txt", "CodeSignalCopy.txt"], 
            ["FILE_SEARCH_AT", "2021-07-01T12:00:00", "Code"]
        ]
    test_output_3 = ["uploaded at Python.txt", "uploaded at CodeSignal.txt", "got at Python.txt", "copied at Python.txt to PythonCopy.txt", "found at [Python.txt, PythonCopy.txt]", "uploaded at Expired.txt", "file not found", "copied at CodeSignal.txt to CodeSignalCopy.txt", "found at [CodeSignal.txt, CodeSignalCopy.txt]"]
    test_pass_3 = simulate_coding_framework(test_data_3) == test_output_3
    print(f"Test 3 passed: {test_pass_3}")