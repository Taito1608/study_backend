from fastapi import FastAPI


app = FastAPI()

#Getリクエストのパスパラメータを取得する
@app.get("/items/{item_id}")
def read_root(item_id: int):
    return {"massage": item_id}