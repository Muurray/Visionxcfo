from forex_python.converter import CurrencyRates
from forex_python.bitcoin import BtcConverter
import json

class MultiCurrencyManager:
    def __init__(self):
        self.currency_rates = CurrencyRates()
        self.btc_converter = BtcConverter()
        self.accounts = {}

    def create_account(self, account_name, currency_type, balance):
        """Create a new account with a specific currency and balance."""
        if currency_type not in ['USD', 'EUR', 'BTC', 'ETH']:
            raise ValueError("Unsupported currency type")
        self.accounts[account_name] = {
            'currency': currency_type,
            'balance': balance
        }

    def get_balance(self, account_name):
        """Get the balance of an account."""
        if account_name not in self.accounts:
            raise ValueError("Account not found")
        return self.accounts[account_name]['balance']

    def convert_currency(self, amount, from_currency, to_currency):
        """Convert an amount from one currency to another."""
        if from_currency == to_currency:
            return amount

        if from_currency in ['BTC', 'ETH'] or to_currency in ['BTC', 'ETH']:
            if from_currency == 'BTC':
                amount_in_usd = self.btc_converter.get_latest_price('USD') * amount
            elif from_currency == 'ETH':
                amount_in_usd = self.btc_converter.get_latest_price('USD') * amount
            else:
                amount_in_usd = self.currency_rates.convert(from_currency, 'USD', amount)
            
            if to_currency == 'BTC':
                return amount_in_usd / self.btc_converter.get_latest_price('USD')
            elif to_currency == 'ETH':
                return amount_in_usd / self.btc_converter.get_latest_price('USD')
            else:
                return self.currency_rates.convert('USD', to_currency, amount_in_usd)

        return self.currency_rates.convert(from_currency, to_currency, amount)

    def add_transaction(self, from_account, to_account, amount):
        """Perform a transaction between two accounts."""
        if from_account not in self.accounts or to_account not in self.accounts:
            raise ValueError("One or both accounts not found")
        
        from_balance = self.accounts[from_account]['balance']
        if from_balance < amount:
            raise ValueError("Insufficient funds")

        converted_amount = self.convert_currency(amount, self.accounts[from_account]['currency'], self.accounts[to_account]['currency'])
        
        self.accounts[from_account]['balance'] -= amount
        self.accounts[to_account]['balance'] += converted_amount

    def get_accounts(self):
        """Get a list of all accounts."""
        return json.dumps(self.accounts, indent=4)

# Example Usage
if __name__ == "__main__":
    manager = MultiCurrencyManager()
    
    # Create accounts
    manager.create_account("Account1", "USD", 1000)
    manager.create_account("Account2", "BTC", 0.1)
    
    # Print account details
    print("Accounts before transaction:")
    print(manager.get_accounts())
    
    # Perform a transaction
    manager.add_transaction("Account1", "Account2", 100)
    
    # Print account details after transaction
    print("\nAccounts after transaction:")
    print(manager.get_accounts())
