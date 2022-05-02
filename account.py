class Back :
    transaction = []

    def __init__(self, account):
        self.account = account

    def register(self, name, amount):
        self.transaction.append((name, amount))

    def compute(self):

        for i in self.transaction:
            if i[1] >= 0:
                self.account.deposit


class Account:

    def __init__(self) -> None:
        self.cash = 0
        self.transaction = []

    def deposit(self, amount:int):
        self.cash += amount
    
    def withdraw(self, amount:int):
        if amount > self.cash:
            raise ValueError("Insufficient funds")
        self.cash