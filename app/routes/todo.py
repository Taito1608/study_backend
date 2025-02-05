from fastapi import APIRouter, Request,Query
from fastapi.responses import HTMLResponse,RedirectResponse,JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from app.database.setting import SessionLocal
from app.database.table.models import Todo, Tag, Set
from typing import List
from datetime import datetime

router = APIRouter()
db = SessionLocal()
templates = Jinja2Templates(directory="app/templates")

# JSON形式のリクエストボディ用のPydanticモデル
class TodoRequest(BaseModel):
    box: str
    tag: List[int] = []  # タグはリスト（デフォルトは空リスト）

@router.get("/api/todos")
async def get_todos(
    skip: int = Query(0), 
    limit: int = Query(100), 
    completed: bool = Query(False)):
    db = SessionLocal()

    # ToDoリストを取得
    todos = db.query(Todo).filter(Todo.completed == completed).offset(skip).limit(limit).all()

    # ToDoごとのタグ情報を取得
    todo_list = []
    for todo in todos:
        tags = db.query(Tag.desc).join(Set, Set.tag_id == Tag.id).filter(Set.todo_id == todo.id).all()
        tag_descs = [tag.desc for tag in tags]

        todo_list.append({
            "id": todo.id,
            "box": todo.box,
            "date": todo.date.isoformat() if todo.date else None,
            "completed": todo.completed,
            "tags": tag_descs
        })

    return todo_list

# Todo 取得(一覧)
@router.get("/todo")
async def read_todolist(
    request: Request,
    skip: int = Query(0),
    limit: int = Query(100),
    completed: bool = Query(False)
):
    if limit <0 or skip < 0:
        return RedirectResponse(url="/error/todo")

    # タグのリストを取得
    tag_list = db.query(Tag).all()

    return templates.TemplateResponse("todolist.html", {
        "request": request,
        "name": "Taito!",
        "tag_list": tag_list,
    })

#Todo 取得(個別)
@router.get("/todo/{todo_id}", response_class=HTMLResponse)
async def read_todo(request: Request, todo_id: int):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        return RedirectResponse(url="/error/todo")

    tag_list = db.query(Tag).all()  # 全タグリスト（選択用）
    
    # ToDo に紐づくタグを取得
    todo_tags = db.query(Tag).join(Set).filter(Set.todo_id == todo_id).all()

    return templates.TemplateResponse("todo.html", {
        "request": request,
        "name": "Taito!",
        "todo": todo,
        "tag_list": tag_list,  # 全タグ（選択肢）
        "todo_tags": todo_tags  # 紐づくタグ（表示用）
    })

#Todo 作成
@router.post("/todo")
async def create_todo(
    todo_data: TodoRequest
):
    print(f"ToDo: {todo_data.box}, タグID: {todo_data.tag}")

    # ToDo のレコード作成
    new_record = Todo(box=todo_data.box, completed=False)
    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    # Setのレコード作成（複数のtag_idを登録）
    if todo_data.tag:
        for tag_id in todo_data.tag:
            new_set = Set(todo_id=new_record.id, tag_id=tag_id)
            db.add(new_set)
            print(f"関連付けられたタグ: {tag_id}")

        db.commit()

    print(f"挿入したToDoレコード: {new_record.id}, {new_record.box}, {new_record.completed}")
    
    return JSONResponse(content={"message": "ToDo追加成功", "todo_id": new_record.id})

#Todo 更新
@router.put("/todo/{todo_id}")
async def update_todo(todo_id: int, request:Request):
    data = await request.json()
    #それぞれのデータを取り出す
    todobox = data.get("todobox")    
    todocomp = data.get("todocomp")  
    tag_ids = data.get("tag_ids", [])
    #data.get("tag_id") 

    date_str = data.get("tododate")
    if date_str:
        # 日付文字列をdatetimeオブジェクトに変換
        tododate = datetime.strptime(date_str, "%Y-%m-%d").date()  # "%Y-%m-%d"形式の文字列をdatetime.dateに変換
    else:
        tododate = None

    todo_update = db.query(Todo).filter(Todo.id == todo_id).first()
    #Tagの重複を避けるために現在のタグを削除
    db.query(Set).filter(Set.todo_id == todo_id).delete()

    #Tagの追加
    if tag_ids:
        for tag_set in tag_ids:
            new_set = Set(todo_id=todo_update.id, tag_id=tag_set)
            db.add(new_set)
            print(f"関連付けられたタグ: {tag_set}")

    if not todo_update:
        return RedirectResponse(url="/error/todo")
    
    todo_update.box = todobox
    todo_update.date = tododate
    todo_update.completed = todocomp

    db.commit()

    # 取り出したデータを表示
    print(f"ToDo: {todobox}, 日付: {tododate}, 完了: {todocomp}")
    return JSONResponse(status_code=200, content={"message": "ToDoが更新されました"})

#Todo 削除
@router.delete("/todo/{todo_id}")
def delete_todo(todo_id: int):
    # 指定されたToDoを取得
    todo_item = db.query(Todo).filter(Todo.id == todo_id).first()
    
    if not todo_item:
        return RedirectResponse(url="/error/todo")

    # 関連するSetテーブルのレコードを削除
    db.query(Set).filter(Set.todo_id == todo_id).delete()
    
    # Todo自体を削除
    db.delete(todo_item)
    db.commit()

    return JSONResponse(status_code=200, content={"message": "ToDoが削除されました"})