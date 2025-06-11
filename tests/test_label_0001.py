from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_crud():
    # create
    payload = [
        {
            "key": "teste",
            "value": "teste"
        },
        {
            "key": "teste1",
            "value": "teste2"
        },
        {
            "key": "teste3",
            "value": "teste23"
        }
    ]

    response = client.post("/labels", json=payload)
    assert response.status_code == 200

    # list
    response = client.get("/labels")
    assert response.status_code == 200

    # delete

    for label in response.json():
        response = client.delete(f"/labels/{label['id']}")
        assert response.status_code == 200