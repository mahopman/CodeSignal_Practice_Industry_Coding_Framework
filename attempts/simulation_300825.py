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
import sortedcontainers

from datetime import datetime as dt
from datetime import timedelta

class File():
    def __init__(self, file_name, size, upload_time = None, ttl = 10000000000):
        self.file_name = file_name
        self.size = size
        self.upload_time = dt.fromisoformat(upload_time)
        self.ttl = ttl

    def is_alive(self, timestamp):
        return self.upload_time + timedelta(seconds=self.ttl) > dt.fromisoformat(timestamp) 

class FileSystem():
    def __init__(self):
        self.files = []
    
    def FILE_UPLOAD(self, file_name, size):
        file_names = [file.file_name for file in self.files]

        if file_name in file_names:
            print(f"File with name {file_name} already exists")
        self.files.append(File(file_name, size))

        return f"uploaded {file_name}"

    def FILE_GET(self, file_name):
        for file in self.files:
            if file.file_name == file_name:
                return f"got {file_name}"

    def FILE_GET_SIZE(self, file_name):
        for file in self.files:
            if file.file_name == file_name:
                return file.size

    def FILE_COPY(self, source, dest):
        source_size = self.FILE_GET_SIZE(source)
        if not source_size:
            RuntimeError(f"{source} does not exist")
        
        for file in self.files:
            if file.file_name == dest:
                file.size = source_size
                return f"copied {source} to {dest}"

        self.FILE_UPLOAD(dest, source_size)
        return f"copied {source} to {dest}"

    def FILE_SEARCH(self, prefix):
        files = []
        for file in self.files:
            if file.file_name.startswith(prefix):
                files.append(file)
        files.sort(key = lambda file: (file.size, file.file_name), reverse=True)
        res = ", ".join([file.file_name for file in files[:10]])
        return f"found [{res}]"

    def FILE_UPLOAD_AT(self, timestamp, file_name, file_size, ttl = 100000000000):
        file_names = [file.file_name for file in self.files]

        if file_name in file_names:
            print(f"File with name {file_name} already exists")
        self.files.append(File(file_name, file_size, timestamp, ttl))

        return f"uploaded at {file_name}"

    def FILE_GET_AT(self, timestamp, file_name):
        for file in self.files:
            if file.file_name == file_name and file.is_alive(timestamp):
                return f"got at {file_name}"
        return "file not found"

    def FILE_COPY_AT(self, timestamp, file_from, file_to):
        source_size = self.FILE_GET_SIZE(file_from)
        if not source_size:
            RuntimeError(f"{file_from} does not exist")
        
        for file in self.files:
            if file.file_name == file_to:
                file.size = source_size
                file.upload_time = timestamp
                return f"copied {file_from} to {file_to}"

        self.FILE_UPLOAD_AT(timestamp, file_to, source_size)
        return f"copied at {file_from} to {file_to}"

    def FILE_SEARCH_AT(self, timestamp, prefix):
        files = []
        for file in self.files:
            if file.file_name.startswith(prefix) and file.is_alive(timestamp):
                files.append(file)
        files.sort(key = lambda file: (-int(file.size[:-2]), file.file_name))
        res = ", ".join([file.file_name for file in files[:10]])
        return f"found at [{res}]"

    def ROLLBACK(self, timestamp):
        files_to_remove = []
        for file in self.files:
            if file.upload_time > dt.fromisoformat(timestamp):
                files_to_remove.append(file)
        for file in files_to_remove:
            self.files.remove(file)
        return f"rollback to {timestamp}"
            
        

def simulate_coding_framework(list_of_lists):
    """
    Simulates a coding framework operation on a list of lists of strings.

    Parameters:
    list_of_lists (List[List[str]]): A list of lists containing strings.
    """
    file_system = FileSystem()
    res = []

    for operation_list in list_of_lists:
        operation = operation_list[0]
        
        # Convert operation name to method name (lowercase with underscores)
        
        # Get the method using getattr (method dispatch)
        method = getattr(file_system, operation, None)
        
        if method is None:
            raise ValueError(f"Unknown operation: {operation}")
        
        # Call the method with remaining arguments
        result = method(*operation_list[1:])
        res.append(result)
    return res
