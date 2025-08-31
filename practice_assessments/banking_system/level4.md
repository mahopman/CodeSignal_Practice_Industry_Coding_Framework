# Banking Transaction System - Level 4

## Level 4 – Advanced Features & System Rollback

Building on Levels 1-3, we now add the most complex features including system rollback, advanced fraud detection, and multi-account operations.

### System Rollback Operations:

- **ROLLBACK_TO_TIMESTAMP(timestamp)**
  - Rollback the entire banking system state to the specified timestamp
  - All accounts, balances, and transaction history should reflect the state at that time
  - All transactions after the rollback timestamp should be removed
  - Account statuses (ACTIVE, FROZEN, BLOCKED) should be restored
  - Daily limits and fraud detection settings should be restored
  - Return "rolled back to [timestamp]"

- **CREATE_CHECKPOINT(checkpoint_name)**
  - Create a named checkpoint of the current system state
  - Can be used for faster rollback operations
  - Return "checkpoint [name] created"

- **ROLLBACK_TO_CHECKPOINT(checkpoint_name)**
  - Rollback to a previously created checkpoint
  - If checkpoint doesn't exist, return "checkpoint not found"

### Advanced Fraud Detection:

- **ANALYZE_TRANSACTION_PATTERNS(account_id, days)**
  - Analyze transaction patterns for unusual behavior over the specified number of days
  - Detect patterns like:
    - Unusual transaction times (outside normal hours)
    - Sudden large transactions compared to historical average
    - Rapid succession of small transactions (potential money laundering)
    - Geographic inconsistencies (if location data available)
  - Return detailed analysis report

- **SET_VELOCITY_LIMITS(account_id, max_transactions_per_hour, max_amount_per_hour)**
  - Set velocity limits to prevent rapid-fire transactions
  - If limits are exceeded, temporarily freeze the account
  - Return "velocity limits set for ACC001"

- **WHITELIST_ACCOUNT(account_id, trusted_account_id)**
  - Add an account to another account's whitelist for transfers
  - Transfers to whitelisted accounts have relaxed fraud detection
  - Return "ACC002 whitelisted for ACC001"

### Multi-Account Operations:

- **BULK_TRANSFER(from_account, transfer_list)**
  - Perform multiple transfers from one account to multiple recipients
  - transfer_list format: [(to_account1, amount1), (to_account2, amount2), ...]
  - All transfers must succeed or none are processed (atomic operation)
  - Check total amount against account balance before processing
  - Return "bulk transfer completed: X transfers totaling $Y.YY"

- **CALCULATE_NET_FLOW(account_id, start_timestamp, end_timestamp)**
  - Calculate net money flow (inflows - outflows) for an account between timestamps
  - Include deposits, withdrawals, and transfers
  - Return "net flow for ACC001: +$1,250.00" (+ for net inflow, - for net outflow)

- **GET_ACCOUNT_RELATIONSHIPS(account_id)**
  - Find all accounts that have had transactions with the specified account
  - Return accounts sorted by total transaction volume
  - Include relationship strength (number of transactions and total amount)

### System Analytics:

- **GENERATE_DAILY_REPORT(date)**
  - Generate a comprehensive daily report including:
    - Total number of transactions
    - Total money moved
    - Number of new accounts created
    - Number of fraud alerts
    - Top 5 most active accounts
  - Return formatted report

- **DETECT_MONEY_LAUNDERING_PATTERNS()**
  - System-wide analysis to detect potential money laundering
  - Look for circular transfers, structuring patterns, rapid movement of funds
  - Return list of suspicious account groups

### Expected Return Messages:
- "rolled back to 2024-01-15T10:30:00"
- "checkpoint daily_backup created"
- "velocity limits set for ACC001: 10 transactions/hour, $5000/hour"
- "bulk transfer completed: 5 transfers totaling $2,750.00"
- "net flow for ACC001 from 2024-01-15 to 2024-01-16: +$1,250.00"
- "suspicious money laundering pattern detected: accounts [ACC001, ACC005, ACC009]"
