from dataclasses import dataclass
from decimal import Decimal
from datetime import date

@dataclass
class Expense:
    description: str
    amount: Decimal
    category_id: int
    spent_at: date
    id: int | None = None
