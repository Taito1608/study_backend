from database.setting import SessionLocal
from database.table.models import Todo

def create_test():
    db = SessionLocal()
    new_record = Todo(box="Hello, World!", date="2025-01-27", done=False)
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    print(f"挿入したレコード: {new_record.id}, {new_record.box}, {new_record.date}, {new_record.done}")

if __name__ == "__main__":
    create_test()