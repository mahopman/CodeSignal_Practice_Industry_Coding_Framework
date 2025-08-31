# Banking Transaction System - Level 2

## Level 2 – Transaction History & Advanced Queries

Building on Level 1, we now add transaction tracking, account management, and sophisticated query capabilities.

### New Operations:

- **GET_TRANSACTION_HISTORY(account_id, limit)**
  - Return the most recent `limit` transactions for the specified account
  - Transactions should be ordered by timestamp (most recent first)
  - Include transaction type, amount, and timestamp
  - If account doesn't exist, return "account not found"

- **FREEZE_ACCOUNT(account_id)**
  - Set account status to FROZEN
  - Frozen accounts cannot perform any transactions (deposits, withdrawals, transfers)
  - If account doesn't exist, return "account not found"

- **UNFREEZE_ACCOUNT(account_id)**
  - Set account status back to ACTIVE
  - If account doesn't exist, return "account not found"

- **FIND_ACCOUNTS_BY_BALANCE_RANGE(min_balance, max_balance)**
  - Find all ACTIVE accounts with balance between min_balance and max_balance (inclusive)
  - Return list of account IDs sorted by balance (descending), then by account ID (ascending) for ties
  - Only include accounts with ACTIVE status

- **GET_TOP_ACCOUNTS(limit)**
  - Return the top `limit` accounts by balance
  - Only include ACTIVE accounts
  - Sort by balance (descending), then by account ID (ascending) for ties
  - Return account ID, owner name, and balance

- **CALCULATE_TOTAL_DEPOSITS(account_id)**
  - Calculate the total amount of all deposits made to the account
  - If account doesn't exist, return "account not found"

- **CALCULATE_TOTAL_WITHDRAWALS(account_id)**
  - Calculate the total amount of all withdrawals made from the account
  - If account doesn't exist, return "account not found"

### Enhanced Features:
- All transactions are now logged with timestamps
- Account status management (ACTIVE, FROZEN)
- Advanced querying and analytics capabilities
- Transaction categorization and summaries

### Expected Return Messages:
- "froze account ACC001"
- "unfroze account ACC002"  
- "found accounts [ACC001, ACC003, ACC005]"
- "top accounts: ACC001 (John Doe, $5000.00), ACC002 (Jane Smith, $3200.00)"
- "total deposits for ACC001: $2500.00"
