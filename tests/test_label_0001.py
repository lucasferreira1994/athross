from fastapi.testclient import TestClient
from main import app
import os



from factory.factory_log import get_logger

TAG = os.path.basename(__file__) + ": "
logger = get_logger(TAG)

async def test_label_crud(async_client):
    payload = [
        {"key": "teste", "value": "teste"},
        {"key": "teste1", "value": "teste2"},
        {"key": "teste3", "value": "teste23"}
    ]

<<<<<<< HEAD
    create_response = await async_client.post("/labels/", json=payload)
    assert create_response.status_code == 201
=======
    create_response = await async_client.post("/api/v1/labels/", json=payload)
    assert create_response.status_code == 200
>>>>>>> 584054f2643d394146b28b1a7904c5d83a34115a
    created_labels = create_response.json()
    assert len(created_labels) == len(payload)

    created_keys = [label["key"] for label in created_labels]
    for item in payload:
        assert item["key"] in created_keys

<<<<<<< HEAD
    list_response = await async_client.get("/labels/")
=======
    list_response = await async_client.get("/api/v1/labels/")
>>>>>>> 584054f2643d394146b28b1a7904c5d83a34115a
    assert list_response.status_code == 200
    listed_labels = list_response.json()
    assert len(listed_labels) >= len(payload) 

    for label in created_labels:
<<<<<<< HEAD
        delete_response = await async_client.delete(f"/labels/{label['id']}")
=======
        delete_response = await async_client.delete(f"/api/v1/labels/{label['id']}")
>>>>>>> 584054f2643d394146b28b1a7904c5d83a34115a
        assert delete_response.status_code == 200
        deleted_label = delete_response.json()
        assert deleted_label["id"] == label["id"]
        assert deleted_label["key"] == label["key"]

<<<<<<< HEAD
    final_list_response = await async_client.get("/labels/")
=======
    final_list_response = await async_client.get("/api/v1/labels/")
>>>>>>> 584054f2643d394146b28b1a7904c5d83a34115a
    assert final_list_response.status_code == 200
    remaining_labels = final_list_response.json()
    remaining_ids = [label["id"] for label in remaining_labels]
    for label in created_labels:
        assert label["id"] not in remaining_ids

    logger.info(TAG + "Finalizado test_label_crud com sucesso")