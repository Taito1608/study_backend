from app.database.setting import Engine, Base
from app.database.table.todo import Todo

# テーブルを作成
def create_tables():
    Base.metadata.create_all(bind=Engine)

if __name__ == "__main__":
    create_tables()
    print("テーブルを作成しました！")