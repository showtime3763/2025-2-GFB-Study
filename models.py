"""
데이터베이스 모델 정의
SQLAlchemy ORM을 사용하여 테이블 구조를 정의합니다.
"""

from sqlalchemy import Column, Integer, String, Text
from database import Base


# TODO: Post 모델 클래스 작성
class Post(Base):
    """
    게시글 테이블

    Columns:
        id: 게시글 ID (Primary Key, Auto Increment)
        title: 게시글 제목 (최대 100자, 필수)
        content: 게시글 내용 (긴 텍스트, 필수)
    """

    # TODO: 테이블 이름 지정
    # 힌트: __tablename__ = "posts"
    __tablename__ = "posts"

    # TODO: id 컬럼 정의
    # 힌트: Column(Integer, primary_key=True, index=True)
    id = Column(Integer, primary_key=True, index=True)

    # TODO: title 컬럼 정의
    # 힌트: Column(String(100), nullable=False)
    title = Column(String(100), nullable=False)

    # TODO: content 컬럼 정의
    # 힌트: Column(Text, nullable=False)
    content = Column(Text, nullable=False)