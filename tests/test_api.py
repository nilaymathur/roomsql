import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_all_students():
    query = """
        query {
            getAllStudents {
                _id
                name
                roll
                marks
            }
        }
    """
    response = client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    assert "data" in response.json()

def test_create_student():
    mutation = """
        mutation {
            createStudent(name: "John Doe", roll: 5, marks:[{subject:"Science", mark:60}, {subject:"Math", mark:75}]) {
                _id
                name
                roll
                marks
            }
        }
    """
    response = client.post("/graphql", json={"query": mutation})
    assert response.status_code == 200
    assert "data" in response.json()
