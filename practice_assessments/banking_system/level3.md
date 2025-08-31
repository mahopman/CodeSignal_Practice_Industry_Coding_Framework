# Banking Transaction System - Level 3

## Level 3 – Temporal Operations & Fraud Detection

Building on Levels 1-2, we now add timestamp-based operations and basic fraud detection capabilities.

### Temporal Operations:
All existing operations now have timestamp-aware versions that allow you to specify when the operation should be considered to have occurred.

- **CREATE_ACCOUNT_AT(timestamp, account_id, owner_name, initial_balance)**
- **DEPOSIT_AT(timestamp, account_id, amount)**
- **WITHDRAW_AT(timestamp, account_id, amount)**
- **TRANSFER_AT(timestamp, from_account, to_account, amount)**
- **GET_BALANCE_AT(timestamp, account_id)**
  - Return the account balance as it was at the specified timestamp
- **FREEZE_ACCOUNT_AT(timestamp, account_id)**
- **UNFREEZE_ACCOUNT_AT(timestamp, account_id)**

### Fraud Detection Operations:

- **DETECT_SUSPICIOUS_ACTIVITY(account_id, time_window_minutes)**
  - Detect if an account has suspicious activity within the specified time window
  - Suspicious activity criteria:
    - More than 5 transactions in the time window
    - Total withdrawal amount > $10,000 in the time window
    - More than 3 failed transaction attempts in the time window
  - Return "suspicious activity detected" or "no suspicious activity"

- **SET_DAILY_WITHDRAWAL_LIMIT(account_id, limit)**
  - Set a daily withdrawal limit for an account
  - Default limit is $5,000 if not set
  - If account doesn't exist, return "account not found"

- **CHECK_DAILY_WITHDRAWAL_LIMIT(account_id, amount)**
  - Check if a withdrawal would exceed the daily limit
  - Consider all withdrawals made on the current day
  - Return "within limit" or "exceeds daily limit"

- **BLOCK_ACCOUNT(account_id, reason)**
  - Block an account due to suspicious activity
  - Blocked accounts cannot perform any operations
  - Reason should be logged (e.g., "fraud_detection", "manual_review")
  - If account doesn't exist, return "account not found"

- **GET_FAILED_TRANSACTIONS(account_id, hours)**
  - Get all failed transaction attempts for an account in the last N hours
  - Include transaction type, amount, timestamp, and failure reason

### Enhanced Transaction Validation:
- All transactions now validate against fraud detection rules
- Failed transactions are logged for analysis
- Temporal consistency checks (can't perform operations before account creation)
- Daily limits are enforced automatically

### Expected Return Messages:
- "created account at ACC001 for John Doe with balance $1000.00 at 2024-01-15T10:30:00"
- "suspicious activity detected for ACC001"
- "set daily withdrawal limit for ACC001 to $2500.00"
- "withdrawal exceeds daily limit"
- "blocked account ACC001 due to fraud_detection"
