# Banking Transaction System - CodeSignal Practice Assessment

## Overview

This is a significantly more challenging version of the original file storage practice assessment, reimagined as a sophisticated banking transaction system. While the original system dealt with simple file operations, this banking system introduces complex financial logic, fraud detection, temporal operations, and advanced state management.

## Complexity Comparison

### Original File Storage System
- **Level 1**: Basic file upload/get/copy operations
- **Level 2**: File search with prefix matching
- **Level 3**: Timestamp-based operations with TTL
- **Level 4**: Simple rollback functionality

### New Banking System (Much More Challenging)
- **Level 1**: Account creation, deposits, withdrawals, transfers with validation
- **Level 2**: Transaction history, account freezing, balance queries, analytics
- **Level 3**: Temporal operations, fraud detection, daily limits, suspicious activity monitoring
- **Level 4**: System rollback, bulk operations, money laundering detection, advanced analytics

## Key Improvements & Added Complexity

### 1. **Financial Domain Logic**
- Decimal precision for monetary amounts (no floating point errors)
- Account status management (ACTIVE, FROZEN, BLOCKED)
- Daily withdrawal limits and velocity controls
- Insufficient funds validation
- Multi-account transaction atomicity

### 2. **Advanced Data Structures**
- Complex account objects with metadata
- Transaction history with full audit trail
- Failed transaction logging for fraud analysis
- Temporal state reconstruction
- Checkpoint system for rollbacks

### 3. **Fraud Detection & Security**
- Daily withdrawal limits (default $5,000)
- Suspicious activity detection algorithms
- Velocity limits (transactions per hour, amount per hour)
- Account whitelisting for trusted transfers
- Money laundering pattern detection
- Failed transaction attempt tracking

### 4. **Temporal Operations**
- All operations can be performed "at" specific timestamps
- Balance reconstruction at any point in time
- Temporal consistency validation (no operations before account creation)
- Complex rollback scenarios with state restoration

### 5. **Advanced Features**
- Bulk transfer operations (atomic multi-recipient transfers)
- Net flow calculations between timestamps
- Account relationship analysis
- System-wide analytics and reporting
- Comprehensive error handling and validation

## Technical Implementation Highlights

### Precision & Accuracy
```python
from decimal import Decimal, ROUND_HALF_UP

# All monetary amounts use Decimal for precision
balance = Decimal('1000.00')
amount = Decimal('123.45')
```

### Transaction Logging
```python
# Every operation is logged with full metadata
transaction = {
    'id': 'TXN000001',
    'type': 'TRANSFER_OUT', 
    'account_id': 'ACC001',
    'amount': Decimal('500.00'),
    'timestamp': datetime.now(),
    'status': 'SUCCESS',
    'details': {'to_account': 'ACC002'}
}
```

### Fraud Detection
```python
# Daily withdrawal limit enforcement
today = datetime.now().date()
daily_total = self.daily_withdrawals[account_id].get(today, Decimal('0'))
if daily_total + amount > daily_limit:
    return "exceeds daily limit"
```

### Temporal State Reconstruction
```python
# Calculate balance at any point in time
def get_balance_at(self, timestamp, account_id):
    balance = Decimal('0')
    for txn in self.transactions:
        if txn['timestamp'] <= timestamp and txn['account_id'] == account_id:
            # Apply transaction to balance
```

## Test Coverage

The test suite includes comprehensive coverage of:

1. **Basic Operations**: Account creation, deposits, withdrawals, transfers
2. **Error Handling**: Invalid accounts, insufficient funds, frozen accounts
3. **Edge Cases**: Zero balances, exact withdrawals, large amounts
4. **Temporal Operations**: Operations at specific timestamps, balance reconstruction
5. **Fraud Detection**: Daily limits, suspicious activity patterns
6. **Complex Scenarios**: Multi-account interactions, state consistency

## Running the Tests

```bash
# Activate virtual environment
source venv/bin/activate

# Navigate to the banking system directory
cd practice_assessments/file_storage

# Run the tests
python test_banking_simulation.py
```

## Difficulty Progression

### Level 1: Foundation (Moderate)
- Basic account management
- Simple transaction validation
- Error handling for common cases
- **Skills Tested**: Object-oriented design, basic validation, decimal arithmetic

### Level 2: Intermediate (Challenging)
- Transaction history tracking
- Account status management
- Advanced queries and analytics
- **Skills Tested**: Data structures, sorting algorithms, state management

### Level 3: Advanced (Very Challenging)
- Temporal operations with timestamp handling
- Fraud detection algorithms
- Daily limits and velocity controls
- **Skills Tested**: Time-based logic, pattern detection, complex validation

### Level 4: Expert (Extremely Challenging)
- System rollback and state restoration
- Bulk operations with atomicity
- Money laundering detection
- Advanced analytics and reporting
- **Skills Tested**: System design, transaction management, advanced algorithms

## Key Learning Outcomes

Candidates working through this assessment will learn:

1. **Financial Software Development**: Handling money with precision, regulatory compliance
2. **Complex State Management**: Temporal operations, rollbacks, consistency
3. **Fraud Detection**: Pattern recognition, anomaly detection, security measures
4. **System Design**: Scalable architecture, transaction logging, error handling
5. **Advanced Algorithms**: Time-series analysis, graph relationships, bulk operations

This banking system provides a much more realistic and challenging assessment that better reflects the complexity of real-world financial software development.

## Files

- `simulation.py` - Main implementation file (starter code - needs to be completed)
- `test_simulation.py` - Comprehensive test suite with 9 test cases
- `level1.md` - Level 1 requirements and specifications
- `level2.md` - Level 2 requirements and specifications  
- `level3.md` - Level 3 requirements and specifications
- `level4.md` - Level 4 requirements and specifications

## Implementation Notes

The main function to implement is:

```python
def simulate_banking_system(operations_list):
    """
    Simulates a banking system with various operations.
    
    Parameters:
    operations_list (List[List[str]]): A list of operations to perform.
    """
    # Implementation needed here
    pass
```

This assessment provides a significantly more challenging and realistic assessment compared to the original file storage system, while maintaining the same progressive structure and testing methodology.
