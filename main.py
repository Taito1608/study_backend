from fastapi import FastAPI, Header
from typing import Union

app = FastAPI()

@app.get("/sample/")
def read_sample(authorization: Union[str, None] = Header(default=None)):
    print(authorization)
    return {"message": "ヘッダー情報を取得しました"}