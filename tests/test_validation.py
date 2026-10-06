import datetime

import pytest
from decimal import Decimal
from validation import validate_amount, validate_date, validate_id, validate_category_name, validate_description


def test_validate_amount():
    assert validate_amount("150.50") == Decimal("150.50")

def test_validate_amount_accepts_comma():
    assert validate_amount("150,50") == Decimal("150.50")


@pytest.mark.parametrize("bad_amount", ["hello", "0", "-10"])
def test_validate_amount_raises_on_text(bad_amount):
    with pytest.raises(ValueError):
        validate_amount(bad_amount)


def test_validate_date():
    assert validate_date("2020-03-31") == datetime.date(2020, 3, 31)

def test_validate_bad_date():
    with pytest.raises(ValueError):
        validate_date("32-13-2020")


def test_validate_id():
    assert validate_id("11") == 11

def test_validate_str_id():
    with pytest.raises(ValueError):
        validate_id("Одиннадцать")


def test_validate_category_name():
    assert validate_category_name("Транспорт") == "Транспорт"

def test_validate_empy_category_name():
    with pytest.raises(ValueError):
        validate_category_name("")

def test_validate_description():
    assert validate_description("Проезд") == "Проезд"

def test_validate_empty_description():
    with pytest.raises(ValueError):
        validate_description("")