from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.base import BaseHTTPMiddleware
from .routes import todo, tag
from .database.setting import SessionLocal

app = FastAPI(
    title='FastAPIでつくるtoDoアプリケーション',
)

# ミドルウェアでキャッシュ制御を設定
class CacheControlMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        if response.headers.get("content-type", "").startswith("text/html"):
            # HTMLのキャッシュを無効化
            response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        return response

# ミドルウェアを追加
app.add_middleware(CacheControlMiddleware)

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

# error画面
@app.get("/error/{id}")
async def error_page(request: Request, id: str):
    return templates.TemplateResponse("error.html", {
        "request": request,
        "massage": id
    })

# 404エラーのリダイレクト設定
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return RedirectResponse(url="/error")

# ルート登録（ルーティング）
app.include_router(todo.router)
app.include_router(tag.router)