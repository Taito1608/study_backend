from app.database.setting import Engine, Base
from app.database.table.models import Set, Tag, Todo

# 一度に全てのテーブルを作成できるようにする
def create_tables():
    Base.metadata.create_all(bind=Engine)

if __name__ == "__main__":
    create_tables()
    print("テーブルを作成しました！")