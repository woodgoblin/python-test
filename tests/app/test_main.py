import os
import time

import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app, get_db
from app.database import Base, SessionLocal

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
# Create a new SQLite database for testing
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Override the get_db dependency to use the test database
# Override the get_db dependency to use the test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def test_db():
    db = TestingSessionLocal()
    yield db
    print(f"!!!!!!! teardown entered")
    db.close()

    # Teardown
    db_path = SQLALCHEMY_DATABASE_URL
    try:
        # Close all connections
        db.session.close_all()
        # Attempt to remove the file
        print(f"!!!!!!! removing {db_path}")
        os.remove(db_path)
    except Exception as e:
        print(f"Error removing {db_path}: {e}")
        # Retry the removal after some time
        for i in range(5):
            try:
                time.sleep(1)
                os.remove(db_path)
                print(f"Successfully removed {db_path} on attempt {i + 1}")
                break
            except Exception as e:
                print(f"Retry {i + 1} failed: {e}")


app.dependency_overrides[get_db] = override_get_db

# Create the tables in the test database
Base.metadata.create_all(bind=engine)


@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_create_cat(async_client: AsyncClient):
    response = await async_client.post("/cats/", json={
        "birth_date": "2020-01-01",
        "paws_quantity": 4,
        "name": "Whiskers",
        "gender": "M",
        "tails_quantity": 1
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Whiskers"


@pytest.mark.asyncio
async def test_read_cats(async_client):
    response = await async_client.get("/cats/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0


@pytest.mark.asyncio
async def test_read_cat(async_client):
    response = await async_client.get("/cats/1")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Whiskers"


@pytest.mark.asyncio
async def test_update_cat(async_client):
    response = await async_client.put("/cats/1", json={
        "birth_date": "2020-01-01",
        "paws_quantity": 4,
        "name": "Whiskers Updated",
        "gender": "M",
        "tails_quantity": 1
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Whiskers Updated"


@pytest.mark.asyncio
async def test_delete_cat(async_client):
    response = await async_client.delete("/cats/1")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Whiskers Updated"


@pytest.mark.asyncio
async def test_create_rat(async_client):
    # Create a rat that is not eaten
    response = await async_client.post(
        "/rats/",
        json={"birth_date": "2022-01-01", "courage": 5, "stupidity": 2, "is_eaten": False}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["birth_date"] == "2022-01-01"
    assert data["courage"] == 5
    assert data["stupidity"] == 2
    assert data["is_eaten"] == False
    assert data["cat_id"] is None


@pytest.mark.asyncio
async def test_read_rats(async_client):
    response = await async_client.get("/rats/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_read_rat(async_client):
    response = await async_client.post(
        "/rats/",
        json={"birth_date": "2022-01-01", "courage": 5, "stupidity": 2, "is_eaten": False}
    )
    rat_id = response.json()["id"]
    response = await async_client.get(f"/rats/{rat_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == rat_id


@pytest.mark.asyncio
async def test_update_rat(async_client):
    response = await async_client.post(
        "/rats/",
        json={"birth_date": "2022-01-01", "courage": 5, "stupidity": 2, "is_eaten": False, "cat_id": None}
    )
    rat_id = response.json()["id"]


@pytest.mark.asyncio
async def test_delete_rat(async_client):
    response = await async_client.post(
        "/rats/",
        json={"birth_date": "2022-01-01", "courage": 5, "stupidity": 2, "is_eaten": False, "cat_id": None}
    )
    rat_id = response.json()["id"]
    response = await async_client.delete(f"/rats/{rat_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == rat_id
    response = await async_client.get(f"/rats/{rat_id}")
    assert response.status_code == 404
