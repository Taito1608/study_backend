from sqlalchemy import Column, Integer, String, Boolean, Date
from sqlalchemy.orm import relationship

from app.database.setting import Engine
from app.database.setting import Base
from app.database.table import Set


class Todo(Base):

    __tablename__ = 'todo'
    __table_args__ = {
        'comment': 'todoの内容を管理するテーブル'
    }

    id   = Column('todo_id', Integer, primary_key=True, autoincrement=True)
    box  = Column('box', String(200), nullable=False)
    date = Column('date', Date, nullable=False)
    done = Column('done', Boolean, default=False)
    settings = relationship("Set", back_populates="todo")