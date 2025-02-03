from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse,RedirectResponse,JSONResponse
from fastapi.templating import Jinja2Templates
from app.database.setting import SessionLocal
from app.database.table.models import Todo, Tag, Set
from typing import List
from datetime import datetime

router = APIRouter()
db = SessionLocal()
templates = Jinja2Templates(directory="app/templates")

#Todo 削除
@router.delete("/todo/{todo_id}")
def delete_todo(todo_id: int):
    # 指定されたToDoを取得
    todo_item = db.query(Todo).filter(Todo.id == todo_id).first()
    
    if not todo_item:
        return JSONResponse(status_code=404, content={"message": "ToDoが見つかりません"})

    # 関連するSetテーブルのレコードを削除
    db.query(Set).filter(Set.todo_id == todo_id).delete()
    
    # Todo自体を削除
    db.delete(todo_item)
    db.commit()

    return JSONResponse(status_code=200, content={"message": "ToDoが削除されました"})

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
        return JSONResponse(status_code=404, content={"message": "ToDoが見つかりません"})
    
    todo_update.box = todobox
    todo_update.date = tododate
    todo_update.completed = todocomp

    db.commit()

    # 取り出したデータを表示
    print(f"ToDo: {todobox}, 日付: {tododate}, 完了: {todocomp}")
    return JSONResponse(status_code=200, content={"message": "ToDoが更新されました"})

#Todo 作成
@router.post("/todo")
async def create_todo(
    box: str = Form(...), 
    tag: List[int] = Form(...),  # 複数タグ対応
):
    print(f"ToDo: {box}, タグID: {tag}")
    
    # ToDo のレコード作成
    new_record = Todo(box=box, completed=False)
    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    # Setのレコード作成（複数のtag_idを登録）
    if tag:  # tag_idが空でないことを確認
        for tag_id in tag:
            new_set = Set(todo_id=new_record.id, tag_id=tag_id)
            db.add(new_set)
            print(f"関連付けられたタグ: {tag_id}")

        # コミットはループ外で一括して行う
        db.commit()

    print(f"挿入したToDoレコード: {new_record.id}, {new_record.box}, {new_record.completed}")
    
    # リダイレクトして最新のToDoリストを表示
    return RedirectResponse(url="/todo", status_code=303)

#Todo 取得(個別)
@router.get("/todo/{todo_id}", response_class=HTMLResponse)
async def read_todo(request: Request, todo_id: int):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        return JSONResponse(status_code=404, detail="ToDoが見つかりません")

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

#Todo 取得(一覧)
@router.get("/todo")
async def read_todolist(request: Request):
    # タグとToDoのリストを取得
    tag_list = db.query(Tag).all()
    todo_list = db.query(Todo).all()

    # set_tagリストを各Todoに関連するTag.descを格納
    todo_list_with_tags = []
    for todo in todo_list:
        # Todoに関連するTag.descを取得
        set_tags = (
            db.query(Tag.desc)
            .join(Set, Set.tag_id == Tag.id)
            .filter(Set.todo_id == todo.id)
            .all()
        )
        tag_descs = [set_tag.desc for set_tag in set_tags]
        
        # 取得したTag.descをセット
        todo_list_with_tags.append({
            "todo": todo,
            "set_tag_descs": tag_descs
        })
    
    db.close()

    return templates.TemplateResponse("todolist.html", {
        "request": request,
        "name": "Taito!",
        "todo_list": todo_list_with_tags,
        "tag_list": tag_list,
    })