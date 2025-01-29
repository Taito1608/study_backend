from app.database.setting import SessionLocal
from app.database.table.models import Todo

def delete_test():
    db = SessionLocal()
    todo = db.query(Todo).filter(Todo.id == "2").delete()
    db.commit()
    
if __name__ == "__main__":
    delete_test()

    