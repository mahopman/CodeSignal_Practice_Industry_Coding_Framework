import json
import math
import string
import re
import random
import sys
import traceback
import functools
from collections import OrderedDict
import numpy as np
from datetime import datetime as dt

import numpy
import sortedcontainers

size_map = {"kb": 1000}

def to_bytes(size: str):
    unit = size[-2:]
    amount = int(size[:-2])
    return amount * size_map[unit]

class File:
    def __init__(self, file_name: str, size: str, timestamp: str = None, ttl: int = np.inf):
        self.file_name = file_name
        self.size = size
        self.size_bytes = to_bytes(size)
        if timestamp:  
            self.uploaded_at = dt.fromisoformat(timestamp)
        self.ttl = dt.second(ttl)
    def is_alive(self, timestamp: str):
        return dt.fromisoformat(timestamp) - (self.uploaded_at + self.ttl)

class FileSystem:
    def __init__(self):
        self.files: list[File] = []

    def file_upload(self, file_name: str, size: str):
        for file in self.files:
            if file.file_name == file_name:
                RuntimeError(f"File with name: {file_name} already exsists")
        self.files.append(File(file_name, size))
        return f"uploaded {file_name}"

    def file_get(self, file_name):
        for file in self.files:
            if file.file_name == file_name:
                return f"got {file_name}"
    
    def file_copy(self, source: str, dest: str):
        for i, file in enumerate(self.files):
            if file.file_name == dest:
                self.files.pop(i)
            if file.file_name == source:
                file.file_name = dest
                return f"copied {source} to {dest}"
        RuntimeError(f"File with name: {source} does not exsist")

    def file_search(self, prefix: str):
        search_res = []
        for file in self.files:
            if file.file_name.startswith(prefix):
                search_res.append((file.file_name, file.size_bytes))
        search_res.sort(key = lambda x: (-x[1], x[0]))
        res = "found ["
        for file_name, size in search_res[:10]:
            res += f"{file_name}, "
        res = res[:-2] + "]"
        return res
    
    def file_upload_at(self, timestamp: str, file_name: str, size: str, ttl: int = np.inf):
        for file in self.files:
            if file.file_name == file_name:
                RuntimeError(f"File with name: {file_name} already exsists")
        self.files.append(File(file_name, size, timestamp, ttl))
        return f"uploaded at {file_name}"
    
    def file_get_at(self, timestamp: str, file_name: str):
        for file in self.files:
            if file.file_name == file_name and file.is_alive(timestamp):
                return f"got at {file_name}"
        
    def file_copy_at(self, timestamp: str, file_from: str, file_to: str):
        for i, file in enumerate(self.files):
            if file.file_name == file_to:
                self.files.pop(i)
            if file.file_name == file_from:
                file.file_name = file_to
                file.timestamp = timestamp
                return f"copied at {file_from} to {file_to}"
        RuntimeError(f"File with name: {file_from} does not exsist")
    
    def file_search_at(self, timestamp: str, prefix: str):
        search_res = []
        for file in self.files:
            if file.file_name.startswith(prefix) and file.is_alive(timestamp):
                search_res.append((file.file_name, file.size_bytes))
        search_res.sort(key = lambda x: (-x[1], x[0]))
        res = "found ["
        for file_name, size in search_res[:10]:
            res += f"{file_name}, "
        res = res[:-2] + "]"
        return res



def simulate_coding_framework(list_of_lists):
    """
    Simulates a coding framework operation on a list of lists of strings.

    Parameters:
    list_of_lists (List[List[str]]): A list of lists containing strings.
    """
    res = []
    file_system = FileSystem()
    for list in list_of_lists:
        if list[0] == "FILE_UPLOAD":
            res.append(file_system.file_upload(file_name=list[1], size=list[2]))
        if list[0] == "FILE_GET":
            res.append(file_system.file_get(file_name=list[1]))
        if list[0] == "FILE_COPY":
            res.append(file_system.file_copy(source=list[1], dest=list[2]))
        if list[0] == "FILE_SEARCH":
            res.append(file_system.file_search(prefix=list[1]))
        if list[0] == "FILE_UPLOAD_AT":
            res.append(file_system.file_upload_at(timestamp=list[1], file_name=list[2], size=list[3]))
        if list[0] == "FILE_GET_AT":
            res.append(file_system.file_get_at(timestamp=list[1], file_name=list[2]))
        if list[0] == "FILE_COPY_AT":
            res.append(file_system.file_copy_at(timestamp=list[1], file_from=list[2], file_to=list[3]))
        if list[0] == "FILE_SEARCH_AT":
            res.append(file_system.file_search_at(timestamp=list[1], prefix=list[2]))
    return res
    

        



