from sqlalchemy import Column, Integer, String, Boolean

from app.database.setting import Engine
from app.database.setting import Base


class Todo(Base):

    __tablename__ = 'todo'
    __table_args__ = {
        'comment': 'todoの内容を管理するテーブル'
    }

    num_todo = Column('num_todo', Integer, primary_key=True, autoincrement=True)
    box =  Column('box', String(200), nullable=False)
    date = Column('date', Integer)
    done = Column('done', Boolean, default=False)