from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .database.setting import SessionLocal
from .database.table.models import Todo, Tag
from urllib.parse import urljoin

app = FastAPI(
    title='FastAPIでつくるtoDoアプリケーション',
)
app.mount(path="/app/static", app=StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

db = SessionLocal()

#ルートページ
@app.get("/aaaa", response_class=HTMLResponse)
async def read_root(request: Request):
    items = ("bread","milk","apple")
    return templates.TemplateResponse("index.html", {
        "request": request,
        "name": "Taito!",
        "items": items
        })

#テスト
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    tag_list = db.query(Tag).all()
    todo_list = db.query(Todo).all()      
    db.close()
    
    return templates.TemplateResponse("todolist_get.html", {
        "request": request,
        "name": "Taito!",
        "todo_list": todo_list,
        "tag_list": tag_list
        })

#Todo 取得(一覧)
@app.get("/todo")
def read_todolist():
    return

#Todo 取得(個別)
@app.get("/todo/{todo_id}", response_class=HTMLResponse)
async def read_todo(request: Request, todo_id):
  todo = db.query(Todo).filter(Todo.id == todo_id).first()


  return templates.TemplateResponse("todo_get.html", {
        "request": request,
        "name": "Taito!",
        "todo_list": todo.box
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

