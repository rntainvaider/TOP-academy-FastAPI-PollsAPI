from typing import Any, Generator
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from crud import delete_poll, vote_in_poll
from model.models import Poll
from schemas import PollCreate, PollResponse, VoteResponse
from database.database import SessionLocal
from security import get_current_user

app = FastAPI()


# Зависимость для получения сессии базы данных
def get_db() -> Generator[Session, Any, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/polls/", response_model=PollResponse)
def create_poll(
    poll: PollCreate,
    db: Session = Depends(get_db),
    username: str = Depends(get_current_user),
) -> None:
    new_poll = Poll(question=poll.question, creator_username=username)
    db.add(new_poll)  # Добавляем в БД
    db.commit()  # Сохраняем изменения
    db.refresh(new_poll)  # Обновляем состояние объекта
    return new_poll


@app.post("/polls/{poll_id}/vote", response_model=VoteResponse)
def vote(
    poll_id: int,
    db: Session = Depends(get_db),
    username: str = Depends(get_current_user),
):
    return vote_in_poll(db, poll_id, username)


@app.delete("/polls/{poll_id}")
def delete_poll_endpoint(
    poll_id: int,
    db: Session = Depends(get_db),
    username: str = Depends(get_current_user),
):
    return delete_poll(db, poll_id, username)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app=app, host="127.0.0.1", port=8000)
