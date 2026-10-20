import pytest
from fastapi.testclient import TestClient

from api import app
from dependencies import get_repository


class FakeExpenseRepository:
    def __init__(self, expenses=None, category_ids=(1, 2)):
        self.expenses = list(expenses or [])
        self.category_ids = set(category_ids)

    def list_expenses(self):
        return sorted(self.expenses, key=lambda e: e["id"])

    def get_expense(self, expense_id):
        for expense in self.expenses:
            if expense["id"] == expense_id:
                return expense
        return None

    def category_exists(self, category_id):
        return category_id in self.category_ids

    def create_expense(self, expense):
        new_id = max((e["id"] for e in self.expenses), default=0) + 1
        self.expenses.append({
            "id": new_id,
            "description": expense.description,
            "amount": expense.amount,
            "category_id": expense.category_id,
            "spent_at": expense.spent_at,
        })
        return new_id


@pytest.fixture
def api_client():
    repo = FakeExpenseRepository(expenses=[
        {"id": 1, "description": "Кофе", "amount": "150.00",
         "category_id": 1, "spent_at": "2026-10-20"},
    ])
    app.dependency_overrides[get_repository] = lambda: repo
    client = TestClient(app)
    yield client, repo
    app.dependency_overrides.clear()


def test_health(api_client):
    client, repo = api_client
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_empty_list(api_client):
    client, repo = api_client
    repo.expenses.clear()
    response = client.get("/expenses")
    assert response.status_code == 200
    assert response.json() == []


VALID = {"description": "Такси", "amount": "500.00",
         "category_id": 1, "spent_at": "2026-10-20"}


def test_list_expenses_fields(api_client):
    client, repo = api_client
    response = client.get("/expenses")
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "description": "Кофе", "amount": "150.00",
         "category_id": 1, "spent_at": "2026-10-20"}
    ]


def test_get_expense_by_id(api_client):
    client, repo = api_client
    response = client.get("/expenses/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["description"] == "Кофе"


def test_get_expense_not_found(api_client):
    client, repo = api_client
    response = client.get("/expenses/999")
    assert response.status_code == 404
    assert "detail" in response.json()


@pytest.mark.parametrize("bad_id", ["abc", "0", "-1"])
def test_get_expense_bad_id(api_client, bad_id):
    client, repo = api_client
    response = client.get(f"/expenses/{bad_id}")
    assert response.status_code == 422


def test_create_expense(api_client):
    client, repo = api_client
    response = client.post("/expenses", json=VALID)
    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 2
    assert body["description"] == "Такси"
    assert body["amount"] == "500.00"
    assert len(repo.expenses) == 2


@pytest.mark.parametrize("bad_amount", ["-5", "0", "abc", "10.555"])
def test_create_expense_bad_amount(api_client, bad_amount):
    client, repo = api_client
    response = client.post("/expenses", json={**VALID, "amount": bad_amount})
    assert response.status_code == 422


@pytest.mark.parametrize("bad_description", ["", "   "])
def test_create_expense_bad_description(api_client, bad_description):
    client, repo = api_client
    response = client.post("/expenses", json={**VALID, "description": bad_description})
    assert response.status_code == 422


@pytest.mark.parametrize("bad_date", ["2026-13-45", "not a date"])
def test_create_expense_bad_date(api_client, bad_date):
    client, repo = api_client
    response = client.post("/expenses", json={**VALID, "spent_at": bad_date})
    assert response.status_code == 422


def test_create_expense_unknown_category(api_client):
    client, repo = api_client
    response = client.post("/expenses", json={**VALID, "category_id": 999})
    assert response.status_code == 404
    assert len(repo.expenses) == 1


@pytest.mark.parametrize("missing_field", ["description", "amount", "category_id", "spent_at"])
def test_create_expense_missing_field(api_client, missing_field):
    client, repo = api_client
    body = {key: value for key, value in VALID.items() if key != missing_field}
    response = client.post("/expenses", json=body)
    assert response.status_code == 422


def test_create_expense_extra_field(api_client):
    client, repo = api_client
    response = client.post("/expenses", json={**VALID, "id": 5})
    assert response.status_code == 422