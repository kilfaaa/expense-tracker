from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ExpenseCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    description: str
    amount: Decimal = Field(gt=0, decimal_places=2)
    category_id: int = Field(gt=0)
    spent_at: date

    @field_validator("description")
    @classmethod
    def clean_description(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Описание не может быть пустым.")
        return value


class ExpenseRead(ExpenseCreate):
    id: int = Field(gt=0)