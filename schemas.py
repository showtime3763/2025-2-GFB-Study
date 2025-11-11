"""
Pydantic 스키마 정의
API 요청/응답 데이터의 구조와 검증 규칙을 정의합니다.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional


# TODO: PostCreate 스키마 작성 (게시글 생성용)
class PostCreate(BaseModel):
    """
    게시글 생성 요청 스키마

    Fields:
        title: 게시글 제목 (1~100자, 필수)
        content: 게시글 내용 (1자 이상, 필수)
    """

    # TODO: title 필드 정의
    # 힌트: str = Field(..., min_length=1, max_length=100)
    title: str = Field(..., min_length=1, max_length=100)

    # TODO: content 필드 정의
    # 힌트: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)

    # TODO: title validator 작성 (공백만 있으면 에러)
    @validator('title')
    def title_must_not_be_empty(cls, v):
        # 힌트: if not v.strip(): raise ValueError('...')
        if not v.strip():
            raise ValueError('Title cannot be empty or whitespace only')
        return v


# TODO: PostUpdate 스키마 작성 (게시글 수정용)
class PostUpdate(BaseModel):
    """
    게시글 수정 요청 스키마

    Fields:
        title: 게시글 제목 (선택, 있으면 1~100자)
        content: 게시글 내용 (선택, 있으면 1자 이상)
    """

    # TODO: title 필드 정의 (Optional)
    # 힌트: Optional[str] = Field(None, min_length=1, max_length=100)
    title: Optional[str] = Field(None, min_length=1, max_length=100)

    # TODO: content 필드 정의 (Optional)
    content: Optional[str] = Field(None, min_length=1)


# TODO: PostResponse 스키마 작성 (게시글 응답용)
class PostResponse(BaseModel):
    """
    게시글 응답 스키마

    Fields:
        id: 게시글 ID
        title: 게시글 제목
        content: 게시글 내용
    """

    # TODO: id, title, content 필드 정의
    id: int
    title: str
    content: str

    # TODO: Config 클래스 작성
    # 힌트: from_attributes = True (SQLAlchemy 모델 -> Pydantic 변환)
    class Config:
        from_attributes = True