from http.client import responses

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from starlette import status
from ..database import Base
from ..main import app
from ..routers.todos import get_db,get_current_user
from fastapi.testclient import TestClient
import pytest
from ..models import Todos

SQLALCHEMY_DATABASE_URL= "sqlite:///./testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit = False, autoflush=False, bind = engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return { 'username': 'abhi80', 'id': 1, 'user_role' : 'admin' }

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos(title = 'Learn fast api',
                 description = 'Its awesome',
                 priority = 5,
                 complete = False,
                 owner_id = 1)
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE from todos;"))
        connection.commit()

def test_read_all_authenticated(test_todo):
    response = client.get("/")
    assert  response.status_code == status.HTTP_200_OK
    assert response.json() == [{'title' : 'Learn fast api',
                 'description' : 'Its awesome',
                 'priority' : 5,
                 'complete' : False,
                 'owner_id' : 1,
                 'id': 1
                }]

def test_read_one_authenticated(test_todo):
    response = client.get("/todos/1")
    assert  response.status_code == status.HTTP_200_OK
    assert response.json() == {'title' : 'Learn fast api',
                 'description' : 'Its awesome',
                 'priority' : 5,
                 'complete' : False,
                 'owner_id' : 1,
                 'id': 1
                }
def test_read_one_authenticated_not_found(test_todo):
    response = client.get("/todos/444")
    assert  response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail' : 'Todo Not Found!'}

def test_create_todo(test_todo):
    request_todo={
        'title': 'Feed the dog',
        'description': 'Its Hungry',
        'priority': 2,
        'complete': False
    }
    response = client.post("/todo", json = request_todo)
    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_todo.get('title')
    assert model.description == request_todo.get('description')
    assert model.priority == request_todo.get('priority')
    assert model.complete == request_todo.get('complete')