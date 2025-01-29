from app.database.setting import SessionLocal
from app.database.table.models import Todo

def update_test():
    db = SessionLocal()
    update = db.query(Todo).filter(Todo.id == "3").first()
    update.id = "1"
    db.commit()

if __name__ == "__main__":
    update_test()