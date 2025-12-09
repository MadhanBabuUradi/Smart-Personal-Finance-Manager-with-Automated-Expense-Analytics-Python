from dataclasses import dataclass
from datetime import datetime

@dataclass
class Expense:
    date: datetime
    description: str
    category: str
    amount: float

    @staticmethod
    def from_dict(d):
        return Expense(
            date = datetime.strptime(d['date'], '%Y-%m-%d'),
            description = d.get('description',''),
            category = d.get('category','Uncategorized'),
            amount = float(d.get('amount',0))
        )
