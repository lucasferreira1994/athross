from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_crud():
    # create
    payload = [
            {
                "hash": "4124bc0a9335c27f086f24ba207a4912",
                "type": "test1",
                "created_by": "pytest",
                "labels": [
                    {"key": "label1", "value": "label1"},
                    {"key": "label2", "value": "label2"},
                    {"key": "label3", "value": "label3"}
                ],
                "document": {
                    "a": "aa",
                    "b": "bb",
                    "c": "cc",
                    "d": "dd"
                }
            }
        ]

    response = client.post("/documents", json=payload)
    assert response.status_code == 200

    # list
    response = client.get("/documents")
    assert response.status_code == 200
    assert len(response.json()) == 1

    # repost and change labels
    payload = [
        {
            "hash": "4124bc0a9335c27f086f24ba207a4912",
            "type": "test2",
            "created_by": "pytest2",
            "labels": [
                {"key": "label1", "value": "label111"},
                {"key": "label4", "value": "label444"}
            ],
            "document": {
                "a": "aaa",
                "b": "bbb",
                "c": "ccc",
                "d": "ddd"
            }
        }
    ]
    response = client.post("/documents", json=payload)
    assert response.status_code == 200

    # delete
    # for document_type in response.json():
    #     response = client.delete(f"/documents/{document_type['id']}")
    #     assert response.status_code == 200