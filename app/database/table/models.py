from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database.setting import Engine
from app.database.setting import Base

class Todo(Base):
    __tablename__ = 'todo'
    __table_args__ = {
        'comment': 'todoの内容を管理するテーブル'
    }

    id   = Column('todo_id', Integer, primary_key=True, autoincrement=True)
    box  = Column('box', String(200), nullable=False)
    date = Column('date', DateTime, default=datetime.now, nullable=False)  # 現在時刻をデフォルトに設定
    completed = Column('completed', Boolean, default=False)
    settings = relationship("Set", back_populates="todo")

class Tag(Base):
    __tablename__ = 'tag'
    __table_args__ = {
        'comment': 'tagの内容を管理するテーブル'
    }

    id   = Column('tag_id', Integer, primary_key=True, autoincrement=True)
    desc = Column('description', String(200), nullable=False)
    settings = relationship("Set", back_populates="tag")

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