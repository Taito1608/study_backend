from app.database.setting import SessionLocal
from app.database.table.models import Todo

def read_test():
    db = SessionLocal()
    records = db.query(Todo).all()
    for record in records:
        print(f"読み込んだレコード: {record.id}, {record.box}, {record.date}, {record.done}")

if __name__ == "__main__":
    read_test()