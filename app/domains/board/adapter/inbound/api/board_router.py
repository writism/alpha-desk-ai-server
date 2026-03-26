from typing import Optional

from fastapi import APIRouter, Cookie, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.domains.account.adapter.outbound.persistence.account_repository_impl import AccountRepositoryImpl
from app.domains.auth.adapter.outbound.in_memory.redis_session_adapter import RedisSessionAdapter
from app.domains.board.adapter.outbound.persistence.board_repository_impl import BoardRepositoryImpl
from app.domains.board.application.response.board_list_response import BoardListResponse, BoardListItemResponse
from app.domains.board.application.usecase.delete_board_usecase import DeleteBoardUseCase
from app.domains.board.application.usecase.get_board_list_usecase import GetBoardListUseCase
from app.domains.board.application.usecase.get_board_read_usecase import GetBoardReadUseCase
from app.domains.board.application.usecase.update_board_usecase import UpdateBoardUseCase
from app.domains.board.domain.entity.board import Board
from app.infrastructure.cache.redis_client import redis_client
from app.infrastructure.database.session import get_db

router = APIRouter(prefix="/board", tags=["board"])

_session_adapter = RedisSessionAdapter(redis_client)


class CreateBoardRequest(BaseModel):
    title: str
    content: str


class UpdateBoardRequest(BaseModel):
    title: str
    content: str


@router.post("", response_model=BoardListItemResponse, status_code=201)
async def create_board(
    request: CreateBoardRequest,
    account_id: Optional[str] = Cookie(default=None),
    db: Session = Depends(get_db),
):
    if not account_id:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")

    parsed_account_id = int(account_id)
    account_repository = AccountRepositoryImpl(db)
    account = account_repository.find_by_id(parsed_account_id)
    if not account:
        raise HTTPException(status_code=401, detail="존재하지 않는 계정입니다.")

    board_repository = BoardRepositoryImpl(db)
    saved = board_repository.save(Board(
        title=request.title,
        content=request.content,
        account_id=parsed_account_id,
    ))

    return BoardListItemResponse(
        board_id=saved.id,
        title=saved.title,
        content=saved.content,
        nickname=account.nickname,
        created_at=saved.created_at,
        updated_at=saved.updated_at,
    )


@router.get("/list", response_model=BoardListResponse)
async def get_board_list(
    page: int = 1,
    size: int = 10,
    account_id: Optional[str] = Cookie(default=None),
    db: Session = Depends(get_db),
):
    if not account_id:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")

    board_repository = BoardRepositoryImpl(db)
    account_repository = AccountRepositoryImpl(db)
    usecase = GetBoardListUseCase(board_repository, account_repository)
    return usecase.execute(page=page, size=size)


@router.delete("/delete/{board_id}")
async def delete_board(
    board_id: int,
    user_token: Optional[str] = Cookie(default=None),
    db: Session = Depends(get_db),
):
    if not user_token:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")

    session = _session_adapter.find_by_token(user_token)
    if not session:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")

    account_id = int(session.user_id)
    board_repository = BoardRepositoryImpl(db)
    usecase = DeleteBoardUseCase(board_repository)

    try:
        return usecase.execute(board_id, account_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.get("/read/{board_id}", response_model=BoardListItemResponse)
async def read_board(
    board_id: int,
    user_token: Optional[str] = Cookie(default=None),
    db: Session = Depends(get_db),
):
    if not user_token:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")

    session = _session_adapter.find_by_token(user_token)
    if not session:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")

    board_repository = BoardRepositoryImpl(db)
    account_repository = AccountRepositoryImpl(db)
    usecase = GetBoardReadUseCase(board_repository, account_repository)
    result = usecase.execute(board_id)

    if result is None:
        raise HTTPException(status_code=404, detail="게시물을 찾을 수 없습니다.")

    return result


@router.put("/{board_id}", response_model=BoardListItemResponse)
async def update_board(
    board_id: int,
    request: UpdateBoardRequest,
    account_id: Optional[str] = Cookie(default=None),
    db: Session = Depends(get_db),
):
    if not account_id:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")

    board_repository = BoardRepositoryImpl(db)
    account_repository = AccountRepositoryImpl(db)
    usecase = UpdateBoardUseCase(board_repository, account_repository)
    result = usecase.execute(board_id, request.title, request.content)

    if result is None:
        raise HTTPException(status_code=404, detail="게시물을 찾을 수 없습니다.")

    return result


@router.get("/{board_id}", response_model=BoardListItemResponse)
async def get_board(
    board_id: int,
    account_id: Optional[str] = Cookie(default=None),
    db: Session = Depends(get_db),
):
    if not account_id:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")

    board_repository = BoardRepositoryImpl(db)
    board = board_repository.find_by_id(board_id)
    if not board:
        raise HTTPException(status_code=404, detail="게시물을 찾을 수 없습니다.")

    account_repository = AccountRepositoryImpl(db)
    account = account_repository.find_by_id(board.account_id)

    return BoardListItemResponse(
        board_id=board.id,
        title=board.title,
        content=board.content,
        nickname=account.nickname if account else "알 수 없음",
        created_at=board.created_at,
        updated_at=board.updated_at,
    )
