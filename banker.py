import sys
parentPath='c:/Users/ajcltm/PycharmProjects/signalProcessor' # parent 경로
sys.path.append(parentPath) # 경로 추가
import account
import transactionModels as tm

class Banker :

    def create_account(self) -> None:
        self.account = account.Account()

    def register(self, date, amounts, name='kim'):
        self.account.cash_transaction.append(tm.cash_transaction(date=date, offer=name, amounts=amounts))
        self.compute()

    def compute(self):
        self.account.cash=0
        for i in self.account.cash_transaction:
            if i.amounts >= 0:
                self.account.deposit(abs(i.amounts))
            else :
                self.account.withdraw(abs(i.amounts))