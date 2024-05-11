from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from schemas import TodoSchema
from models import Todo  # Import the Todo model

app = FastAPI()

# Dependency function to get a database session
def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()

@app.post("/createTodo", response_model=TodoSchema)
def create_todo(todo: TodoSchema, session: Session = Depends(get_session)):
    new_todo = Todo(title=todo.title, completed=todo.completed)
    session.add(new_todo)
    session.commit()
    session.refresh(new_todo)
    return new_todo

@app.get("/getTodoById/{todo_id}", response_model=TodoSchema)
def get_todo_by_id(todo_id: int, session: Session = Depends(get_session)):
    todo = session.query(Todo).get(todo_id)
    if todo:
        return todo
    else:
        return {"error": "Todo not found"}

@app.get("/getTodoByTitle/{title}", response_model=list[TodoSchema])
def get_todo_by_title(title: str, session: Session = Depends(get_session)):
    todos = session.query(Todo).filter(Todo.title == title).all()
    if todos:
        return todos
    else:
        return {"error": f"No todos found with title '{title}'"}

@app.delete("/deleteById/{todo_id}")
def delete_todo_by_id(todo_id: int, session: Session = Depends(get_session)):
    todo = session.query(Todo).get(todo_id)
    if todo:
        session.delete(todo)
        session.commit()
        return {"message": "Todo deleted successfully"}
    else:
        return {"error": "Todo not found"}

@app.delete("/deleteByTitle/{title}")
def delete_todo_by_title(title: str, session: Session = Depends(get_session)):
    todos = session.query(Todo).filter(Todo.title == title).all()
    if todos:
        for todo in todos:
            session.delete(todo)
        session.commit()
        return {"message": f"All todos with title '{title}' deleted successfully"}
    else:
        return {"error": f"No todos found with title '{title}'"}

@app.delete("/deleteAll")
def delete_all_todos(session: Session = Depends(get_session)):
    session.query(Todo).delete()
    session.commit()
    return {"message": "All todos deleted successfully"}

@app.get("/getAllTodos", response_model=list[TodoSchema])
def get_all_todos(session: Session = Depends(get_session)):
    todos = session.query(Todo).all()
    return todos

@app.put("/updateTodo/{todo_id}", response_model=TodoSchema)
def update_todo(todo_id: int, updated_todo: TodoSchema, session: Session = Depends(get_session)):
    todo = session.query(Todo).get(todo_id)
    if todo:
        todo.title = updated_todo.title
        todo.completed = updated_todo.completed
        session.commit()
        return todo
    else:
        return {"error": "Todo not found"}