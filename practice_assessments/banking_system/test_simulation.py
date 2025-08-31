import unittest
from unittest.mock import patch
from simulation import simulate_banking_system

class TestBankingSystem(unittest.TestCase):

    def setUp(self):
        """Set up test data for all levels"""
        
        # Level 1 Tests - Basic Account Management & Transactions
        self.level1_basic_operations = [
            ["CREATE_ACCOUNT", "ACC001", "John Doe", "1000.00"],
            ["CREATE_ACCOUNT", "ACC002", "Jane Smith", "500.00"],
            ["GET_BALANCE", "ACC001"],
            ["DEPOSIT", "ACC001", "200.00"],
            ["WITHDRAW", "ACC002", "100.00"],
            ["TRANSFER", "ACC001", "ACC002", "150.00"]
        ]
        
        self.level1_error_cases = [
            ["CREATE_ACCOUNT", "ACC001", "John Doe", "1000.00"],
            ["CREATE_ACCOUNT", "ACC001", "Jane Smith", "500.00"],  # Duplicate account
            ["GET_BALANCE", "ACC999"],  # Non-existent account
            ["DEPOSIT", "ACC999", "100.00"],  # Non-existent account
            ["WITHDRAW", "ACC001", "2000.00"],  # Insufficient funds
            ["TRANSFER", "ACC001", "ACC999", "100.00"]  # Non-existent destination
        ]
        
        self.level1_edge_cases = [
            ["CREATE_ACCOUNT", "ACC001", "Alice Johnson", "0.00"],  # Zero balance
            ["DEPOSIT", "ACC001", "0.01"],  # Minimum deposit
            ["WITHDRAW", "ACC001", "0.01"],  # Exact balance withdrawal
            ["CREATE_ACCOUNT", "ACC002", "Bob Wilson", "10000.00"],
            ["TRANSFER", "ACC002", "ACC001", "5000.00"]  # Large transfer
        ]
        
        # Level 2 Tests - Transaction History & Advanced Queries
        self.level2_account_management = [
            ["CREATE_ACCOUNT", "ACC001", "John Doe", "2000.00"],
            ["CREATE_ACCOUNT", "ACC002", "Jane Smith", "1500.00"],
            ["CREATE_ACCOUNT", "ACC003", "Bob Wilson", "3000.00"],
            ["DEPOSIT", "ACC001", "500.00"],
            ["WITHDRAW", "ACC002", "200.00"],
            ["TRANSFER", "ACC003", "ACC001", "800.00"],
            ["FREEZE_ACCOUNT", "ACC002"],
            ["DEPOSIT", "ACC002", "100.00"],  # Should fail - frozen account
            ["UNFREEZE_ACCOUNT", "ACC002"],
            ["WITHDRAW", "ACC002", "50.00"]  # Should succeed now
        ]
        
        # Level 3 Tests - Temporal Operations & Fraud Detection
        self.level3_temporal_operations = [
            ["CREATE_ACCOUNT_AT", "2024-01-15T09:00:00", "ACC001", "Alice Brown", "2500.00"],
            ["CREATE_ACCOUNT_AT", "2024-01-15T09:30:00", "ACC002", "Charlie Davis", "1800.00"],
            ["DEPOSIT_AT", "2024-01-15T10:00:00", "ACC001", "300.00"],
            ["WITHDRAW_AT", "2024-01-15T10:30:00", "ACC002", "150.00"],
            ["TRANSFER_AT", "2024-01-15T11:00:00", "ACC001", "ACC002", "400.00"],
            ["GET_BALANCE_AT", "2024-01-15T10:15:00", "ACC001"],
            ["FREEZE_ACCOUNT_AT", "2024-01-15T11:30:00", "ACC002"],
            ["WITHDRAW_AT", "2024-01-15T12:00:00", "ACC002", "100.00"],  # Should fail - frozen
            ["UNFREEZE_ACCOUNT_AT", "2024-01-15T12:30:00", "ACC002"]
        ]
        
        self.level3_fraud_detection = [
            ["CREATE_ACCOUNT", "ACC001", "Suspicious User", "5000.00"],
            ["WITHDRAW", "ACC001", "1000.00"],
            ["WITHDRAW", "ACC001", "1500.00"],
            ["WITHDRAW", "ACC001", "2000.00"],  # Large withdrawals
            ["CREATE_ACCOUNT", "ACC002", "Normal User", "3000.00"],
            ["WITHDRAW", "ACC002", "100.00"],
            ["DEPOSIT", "ACC002", "50.00"]
        ]
        
        # Level 4 Tests - Advanced Features & System Rollback
        self.level4_rollback_scenario = [
            ["CREATE_ACCOUNT_AT", "2024-01-15T09:00:00", "ACC001", "Test User 1", "1000.00"],
            ["CREATE_ACCOUNT_AT", "2024-01-15T09:30:00", "ACC002", "Test User 2", "1500.00"],
            ["DEPOSIT_AT", "2024-01-15T10:00:00", "ACC001", "500.00"],
            ["TRANSFER_AT", "2024-01-15T10:30:00", "ACC001", "ACC002", "200.00"],
            ["WITHDRAW_AT", "2024-01-15T11:00:00", "ACC002", "300.00"],
            ["GET_BALANCE", "ACC001"],  # Should show current balance
            ["GET_BALANCE", "ACC002"],  # Should show current balance
            # Rollback functionality would be tested here if implemented
        ]
        
        self.level4_bulk_operations = [
            ["CREATE_ACCOUNT", "ACC001", "Main Account", "10000.00"],
            ["CREATE_ACCOUNT", "ACC002", "Recipient 1", "0.00"],
            ["CREATE_ACCOUNT", "ACC003", "Recipient 2", "0.00"],
            ["CREATE_ACCOUNT", "ACC004", "Recipient 3", "0.00"],
            # Bulk transfer would be: ["BULK_TRANSFER", "ACC001", [("ACC002", "1000"), ("ACC003", "1500"), ("ACC004", "2000")]]
        ]

    def test_level1_basic_operations(self):
        """Test Level 1: Basic account operations"""
        output = simulate_banking_system(self.level1_basic_operations)
        expected = [
            "created account ACC001 for John Doe with balance $1000.00",
            "created account ACC002 for Jane Smith with balance $500.00", 
            "balance $1000.00",
            "deposited $200.00 to ACC001, new balance $1200.00",
            "withdrew $100.00 from ACC002, new balance $400.00",
            "transferred $150.00 from ACC001 to ACC002"
        ]
        self.assertEqual(output, expected)

    def test_level1_error_handling(self):
        """Test Level 1: Error handling and edge cases"""
        output = simulate_banking_system(self.level1_error_cases)
        expected = [
            "created account ACC001 for John Doe with balance $1000.00",
            "error: Account ACC001 already exists",
            "account not found",
            "account not found", 
            "insufficient funds",
            "destination account not found"
        ]
        self.assertEqual(output, expected)

    def test_level1_edge_cases(self):
        """Test Level 1: Edge cases with zero balances and large amounts"""
        output = simulate_banking_system(self.level1_edge_cases)
        expected = [
            "created account ACC001 for Alice Johnson with balance $0.00",
            "deposited $0.01 to ACC001, new balance $0.01",
            "withdrew $0.01 from ACC001, new balance $0.00",
            "created account ACC002 for Bob Wilson with balance $10000.00",
            "transferred $5000.00 from ACC002 to ACC001"
        ]
        self.assertEqual(output, expected)

    def test_level2_account_management(self):
        """Test Level 2: Account freezing and advanced operations"""
        output = simulate_banking_system(self.level2_account_management)
        expected = [
            "created account ACC001 for John Doe with balance $2000.00",
            "created account ACC002 for Jane Smith with balance $1500.00",
            "created account ACC003 for Bob Wilson with balance $3000.00",
            "deposited $500.00 to ACC001, new balance $2500.00",
            "withdrew $200.00 from ACC002, new balance $1300.00",
            "transferred $800.00 from ACC003 to ACC001",
            "froze account ACC002",
            "account inactive",
            "unfroze account ACC002",
            "withdrew $50.00 from ACC002, new balance $1250.00"
        ]
        self.assertEqual(output, expected)

    def test_level3_temporal_operations(self):
        """Test Level 3: Timestamp-based operations"""
        output = simulate_banking_system(self.level3_temporal_operations)
        expected = [
            "created account at ACC001 for Alice Brown with balance $2500.00 at 2024-01-15T09:00:00",
            "created account at ACC002 for Charlie Davis with balance $1800.00 at 2024-01-15T09:30:00",
            "deposited at $300.00 to ACC001, new balance $2800.00",
            "withdrew at $150.00 from ACC002, new balance $1650.00", 
            "transferred at $400.00 from ACC001 to ACC002",
            "balance at $2800.00",  # Balance at 10:15 (after deposit, before transfer)
            "froze account at ACC002",
            "account inactive",
            "unfroze account at ACC002"
        ]
        self.assertEqual(output, expected)

    def test_level3_daily_withdrawal_limits(self):
        """Test Level 3: Daily withdrawal limits (default $5000)"""
        operations = [
            ["CREATE_ACCOUNT", "ACC001", "High Roller", "10000.00"],
            ["WITHDRAW", "ACC001", "3000.00"],  # First withdrawal
            ["WITHDRAW", "ACC001", "1500.00"],  # Second withdrawal (total $4500)
            ["WITHDRAW", "ACC001", "600.00"],   # Should fail - exceeds $5000 daily limit
        ]
        output = simulate_banking_system(operations)
        expected = [
            "created account ACC001 for High Roller with balance $10000.00",
            "withdrew $3000.00 from ACC001, new balance $7000.00",
            "withdrew $1500.00 from ACC001, new balance $5500.00",
            "exceeds daily limit"
        ]
        self.assertEqual(output, expected)

    def test_temporal_consistency(self):
        """Test that operations can't happen before account creation"""
        operations = [
            ["CREATE_ACCOUNT_AT", "2024-01-15T10:00:00", "ACC001", "Time Traveler", "1000.00"],
            ["DEPOSIT_AT", "2024-01-15T09:00:00", "ACC001", "500.00"],  # Before account creation
            ["WITHDRAW_AT", "2024-01-15T11:00:00", "ACC001", "200.00"]   # After account creation
        ]
        output = simulate_banking_system(operations)
        expected = [
            "created account at ACC001 for Time Traveler with balance $1000.00 at 2024-01-15T10:00:00",
            "account not found",  # Operation before account creation
            "withdrew at $200.00 from ACC001, new balance $800.00"
        ]
        self.assertEqual(output, expected)

    def test_balance_at_timestamp(self):
        """Test getting balance at specific timestamps"""
        operations = [
            ["CREATE_ACCOUNT_AT", "2024-01-15T09:00:00", "ACC001", "Timeline User", "1000.00"],
            ["DEPOSIT_AT", "2024-01-15T10:00:00", "ACC001", "500.00"],
            ["WITHDRAW_AT", "2024-01-15T11:00:00", "ACC001", "200.00"],
            ["GET_BALANCE_AT", "2024-01-15T09:30:00", "ACC001"],  # After creation, before deposit
            ["GET_BALANCE_AT", "2024-01-15T10:30:00", "ACC001"],  # After deposit, before withdrawal
            ["GET_BALANCE_AT", "2024-01-15T11:30:00", "ACC001"]   # After all operations
        ]
        output = simulate_banking_system(operations)
        expected = [
            "created account at ACC001 for Timeline User with balance $1000.00 at 2024-01-15T09:00:00",
            "deposited at $500.00 to ACC001, new balance $1500.00",
            "withdrew at $200.00 from ACC001, new balance $1300.00",
            "balance at $1000.00",  # Original balance
            "balance at $1500.00",  # After deposit
            "balance at $1300.00"   # After withdrawal
        ]
        self.assertEqual(output, expected)

    def test_complex_multi_account_scenario(self):
        """Test complex scenario with multiple accounts and operations"""
        operations = [
            ["CREATE_ACCOUNT", "ACC001", "Alice", "5000.00"],
            ["CREATE_ACCOUNT", "ACC002", "Bob", "3000.00"], 
            ["CREATE_ACCOUNT", "ACC003", "Charlie", "2000.00"],
            ["TRANSFER", "ACC001", "ACC002", "1000.00"],
            ["TRANSFER", "ACC002", "ACC003", "500.00"],
            ["FREEZE_ACCOUNT", "ACC003"],
            ["TRANSFER", "ACC001", "ACC003", "200.00"],  # Should fail - ACC003 frozen
            ["UNFREEZE_ACCOUNT", "ACC003"],
            ["TRANSFER", "ACC001", "ACC003", "200.00"],  # Should succeed now
            ["GET_BALANCE", "ACC001"],
            ["GET_BALANCE", "ACC002"],
            ["GET_BALANCE", "ACC003"]
        ]
        output = simulate_banking_system(operations)
        expected = [
            "created account ACC001 for Alice with balance $5000.00",
            "created account ACC002 for Bob with balance $3000.00",
            "created account ACC003 for Charlie with balance $2000.00",
            "transferred $1000.00 from ACC001 to ACC002",  # ACC001: 4000, ACC002: 4000
            "transferred $500.00 from ACC002 to ACC003",   # ACC002: 3500, ACC003: 2500
            "froze account ACC003",
            "account inactive",  # Transfer to frozen account fails
            "unfroze account ACC003",
            "transferred $200.00 from ACC001 to ACC003",   # ACC001: 3800, ACC003: 2700
            "balance $3800.00",  # ACC001 final balance
            "balance $3500.00",  # ACC002 final balance  
            "balance $2700.00"   # ACC003 final balance
        ]
        self.assertEqual(output, expected)

if __name__ == '__main__':
    unittest.main()
