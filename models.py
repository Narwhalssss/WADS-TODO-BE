from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create a SQLite database file
engine = create_engine('sqlite:///todos.db', connect_args={'check_same_thread': False})

# Create a base class for the declarative models
Base = declarative_base()

# Define the Todo model
class Todo(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    completed = Column(Boolean, default=False)

    def __repr__(self):
        return f"Todo(id={self.id}, title='{self.title}', completed={self.completed})"

# Create the database tables
Base.metadata.create_all(engine)

# Create a session maker
Session = sessionmaker(bind=engine)