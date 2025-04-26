import json
import math
import string
import re
import random
import sys
import traceback
import functools
from collections import OrderedDict

import numpy
import sortedcontainers
from datetime import datetime

def is_alive(upload_timestamp, current_timestamp, ttl):
    if not upload_timestamp:
        return True
    return ((datetime.strptime(current_timestamp, "%Y-%m-%dT%H:%M:%S") - datetime.strptime(upload_timestamp, "%Y-%m-%dT%H:%M:%S")).total_seconds() < ttl)

class File():
    def __init__(self, file_name: str, size: str, upload_time: str | None = None, ttl: int | None = None):
        self.file_name = file_name
        self.size = size
        self.size_num = int(size[:-2])
        self.upload_time = upload_time 
        self.ttl = ttl if ttl else numpy.inf

class FileManagementSystem():
    def __init__(self, files: list[File] | None = None):
        self.files = files if files else []

    def file_upload(self, file_name: str, size: str):
        for file in self.files:
            if file.file_name == file_name:
                raise Exception(f"{file_name} already exists")
        self.files.append(File(file_name, size))
        return f"uploaded {file_name}"
    
    def file_get(self, file_name: str):
        for file in self.files:
            if file.file_name == file_name:
                return file, f"got {file_name}"
        return None
    
    def overwrite_file(self, file_name, size, timestamp = None, ttl = None):
        for idx, file in enumerate(self.files):
            if file.file_name == file_name:
                self.files[idx] = File(file_name, size, timestamp, ttl)
        return f"overwrote {file_name}"
    
    def file_copy(self, source: str, dest: str):
        source_file = self.file_get(source)[0]
        if not source_file:
            raise Exception(f"{source} does not exist")
        dest_file = self.file_get(dest)
        if dest_file:
            self.overwrite_file(source, source_file.size)
        self.file_upload(dest, source_file.size)
        return f"copied {source} to {dest}"
    
    def file_search(self, prefix: str):
        results = []
        for file in self.files:
            if file.file_name.startswith(prefix):
                results.append((file.file_name, file.size_num))
        results.sort(key=lambda x: x[1], reverse=True)
        str_results = ', '.join([result[0] for result in results[:10]])
        return f"found [{str_results}]"
    
    def file_upload_at(self, timestamp, file_name, size, ttl = None):
        for file in self.files:
            if file.file_name == file_name:
                raise Exception(f"{file_name} already exists")
        self.files.append(File(file_name, size, timestamp, ttl))
        return f"uploaded at {file_name}"

    def file_get_at(self, timestamp, file_name):
        for file in self.files:
            if file.file_name == file_name and is_alive(file.upload_time, timestamp, file.ttl):
                return file, f"got at {file_name}"
        return None, "file not found"
    
    def file_copy_at(self, timestamp, source, dest):
        source_file = self.file_get_at(timestamp, source)[0]
        if not source_file:
            raise Exception(f"{source} does not exist")
        dest_file = self.file_get(dest)
        if dest_file:
            self.overwrite_file(source, source_file.size, timestamp, source_file.ttl)
        self.file_upload_at(file_name=dest, size=source_file.size, timestamp=timestamp, ttl=source_file.ttl)
        return f"copied at {source} to {dest}"
    
    def file_search_at(self, timestamp, prefix):
        results = []
        for file in self.files:
            if file.file_name.startswith(prefix) and is_alive(file.upload_time, timestamp, file.ttl):
                results.append((file.file_name, file.size_num))
        results.sort(key=lambda x: x[1], reverse=True)
        str_results = ', '.join([result[0] for result in results[:10]])
        print(str_results)
        return f"found at [{str_results}]"
    
    def rollback(self, timestamp):
        for idx, file in enumerate(self.files):
            # check if file was uploaded yet
            if is_alive(file.upload_time, timestamp, 0):
                self.files.pop(idx)
        return f"rollback to {timestamp}"
            


def simulate_coding_framework(list_of_lists):
    """
    Simulates a coding framework operation on a list of lists of strings.

    Parameters:
    list_of_lists (List[List[str]]): A list of lists containing strings.
    """
    file_management_system = FileManagementSystem()

    outputs = []
    for action in list_of_lists:
        if action[0] == "FILE_UPLOAD":
            outputs.append(file_management_system.file_upload(file_name=action[1], size=action[2]))
        if action[0] == "FILE_GET":
            outputs.append(file_management_system.file_get(file_name=action[1])[1])
        if action[0] == "FILE_COPY":
            outputs.append(file_management_system.file_copy(source=action[1], dest=action[2]))
        if action[0] == "FILE_SEARCH":
            outputs.append(file_management_system.file_search(prefix=action[1]))
        if action[0] == "FILE_UPLOAD_AT":
            if len(action) == 4:
                action.append(None)
            outputs.append(file_management_system.file_upload_at(file_name=action[2], size=action[3], timestamp=action[1], ttl=action[4]))
        if action[0] == "FILE_GET_AT":
            outputs.append(file_management_system.file_get_at(timestamp=action[1], file_name=action[2])[1])
        if action[0] == "FILE_COPY_AT":
            outputs.append(file_management_system.file_copy_at(timestamp=action[1], source=action[2], dest=action[3]))
        if action[0] == "FILE_SEARCH_AT":
            print(file_management_system.file_search_at(timestamp=action[1], prefix=action[2]))
            outputs.append(file_management_system.file_search_at(timestamp=action[1], prefix=action[2]))
        if action[0] == "ROLLBACK":
            outputs.append(file_management_system.rollback(timestamp=action[1]))
        
    return outputs

