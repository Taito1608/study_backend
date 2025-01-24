from typing import Union
from typing import Annotated    #クエリパラメータの最小値と最大値を設定するため（大量のデータを一度に取得しようとするとサービスの遅延に繋がるため）

from fastapi import FastAPI, Query

#クエリパラメータはクライアントからの要求状況をリクエストに含めるために使用する
app = FastAPI()
items = ["item1", "item2", "item3", "item4"]

@app.get("/items")
def read_item(skip: int = 0, limit: Annotated[int, Query(ge=1, le=10)] = 10):   #引数の型とデフォルト引数、クエリパラメータの最小値と最大値を設定する。
    return {"items": items[skip: skip + limit]}