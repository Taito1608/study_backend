from app.database.setting import SessionLocal
from app.database.table.models import Todo

def read_test():
    db = SessionLocal()
    todo = db.query(Todo).filter(Todo.id == "1").first()
    db.close()
    todo_list = [todo.id,todo.box, todo.date, todo.done]
    
    print ("読み込んだレコード:" ,todo.id,todo.box, todo.date, todo.done)
    print(todo_list)
    
    for item in todo_list:
        print(item)

if __name__ == "__main__":
    read_test()