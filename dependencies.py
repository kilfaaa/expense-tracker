import os
from typing import Annotated

import psycopg
from fastapi import Depends

from repository import ExpenseRepository


def get_repository():
    conn = psycopg.connect(os.environ["DATABASE_URL"])
    try:
        yield ExpenseRepository(conn)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


RepositoryDep = Annotated[ExpenseRepository, Depends(get_repository)]