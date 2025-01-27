from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .database.setting import SessionLocal
from .database.table.models import Todo

app = FastAPI()
app.mount(path="/app/static", app=StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/todo/{todo_id}")
def read_todo(todo_id: str):
    db = SessionLocal()
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    print(f"読み込んだレコード: {todo.id}, {todo.box}, {todo.date}, {todo.done}")
    return {f"読み込んだレコード: {todo.id}, {todo.box}, {todo.date}, {todo.done}"}

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": "Hello, FastAPI!"})


