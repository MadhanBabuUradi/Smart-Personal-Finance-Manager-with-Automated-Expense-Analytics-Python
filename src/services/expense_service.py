import pandas as pd

class ExpenseService:
    def __init__(self, df):
        self.df = df.copy()

    def add_expense(self, date, description, category, amount):
        new = {'date': date, 'description': description, 'category': category, 'amount': amount}
        self.df = pd.concat([self.df, pd.DataFrame([new])], ignore_index=True)
        return self.df

    def update_expense(self, idx, **kwargs):
        for k,v in kwargs.items():
            if k in self.df.columns:
                self.df.at[idx,k] = v
        return self.df

    def delete_expense(self, idx):
        self.df = self.df.drop(index=idx).reset_index(drop=True)
        return self.df

    def get_transactions(self):
        return self.df.copy()
