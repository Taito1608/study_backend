from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union
from typing import Annotated    #クエリパラメータの最小値と最大値を設定するため（大量のデータを一度に取得しようとするとサービスの遅延に繋がるため）
from .database.setting import SessionLocal
from .database.table.models import Todo

from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/todo/{todo_id}")
def read_todo(todo_id: str):
    db = SessionLocal()
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    print(f"読み込んだレコード: {todo.id}, {todo.box}, {todo.date}, {todo.done}")
    return {f"読み込んだレコード: {todo.id}, {todo.box}, {todo.date}, {todo.done}"}


