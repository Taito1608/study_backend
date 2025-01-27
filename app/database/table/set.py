from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.database.setting import Engine
from app.database.setting import Base
from app.database.table import Todo
from app.database.table.tag import Tag


class Set(Base):

    __tablename__ = 'set'
    __table_args__ = {
        'comment': 'todoとtagの関連を設定するテーブル'
    }

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    todo_id = Column(Integer, ForeignKey('todo.todo_id'), nullable=False)
    tag_id = Column(Integer, ForeignKey('tag.tag_id'), nullable=False)

    todo = relationship("Todo", back_populates="settings")
    tag = relationship("Tag", back_populates="settings")