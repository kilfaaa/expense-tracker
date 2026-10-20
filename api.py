from typing import Annotated

from fastapi import FastAPI, HTTPException, Path

from dependencies import RepositoryDep
from models import Expense
from schemas import ExpenseCreate, ExpenseRead

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/expenses", response_model=list[ExpenseRead])
def list_expenses(repo: RepositoryDep):
    return repo.list_expenses()


@app.get("/expenses/{expense_id}", response_model=ExpenseRead)
def get_expense(expense_id: Annotated[int, Path(gt=0)], repo: RepositoryDep):
    expense = repo.get_expense(expense_id)
    if expense is None:
        raise HTTPException(status_code=404, detail="Расход не найден.")
    return expense


@app.post("/expenses", response_model=ExpenseRead, status_code=201)
def create_expense(data: ExpenseCreate, repo: RepositoryDep):
    if not repo.category_exists(data.category_id):
        raise HTTPException(status_code=404, detail="Категория не найдена.")
    new_id = repo.create_expense(Expense(**data.model_dump()))
    return ExpenseRead(id=new_id, **data.model_dump())