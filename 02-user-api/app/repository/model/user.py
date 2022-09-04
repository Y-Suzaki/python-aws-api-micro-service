import os
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import relation
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# 環境に合わせて変更すること
# host = os.environ.get('RDS_WRITER_ENDPOINT', 'localhost')
host = os.environ.get('RDS_PROXY_WRITER_ENDPOINT', 'localhost')
user = os.environ.get('RDS_USER', 'admin')
password = os.environ.get('RDS_PASSWORD', '')

DATABASE = 'mysql+pymysql://%s:%s@%s/%s?charset=utf8' % (
    user,
    password,
    host,
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
