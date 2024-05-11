from pydantic import BaseModel

class TodoSchema(BaseModel):
    id: int
    title: str
    completed: bool = False

    class Config:
        orm_mode = True