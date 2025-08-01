import os
from uuid import uuid4
import json
from factory.factory_log import get_logger

TAG = os.path.basename(__file__) + ": "
logger = get_logger(TAG)

async def test_create_list_delete_documents(async_client):
    logger.info("Iniciando test_create_list_delete_documents")
    base_hash = str(uuid4().hex)

    payload = [
        {
            "hash": base_hash,
            "type": "test_type_1",
            "created_by": "pytest_user_1",
            "labels": [
                {"key": "label1", "value": "value1"},
                {"key": "label2", "value": "value2"}
            ],
            "document": {
                "field_a": "value_a",
                "field_b": "value_b"
            }
        }
    ]
    logger.info(f"Payload de criação: {json.dumps(payload, indent=2)}")

    create_resp = await async_client.post("/documents/", json=payload)
    logger.info(f"Response de criação: status={create_resp.status_code} body={create_resp.json()}")
    assert create_resp.status_code == 201

    created_docs = create_resp.json()
    assert len(created_docs) == 1
    created_doc = created_docs[0]
    logger.info(f"Documento criado: {json.dumps(created_doc, indent=2)}")

    list_resp = await async_client.get("/documents/")
    logger.info(f"Response de listagem: status={list_resp.status_code} body={list_resp.json()}")
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 1

    update_payload = [
        {
            "hash": base_hash,
            "type": "test_type_2",
            "created_by": "pytest_user_2",
            "labels": [
                {"key": "label3", "value": "value3"},
                {"key": "label4", "value": "value4"}
            ],
            "document": {
                "field_a": "updated_value_a",
                "field_b": "updated_value_b"
            }
        }
    ]
    logger.info(f"Payload de atualização: {json.dumps(update_payload, indent=2)}")
    update_resp = await async_client.post("/documents/", json=update_payload)
    logger.info(f"Response de atualização: status={update_resp.status_code} body={update_resp.json()}")
    assert update_resp.status_code == 201

    final_list_resp = await async_client.get("/documents/")
    logger.info(f"Response de listagem final: status={final_list_resp.status_code} body={final_list_resp.json()}")
    assert final_list_resp.status_code == 200
    final_docs = final_list_resp.json()
    assert len(final_docs) == 1
    final_doc = final_docs[0]
    assert final_doc["type"]["name"] == "test_type_2"
    assert final_doc["created_by"] == "pytest_user_2"

    logger.info(f"Documento após update: {json.dumps(final_doc, indent=2)}")

    delete_resp = await async_client.request( method="DELETE", url="/documents/", json=[final_doc["id"]])
    logger.info(f"Response de delete_all: status={delete_resp.status_code} body={delete_resp.json()}")
    assert delete_resp.status_code == 200
    assert delete_resp.json()["detail"] == "All documents deleted"

    empty_list_resp = await async_client.get("/documents/")
    logger.info(f"Response de listagem após delete_all: status={empty_list_resp.status_code} body={empty_list_resp.json()}")
    assert empty_list_resp.status_code == 200
    assert empty_list_resp.json() == []

    logger.info("Finalizado test_create_list_delete_documents com sucesso")

#teste errado
# async def test_create_and_update_many_documents(async_client):
#     many_payload = []
#     logger.info("Iniciando test_create_many_documents")
#     for i in range(1000):
#         many_payload.append({
#             "hash": str(uuid4().hex),
#             "type": "test_type_2",
#             "created_by": "pytest_user_2",
#             "labels": [
#                 {"key": "label3", "value": "value3"},
#                 {"key": "label4", "value": "value4"}
#             ],
#             "document": {
#                 "field_a": "updated_value_a",
#                 "field_b": "updated_value_b"
#             }
#         })

#     logger.info(f"Payload to create many: len={len(many_payload)}")
#     many_resp = await async_client.post("/api/v1/documents/", json=many_payload)
#     logger.info(f"Response to create many: status={many_resp.status_code}")
#     assert many_resp.status_code == 200

#     logger.info("Update many documents")
#     logger.info(f"Payload to update many: len={len(many_payload)}")
#     many_update_resp = await async_client.post("/api/v1/documents/", json=many_payload)
#     logger.info(f"Response to update many: status={many_update_resp.status_code}")
#     assert many_update_resp.status_code == 200

#     many_payload_with_new_label = []
#     for i in many_payload:
#         i["labels"].append({"key": "label5", "value": "value5"})
#         many_payload_with_new_label.append(i)
    
#     logger.info(f"Payload to create many: len={len(many_payload)}")
#     many_resp = await async_client.post("/api/v1/documents/", json=many_payload)
#     logger.info(f"Response to create many: status={many_resp.status_code}")
#     assert many_resp.status_code == 200

#     final_list_resp = await async_client.get("/api/v1/documents/")
#     logger.info(f"Response of final list: status={final_list_resp.status_code} body={final_list_resp.json()}")
#     assert final_list_resp.status_code == 200

#     final_docs = final_list_resp.json()
#     assert len(final_docs) == 1000

#     for doc in final_docs:
#         labels = []
#         for label in doc["labels"]:
#             labels.append({
#                 "key": label["key"],
#                 "value": label["value"]
#             })

#         assert {"key": "label4", "value": "value4"} in labels
#         assert {"key": "label3", "value": "value3"} in labels
#         assert {"key": "label5", "value": "value5"} in labels

#     logger.info("Finishing test_create_and_update_many_documents")
