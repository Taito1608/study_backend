from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse,RedirectResponse,JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .database.setting import SessionLocal
from .database.table.models import Todo, Tag, Set
from urllib.parse import urljoin

app = FastAPI(
    title='FastAPIでつくるtoDoアプリケーション',
)
app.mount(path="/app/static", app=StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

db = SessionLocal()

#ルートページ
@app.get("/", response_class=HTMLResponse)
async def root_page(request: Request):
    return templates.TemplateResponse("root.html", {
        "request": request,
        "name": "Taito!",
        })

#Todo 取得(一覧)
@app.get("/todo")
async def read_todolist(request: Request):
    tag_list = db.query(Tag).all()
    todo_list = db.query(Todo).all()   
    set_list = db.query(Set).all   
    db.close()
    
    return templates.TemplateResponse("todolist_get.html", {
        "request": request,
        "name": "Taito!",
        "todo_list": todo_list,
        "tag_list": tag_list,
        "set_list": set_list
        })

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
def create_todo(
    box: str = Form(...), 
    tag_id: int = Form(...)
):
    
    print(f"ToDo: {box}, タグID: {tag_id}")
    
    #todoのレコード作成
    new_record = Todo(box=box, completed=False)
    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    #Setのレコード作成
    new_set = Set(todo_id=new_record.id, tag_id=tag_id)
    db.add(new_set)
    db.commit()
    db.refresh(new_set)
    print(f"挿入したレコード: {new_record.id}, {new_record.box}, {new_record.date}, {new_record.completed}")
    print(f"SETに挿入したレコード: {new_set.id}, {new_set.todo}, {new_set.tag}")
    # 追加後にリダイレクトして、最新のToDoリストを表示する
    return RedirectResponse(url="/todo", status_code=303)

#Todo 更新
@app.put("/todo/{todo_id}")
def update_todo():
    return

#Todo 削除
@app.delete("/todo/{todo_id}")
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
    

#Tag 取得(一覧)
@app.get("/tag")
async def read_tags(request: Request):
    tag_list = db.query(Tag).all()
    todo_list = db.query(Todo).all()   
    set_list = db.query(Set).all   
    db.close()
    
    return templates.TemplateResponse("taglist_get.html", {
        "request": request,
        "name": "Taito!",
        "todo_list": todo_list,
        "tag_list": tag_list,
        "set_list": set_list
        })

#Tag 取得(個別)
@app.get("/tag/{tag_id}")
async def read_tag(request: Request, tag_id):
  tag = db.query(Tag).filter(Tag.id == tag_id).first()


  return templates.TemplateResponse("tag_get.html", {
        "request": request,
        "name": "Taito!",
        "tag_list": tag.desc
        })

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