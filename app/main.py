from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .database.setting import SessionLocal
from .database.table.models import Todo

app = FastAPI(
    title='FastAPIでつくるtoDoアプリケーション',
)
app.mount(path="/app/static", app=StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

#ルートページ
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "name": "Taito!"
        })

#test（データ取得確認）
@app.get("/test")
def test_res():
    db = SessionLocal()
    todo = db.query(Todo).filter(Todo.id == "1").first()
    db.close()
    return {f"読み込んだレコード: {todo.id}, {todo.box}, {todo.date}, {todo.done}"}

#Todo 取得(一覧)
@app.get("/todo")
def read_todos():
    return

#Todo 取得(個別)
@app.get("/todo/{todo_id}", response_class=HTMLResponse)
def read_todo(todo_id: str, request: Request):
    db = SessionLocal()
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    print(f"読み込んだレコード: {todo.id}, {todo.box}, {todo.date}, {todo.done}")
    return templates.TemplateResponse("index.html", {
            "request": request,
            "name": {f"読み込んだレコード: {todo.id}, {todo.box}, {todo.date}, {todo.done}"}
            })

#Todo 作成
@app.post("/todo")
def create_todo():
    return

#Todo 更新
@app.put("/todo/{todo_id}")
def update_todo():
    return

#Todo 削除
@app.delete("/todo/{todo_id}")
def delete_todo():
    return

#Tag 取得(一覧)
@app.get("/tag")
def read_tags():
    return

#Tag 取得(個別)
@app.get("/tag/{tag_id}")
def read_tag():
    return

#Tag 作成
@app.post("/tag")
def create_tag():
    return

#Tag 更新
@app.put("/tag/{tag_id}")
def update_tag():
    return

#Tag 削除
@app.delete("/tag/{tag_id}")
def delete_tag():
    return

