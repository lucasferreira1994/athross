from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_crud():
    # create
    payload = [
        {
            "name": "teste"
        },
        {
            "name": "teste1"
        },
        {
            "name": "teste3"
        }
    ]

    response = client.post("/document-types", json=payload)
    assert response.status_code == 200

    # list
    response = client.get("/document-types")
    assert response.status_code == 200

    # delete

    for document_type in response.json():
        response = client.delete(f"/document-types/{document_type['id']}")
        assert response.status_code == 200