from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import relation
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
# 環境に合わせて変更すること
DATABASE = 'mysql://%s:%s@%s/%s?charset=utf8' % (
    "docker",
    "docker",
    "localhost",
    "test",
)

# echo=True 実行時にSQLが出力される
ENGINE = create_engine(DATABASE, encoding="utf-8", echo=True)


class User(Base):
    # テーブル名やカラム定義は必須
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    age = Column(Integer)
