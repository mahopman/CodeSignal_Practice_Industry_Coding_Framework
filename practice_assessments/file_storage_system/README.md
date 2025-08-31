# File Storage System - CodeSignal Practice Assessment

## Overview

This is the original file storage system practice assessment. It simulates a simplified file hosting service with basic operations like upload, get, copy, search, and temporal operations with TTL (time-to-live).

## Assessment Structure

The assessment is divided into 4 progressive levels:

### Level 1 – Initial Design & Basic Functions
- **FILE_UPLOAD(file_name, size)** - Upload files to remote storage
- **FILE_GET(file_name)** - Retrieve file information
- **FILE_COPY(source, dest)** - Copy files to new locations

### Level 2 – Data Structures & Data Processing
- **FILE_SEARCH(prefix)** - Find files by prefix, ordered by size

### Level 3 – Refactoring & Encapsulation
- Timestamp-based operations with TTL support
- **FILE_UPLOAD_AT**, **FILE_GET_AT**, **FILE_COPY_AT**, **FILE_SEARCH_AT**

### Level 4 – Extending Design & Functionality
- **ROLLBACK(timestamp)** - Rollback system state to specific timestamp

## Files

- `simulation.py` - Main implementation (starter code - needs to be completed)
- `test_simulation.py` - Comprehensive test suite
- `level1.md` - Level 1 requirements and specifications
- `level2.md` - Level 2 requirements and specifications
- `level3.md` - Level 3 requirements and specifications
- `level4.md` - Level 4 requirements and specifications

## Running the Tests

```bash
# From the repository root
cd practice_assessments/file_storage_system

# Run tests
python test_simulation.py
```

## Implementation Notes

The main function to implement is:

```python
def simulate_coding_framework(list_of_lists):
    """
    Simulates a coding framework operation on a list of lists of strings.
    
    Parameters:
    list_of_lists (List[List[str]]): A list of lists containing strings.
    """
    # Implementation needed here
    pass
```

This assessment tests fundamental programming concepts:
- Basic data structures (dictionaries, lists)
- String manipulation and searching
- Time-based logic and TTL handling
- State management and rollback functionality

## Difficulty Level

**Beginner to Intermediate** - Suitable for entry-level to mid-level developers. Focuses on core programming concepts and basic system design principles.
