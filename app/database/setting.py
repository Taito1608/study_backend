from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 接続先DBの設定
DATABASE_URL = "sqlite:///./todo.db"  

# Engine の作成
Engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
  )

# Sessionの作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)

# modelで使用する
Base = declarative_base()