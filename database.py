"""
데이터베이스 연결 설정
SQLAlchemy를 사용하여 SQLite 데이터베이스와 연결합니다.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# TODO: SQLite 데이터베이스 URL 작성
# 힌트: "sqlite:///./community.db"
SQLALCHEMY_DATABASE_URL = "sqlite:///./community.db"

# TODO: 데이터베이스 엔진 생성
# 힌트: create_engine 사용, SQLite의 경우 connect_args 필요
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite 전용: {"check_same_thread": False}
)

# TODO: 세션 로컬 클래스 생성
# 힌트: sessionmaker 사용, autocommit=False, autoflush=False
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# TODO: Base 클래스 생성
# 힌트: declarative_base() 호출
Base = declarative_base()


# TODO: 데이터베이스 세션 의존성 함수 작성
def get_db():
    """
    데이터베이스 세션을 생성하고 반환합니다.
    요청이 끝나면 자동으로 세션을 닫습니다.
    """
    # 1. SessionLocal() 인스턴스 생성
    db = SessionLocal()

    try:
        # 2. yield로 세션 전달
        yield db
    finally:
        # 3. 세션 닫기
        db.close()