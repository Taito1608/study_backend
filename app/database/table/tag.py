from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.setting import Engine
from app.database.setting import Base
from app.database.table.set import Set



class Tag(Base):

    __tablename__ = 'tag'
    __table_args__ = {
        'comment': 'tagの内容を管理するテーブル'
    }

    id   = Column('tag_id', Integer, primary_key=True, autoincrement=True)
    desc = Column('description', String(200), nullable=False)
    settings = relationship("Set", back_populates="tag")
