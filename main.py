"""
FastAPI 메인 애플리케이션
커뮤니티 게시판 API의 진입점입니다.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional  # Optional import 추가

import models
import schemas
from database import engine, get_db

# TODO: 데이터베이스 테이블 생성
# 힌트: models.Base.metadata.create_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

# TODO: FastAPI 앱 인스턴스 생성
# 힌트: FastAPI(title="Community API", version="1.0.0")
app = FastAPI(
    title="Community API",
    description="커뮤니티 게시판 API - Week 1 복습",
    version="1.0.0"
)


# ==================== Chapter 1: Basic ====================

# TODO: 루트 엔드포인트 작성
@app.get("/")
def read_root():
    """
    API 루트 엔드포인트
    API가 정상 작동하는지 확인합니다.
    """
    # 힌트: {"message": "Welcome to Community API"}
    return {"message": "Welcome to Community API"}


# TODO: Path Parameter로 게시글 조회
@app.get("/posts/{post_id}", response_model=schemas.PostResponse, tags=["Posts"])
def get_post_by_path(post_id: int, db: Session = Depends(get_db)):
    """
    특정 게시글 조회 (Path Parameter 사용)

    Args:
        post_id: 조회할 게시글 ID

    Returns:
        PostResponse: 게시글 정보

    Raises:
        404: 게시글을 찾을 수 없음
    """
    # TODO: 데이터베이스에서 게시글 조회
    # 힌트: db.query(models.Post).filter(models.Post.id == post_id).first()
    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    # TODO: 게시글이 없으면 404 에러
    # 힌트: if not post: raise HTTPException(...)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )

    return post


# TODO: Query Parameter로 게시글 검색
@app.get("/posts/", response_model=List[schemas.PostResponse], tags=["Posts"])
def search_posts(
        keyword: Optional[str] = None,  # 힌트: Optional[str]
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
):
    """
    게시글 목록 조회 및 검색 (Query Parameter 사용)

    Args:
        keyword: 검색 키워드 (선택)
        skip: 건너뛸 개수 (페이지네이션)
        limit: 가져올 최대 개수

    Returns:
        List[PostResponse]: 게시글 목록
    """
    # TODO: 기본 쿼리 작성
    query = db.query(models.Post)

    # TODO: keyword가 있으면 필터 추가
    # 힌트: if keyword: query = query.filter(models.Post.title.contains(keyword))
    if keyword:
        query = query.filter(models.Post.title.contains(keyword))

    # TODO: offset, limit 적용 후 조회
    # 힌트: query.offset(skip).limit(limit).all()
    posts = query.offset(skip).limit(limit).all()

    return posts


# TODO: Request Body로 게시글 생성
@app.post(
    "/posts/",
    response_model=schemas.PostResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Posts"]
)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    """
    새 게시글 생성 (Request Body 사용)

    Args:
        post: 게시글 생성 데이터

    Returns:
        PostResponse: 생성된 게시글 정보
    """
    # TODO: Post 모델 인스턴스 생성
    # 힌트: models.Post(title=post.title, content=post.content)
    db_post = models.Post(
        title=post.title,
        content=post.content
    )

    # TODO: 데이터베이스에 추가
    # 힌트: db.add(db_post)
    db.add(db_post)

    # TODO: 커밋 (실제 저장)
    # 힌트: db.commit()
    db.commit()

    # TODO: 새로고침 (id 등 DB 생성 값 가져오기)
    # 힌트: db.refresh(db_post)
    db.refresh(db_post)

    return db_post


# ==================== Chapter 3: Database Task ====================

# TODO: 게시글 전체 조회 (Read All)
@app.get("/api/posts/", response_model=List[schemas.PostResponse], tags=["Database CRUD"])
def get_all_posts(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
):
    """
    모든 게시글 조회

    Args:
        skip: 건너뛸 개수
        limit: 가져올 최대 개수

    Returns:
        List[PostResponse]: 게시글 목록
    """
    # TODO: 모든 게시글 조회
    # 힌트: db.query(models.Post).offset(skip).limit(limit).all()
    posts = db.query(models.Post).offset(skip).limit(limit).all()

    return posts


# TODO: 게시글 단일 조회 (Read One)
@app.get("/api/posts/{post_id}", response_model=schemas.PostResponse, tags=["Database CRUD"])
def get_single_post(post_id: int, db: Session = Depends(get_db)):
    """
    특정 게시글 조회

    Args:
        post_id: 게시글 ID

    Returns:
        PostResponse: 게시글 정보

    Raises:
        404: 게시글을 찾을 수 없음
    """
    # TODO: 게시글 조회
    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    # TODO: 없으면 404 에러
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )

    return post


# TODO: 게시글 수정 (Update)
@app.put("/api/posts/{post_id}", response_model=schemas.PostResponse, tags=["Database CRUD"])
def update_post(
        post_id: int,
        post_update: schemas.PostCreate,  # 힌트: PostCreate 또는 PostUpdate
        db: Session = Depends(get_db)
):
    """
    게시글 수정

    Args:
        post_id: 수정할 게시글 ID
        post_update: 수정할 데이터

    Returns:
        PostResponse: 수정된 게시글 정보

    Raises:
        404: 게시글을 찾을 수 없음
    """
    # TODO: 수정할 게시글 조회
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()

    # TODO: 게시글 없으면 404 에러
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )

    # TODO: 값 수정
    # 힌트: db_post.title = post_update.title
    db_post.title = post_update.title
    db_post.content = post_update.content

    # TODO: 커밋
    db.commit()

    # TODO: 새로고침
    db.refresh(db_post)

    return db_post


# TODO: 게시글 삭제 (Delete)
@app.delete("/api/posts/{post_id}", tags=["Database CRUD"])
def delete_post(post_id: int, db: Session = Depends(get_db)):
    """
    게시글 삭제

    Args:
        post_id: 삭제할 게시글 ID

    Returns:
        dict: 삭제 성공 메시지

    Raises:
        404: 게시글을 찾을 수 없음
    """
    # TODO: 삭제할 게시글 조회
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()

    # TODO: 게시글 없으면 404 에러
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )

    # TODO: 삭제
    # 힌트: db.delete(db_post)
    db.delete(db_post)

    # TODO: 커밋
    db.commit()

    # TODO: 성공 메시지 반환
    return {"message": f"Post with id {post_id} successfully deleted"}


# ==================== Chapter 4: Responses ====================

# TODO: 에러 처리가 포함된 게시글 조회
@app.get("/api/safe/posts/{post_id}", response_model=schemas.PostResponse, tags=["Error Handling"])
def get_post_safely(post_id: int, db: Session = Depends(get_db)):
    """
    에러 처리가 포함된 게시글 조회

    Args:
        post_id: 게시글 ID

    Returns:
        PostResponse: 게시글 정보

    Raises:
        400: 잘못된 요청 (post_id가 0 이하)
        404: 게시글을 찾을 수 없음
        500: 서버 에러
    """
    # TODO: post_id 검증 (0 이하면 400 에러)
    if post_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Post ID must be greater than 0"
        )

    try:
        # TODO: 게시글 조회
        post = db.query(models.Post).filter(models.Post.id == post_id).first()

        # TODO: 게시글 없으면 404 에러
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id {post_id} not found"
            )

        return post

    except HTTPException:
        # HTTPException은 그대로 다시 발생
        raise
    except Exception as e:
        # TODO: 예상치 못한 에러는 500 에러로 처리
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


# TODO: 상태 코드가 명시된 게시글 생성
@app.post(
    "/api/safe/posts/",
    response_model=schemas.PostResponse,
    status_code=status.HTTP_201_CREATED,  # 힌트: status.HTTP_201_CREATED
    tags=["Error Handling"]
)
def create_post_safely(post: schemas.PostCreate, db: Session = Depends(get_db)):
    """
    에러 처리가 포함된 게시글 생성

    Args:
        post: 게시글 생성 데이터

    Returns:
        PostResponse: 생성된 게시글 정보

    Raises:
        400: 잘못된 요청
    """
    try:
        # TODO: 게시글 생성
        db_post = models.Post(title=post.title, content=post.content)
        db.add(db_post)
        db.commit()
        db.refresh(db_post)

        return db_post

    except Exception as e:
        # TODO: 에러 발생 시 롤백
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create post: {str(e)}"
        )


# ==================== 추가: 통계 API ====================

@app.get("/api/stats", tags=["Statistics"])
def get_statistics(db: Session = Depends(get_db)):
    """
    게시판 통계 조회

    Returns:
        dict: 통계 정보 (총 게시글 수 등)
    """
    # TODO: 전체 게시글 수 조회
    # 힌트: db.query(models.Post).count()
    total_posts = db.query(models.Post).count()

    return {
        "total_posts": total_posts,
        "api_version": "1.0.0",
        "status": "active"
    }


# ==================== 앱 실행 ====================

if __name__ == "__main__":
    import uvicorn

    # TODO: 서버 실행 설정
    # 힌트: uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # 개발 모드: 파일 변경 시 자동 재시작
    )