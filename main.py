from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union

app = FastAPI()

#C言語でいう構造体のようなもの
class Item(BaseModel):
    name: str
    price: float
    description: Union[str, None] = None    #Unionは複数の型を宣言することができる

@app.post("/items/")
def create_item(item: Item):
    print(f"データを登録します： {item.name}, {item.price}, {item.description}")
    return item