from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import date

from app.database.setting import Engine
from app.database.setting import Base

class Todo(Base):
    __tablename__ = 'todo'
    __table_args__ = {
        'comment': 'todoの内容を管理するテーブル'
    }

    id   = Column('todo_id', Integer, primary_key=True, autoincrement=True)
    box  = Column('box', String(200), nullable=False)
    date = Column('date', Date, nullable=True)  # 現在時刻をデフォルトに設定
    completed = Column('completed', Boolean, default=False)
    settings = relationship("Set", back_populates="todo", cascade="all, delete-orphan")

class Tag(Base):
    __tablename__ = 'tag'
    __table_args__ = {
        'comment': 'tagの内容を管理するテーブル'
    }

    id   = Column('tag_id', Integer, primary_key=True, autoincrement=True)
    desc = Column('description', String(200), nullable=False)
    settings = relationship("Set", back_populates="tag", cascade="all, delete-orphan")

class Set(Base):
    __tablename__ = 'set'
    __table_args__ = {
        'comment': 'todoとtagの関連を設定するテーブル'
    }

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    todo_id = Column(Integer, ForeignKey('todo.todo_id', ondelete='CASCADE'), nullable=False)
    tag_id = Column(Integer, ForeignKey('tag.tag_id', ondelete='CASCADE'), nullable=False)

    todo = relationship("Todo", back_populates="settings")
    tag = relationship("Tag", back_populates="settings")