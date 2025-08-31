# Banking Transaction System - Practice Assessment

## Scenario

Your task is to implement a sophisticated banking transaction system that handles multiple accounts, various transaction types, fraud detection, and temporal operations. This system is significantly more complex than a simple file storage system and will test your ability to handle financial logic, data validation, and complex state management.

All operations that should be supported are listed below. Partial credit will be granted for each test passed, so press "Submit" often to run tests and receive partial credits for passed tests. Please check tests for requirements and argument types.

### Implementation Tips

Read the question all the way through before you start coding, but implement the operations and complete the levels one by one, not all together, keeping in mind that you will need to refactor to support additional functionality. Please, do not change the existing method signatures.

The banking system becomes progressively more complex with each level, introducing new concepts like fraud detection, temporal operations, and rollback functionality.

## Task

Example of banking system state with various accounts and transactions:

```plaintext
[BankingSystem] - Central Transaction Processor
    Accounts:
    +- ACC001 (John Doe) - Balance: $2,500.00, Status: ACTIVE
    +- ACC002 (Jane Smith) - Balance: $1,200.00, Status: ACTIVE  
    +- ACC003 (Bob Wilson) - Balance: $750.00, Status: FROZEN
    
    Recent Transactions:
    +- TXN001: DEPOSIT $500.00 to ACC001 (2024-01-15 10:30:00)
    +- TXN002: TRANSFER $200.00 from ACC001 to ACC002 (2024-01-15 11:15:00)
    +- TXN003: WITHDRAWAL $100.00 from ACC002 (2024-01-15 12:00:00)
```

## Level 1 – Basic Account Management & Transactions

### Core Operations:

- **CREATE_ACCOUNT(account_id, owner_name, initial_balance)**
  - Create a new account with the specified ID, owner name, and initial balance
  - Initial balance must be non-negative
  - If account ID already exists, throw a runtime exception
  - Account starts in ACTIVE status

- **GET_BALANCE(account_id)**
  - Return the current balance of the specified account
  - If account doesn't exist, return "account not found"

- **DEPOSIT(account_id, amount)**
  - Add the specified amount to the account balance
  - Amount must be positive
  - If account doesn't exist, return "account not found"
  - If account is not ACTIVE, return "account inactive"

- **WITHDRAW(account_id, amount)**
  - Subtract the specified amount from the account balance
  - Amount must be positive
  - If account doesn't exist, return "account not found"
  - If account is not ACTIVE, return "account inactive"
  - If insufficient funds, return "insufficient funds"

- **TRANSFER(from_account, to_account, amount)**
  - Transfer amount from one account to another
  - Amount must be positive
  - Both accounts must exist and be ACTIVE
  - Source account must have sufficient funds
  - If any validation fails, return appropriate error message

### Expected Return Messages:
- Successful operations return descriptive messages like:
  - "created account ACC001 for John Doe with balance $1000.00"
  - "deposited $500.00 to ACC001, new balance $1500.00"
  - "withdrew $200.00 from ACC001, new balance $1300.00"
  - "transferred $100.00 from ACC001 to ACC002"
