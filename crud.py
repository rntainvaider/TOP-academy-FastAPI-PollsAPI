from sqlalchemy.orm import Session
from fastapi import HTTPException

from model.models import Poll, Vote


def vote_in_poll(db: Session, poll_id: int, username: str):
    # Проверяем, существует ли голос для данного пользователя и опроса
    existing_vote = (
        db.query(Vote)
        .filter(Vote.username == username, Vote.poll_id == poll_id)
        .first()
    )
    if existing_vote:
        raise HTTPException(status_code=400, detail="Вы уже голосовали в этом опросе.")

    # Создаем голос
    vote = Vote(username=username, poll_id=poll_id)
    db.add(vote)
    db.commit()
    db.refresh(vote)
    return vote


def delete_poll(db: Session, poll_id: int, username: str):
    # Проверяем, существует ли опрос
    poll = db.query(Poll).filter(Poll.id == poll_id).first()
    if not poll:
        raise HTTPException(status_code=404, detail="Опрос не найден.")

    # Проверяем, что текущий пользователь — создатель опроса
    if poll.creator_username != username:
        raise HTTPException(status_code=403, detail="Вы не можете удалить этот опрос.")

    # Удаляем опрос
    db.delete(poll)
    db.commit()
    return {"detail": "Опрос успешно удален."}
