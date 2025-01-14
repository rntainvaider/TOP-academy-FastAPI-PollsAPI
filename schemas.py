from pydantic import BaseModel


class PollCreate(BaseModel):
    question: str


class PollResponse(BaseModel):
    id: int
    question: str
    creator_username: str

    class Config:
        orm_mode = True


class VoteResponse(BaseModel):
    id: int
    username: str
    poll_id: int

    class Config:
        orm_mode = True
