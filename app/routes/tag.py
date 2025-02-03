from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse,JSONResponse
from fastapi.templating import Jinja2Templates
from app.database.setting import SessionLocal
from app.database.table.models import Todo, Tag, Set

router = APIRouter()
db = SessionLocal()
templates = Jinja2Templates(directory="app/templates")

#Tag 取得(個別)
@router.get("/tag/{tag_id}")
async def read_tag(request: Request, tag_id: int):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()

    if not tag:
        return JSONResponse(status_code=404, detail="Tagが見つかりません")

    # Tagに紐づくTodoを取得（Setテーブルを使う）
    related_todos = (
        db.query(Todo)
        .join(Set, Set.todo_id == Todo.id)
        .filter(Set.tag_id == tag_id)
        .all()
    )

    return templates.TemplateResponse("tag.html", {
        "request": request,
        "name": "Taito!",
        "tag": tag,
        "tag_id": tag_id,
        "related_todos": related_todos  # 紐づくToDoリストを渡す
    })

#Tag 削除
@router.delete("/tag/{tag_id}")
def delete_tag(tag_id: int):
    # 指定されたTagを取得
    tag_item = db.query(Tag).filter(Tag.id == tag_id).first()

    if not tag_item:
        return JSONResponse(status_code=404, content={"message": "Tagが見つかりません"})

    # 関連するSetテーブルのレコードを削除
    db.query(Set).filter(Set.tag_id == tag_id).delete()

    # Tag自体を削除
    db.delete(tag_item)
    db.commit()

    return JSONResponse(status_code=200, content={"message": "Tagが削除されました"})

#Tag 更新
@router.put("/tag/{tag_id}")
async def update_tag(tag_id: int, request: Request):
    # JSONで送信されたデータを取得
    data = await request.json()
    tagdesc = data.get("tagdesc")  # 送信されたtagdescを取得

    # tag_idに対応するTagをデータベースから取得
    tag_update = db.query(Tag).filter(Tag.id == tag_id).first()

    if not tag_update:
        return JSONResponse(status_code=404, content={"message": "Tagが見つかりません"})
    
    # tagdescを更新
    tag_update.desc = tagdesc
    db.commit()  # データベースに変更を反映

    # 更新されたtagdescを表示
    print(f"Tag updated to: {tagdesc}")
    
    return JSONResponse(status_code=200, content={"message": "Tagが更新されました"})

#Tag 取得(一覧)
@router.get("/tag")
async def read_tags(request: Request):
    tag_list = db.query(Tag).all()
    todo_list = db.query(Todo).all()   
    set_list = db.query(Set).all   
    db.close()
    
    return templates.TemplateResponse("taglist.html", {
        "request": request,
        "name": "Taito!",
        "todo_list": todo_list,
        "tag_list": tag_list,
        "set_list": set_list
        })

#Tag 作成
@router.post("/tag")
def create_tab(
    box: str = Form(...), 
):
    
    print(f"Tag: {box}")
    
    #tagのレコード作成
    new_record = Tag(desc=box)
    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    print(f"挿入したレコード: {new_record.id}, {new_record.desc}")
    # 追加後にリダイレクトして、最新のTagリストを表示する
    return RedirectResponse(url="/tag", status_code=303)