if __name__ == "__main__":
    test_data_1 = [["FILE_UPLOAD", "Cars.txt", "200kb"], 
                              ["FILE_GET", "Cars.txt"], 
                              ["FILE_COPY", "Cars.txt", "Cars2.txt"], 
                              ["FILE_GET", "Cars2.txt"]]
    test_data_2 = [["FILE_UPLOAD", "Foo.txt", "100kb"], 
                            ["FILE_UPLOAD", "Bar.csv", "200kb"], 
                            ["FILE_UPLOAD", "Baz.pdf", "300kb"],
                            ["FILE_SEARCH", "Ba"]]
    test_data_3 = [
            ["FILE_UPLOAD_AT", "2021-07-01T12:00:00", "Python.txt", "150kb"], 
            ["FILE_UPLOAD_AT", "2021-07-01T12:00:00", "CodeSignal.txt", "150kb", 3600], 
            ["FILE_GET_AT", "2021-07-01T13:00:01", "Python.txt"], 
            ["FILE_COPY_AT", "2021-07-01T12:00:00", "Python.txt", "PythonCopy.txt"], 
            ["FILE_SEARCH_AT", "2021-07-01T12:00:00", "Py"],
            ["FILE_UPLOAD_AT", "2021-07-01T12:00:00", "Expired.txt", "100kb", 1], 
            ["FILE_GET_AT", "2021-07-01T12:00:02", "Expired.txt"], 
            ["FILE_COPY_AT", "2021-07-01T12:00:00", "CodeSignal.txt", "CodeSignalCopy.txt"], 
            ["FILE_SEARCH_AT", "2021-07-01T12:00:00", "Code"]]
    test_data_4 = [
            ["FILE_UPLOAD_AT", "2021-07-01T12:00:00", "Initial.txt", "100kb"], 
            ["FILE_UPLOAD_AT", "2021-07-01T12:05:00", "Update1.txt", "150kb", 3600], 
            ["FILE_GET_AT", "2021-07-01T12:10:00", "Initial.txt"], 
            ["FILE_COPY_AT", "2021-07-01T12:15:00", "Update1.txt", "Update1Copy.txt"], 
            ["FILE_UPLOAD_AT", "2021-07-01T12:20:00", "Update2.txt", "200kb", 1800], 
            ["ROLLBACK", "2021-07-01T12:10:00"], 
            ["FILE_GET_AT", "2021-07-01T12:25:00", "Update1.txt"], 
            ["FILE_GET_AT", "2021-07-01T12:25:00", "Initial.txt"], 
            ["FILE_SEARCH_AT", "2021-07-01T12:25:00", "Up"],
            ["FILE_GET_AT", "2021-07-01T12:25:00", "Update2.txt"]]
   
    output_data_1 = ["uploaded Cars.txt", "got Cars.txt", "copied Cars.txt to Cars2.txt", "got Cars2.txt"]
    output_data_2 = ["uploaded Foo.txt", "uploaded Bar.csv", "uploaded Baz.pdf", "found [Baz.pdf, Bar.csv]"]
    output_data_3 = ["uploaded at Python.txt", "uploaded at CodeSignal.txt", "got at Python.txt", "copied at Python.txt to PythonCopy.txt", "found at [Python.txt, PythonCopy.txt]", "uploaded at Expired.txt", "file not found", "copied at CodeSignal.txt to CodeSignalCopy.txt", "found at [CodeSignal.txt, CodeSignalCopy.txt]"]
    output_data_4 = ["uploaded at Initial.txt", "uploaded at Update1.txt", "got at Initial.txt", "copied at Update1.txt to Update1Copy.txt", "uploaded at Update2.txt", "rollback to 2021-07-01T12:10:00", "got at Update1.txt", "got at Initial.txt", "found at [Update1.txt, Update1Copy.txt, Update2.txt]", "got at Update2.txt"]

    pass_1 = simulate_coding_framework(test_data_1) == output_data_1
    print(pass_1)

    pass_2 = simulate_coding_framework(test_data_2) == output_data_2
    print(pass_2)

    pass_3 = simulate_coding_framework(test_data_3) == output_data_3
    print(pass_3)

    pass_4 = simulate_coding_framework(test_data_4) == output_data_4
    print(simulate_coding_framework(test_data_4))
    print(output_data_4)
    print(pass_4)