class Wallet:
    def __init__(self, address=None, balance=None, stake_value=None):
        self.address = address
        self.start_balance = balance
        self.balance = balance
        self.stake_value = stake_value

    def send_transaction(self, transaction_fee):
        if self.balance <= self.stake_value:
            print('[ERROR] Not enough balance to send this transaction')
            return False

        self.balance -= transaction_fee
        return True

    def lock_stake(self, stake_value):
        if stake_value >= self.balance:
            print('[ERROR] Not enough balance to stake')
            return False
        self.stake_value = stake_value
        return True
