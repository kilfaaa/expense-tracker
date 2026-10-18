from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/items/{item_id}")
def read_item(item_id: Annotated[int, Path(gt=0)]):
    return {"item_id": item_id}

