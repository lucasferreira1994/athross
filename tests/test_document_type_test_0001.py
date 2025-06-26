import uuid
from factory.factory_log import get_logger
import os

TAG = os.path.basename(__file__) + ": "
logger = get_logger(TAG)


async def test_create_list_delete_document_types(async_client):
    logger.info("Iniciando test_create_list_delete_document_types")

    payload = [
        {"name": "json"},
        {"name": "xml"},
        {"name": "csv"},
        {"name": "parquet"}
    ]
    logger.info(f"Payload utilizado para teste: {payload}")

<<<<<<< HEAD
    create_resp = await async_client.post("/document-types/", json=payload)
    logger.info(f"Response da criação: {create_resp.json()}")
    assert create_resp.status_code == 201
=======
    create_resp = await async_client.post("/api/v1/document-types/", json=payload)
    logger.info(f"Response da criação: {create_resp.json()}")
    assert create_resp.status_code == 200
>>>>>>> 584054f2643d394146b28b1a7904c5d83a34115a
    logger.info(f"Resposta de criação OK, status code: {create_resp.status_code}")

    created_items = create_resp.json()
    logger.info(f"Items criados: {created_items}")
    assert len(created_items) == 4

    created_names = [item["name"] for item in created_items]
    for expected in ["json", "xml", "csv", "parquet"]:
        assert expected in created_names
        logger.info(f"Item '{expected}' confirmado na resposta de criação")

<<<<<<< HEAD
    list_resp = await async_client.get("/document-types/")
=======
    list_resp = await async_client.get("/api/v1/document-types/")
>>>>>>> 584054f2643d394146b28b1a7904c5d83a34115a
    logger.info(f"Response da listagem: status {list_resp.status_code}")
    assert list_resp.status_code == 200

    list_data = list_resp.json()
    logger.info(f"Dados da listagem: {list_data}")
    assert "items" in list_data
    assert list_data["total"] == 4

    listed_names = [item["name"] for item in list_data["items"]]
    for expected in ["json", "xml", "csv", "parquet"]:
        assert expected in listed_names
        logger.info(f"Item '{expected}' confirmado na listagem")

    logger.info("Iniciando remoção dos itens listados")
    for item in list_data["items"]:
<<<<<<< HEAD
        delete_resp = await async_client.delete(f"/document-types/{item['id']}")
        logger.info(f"Delete /document-types/{item['id']} status {delete_resp.status_code}")
=======
        delete_resp = await async_client.delete(f"/api/v1/document-types/{item['id']}")
        logger.info(f"Delete /api/v1/document-types/{item['id']} status {delete_resp.status_code}")
>>>>>>> 584054f2643d394146b28b1a7904c5d83a34115a
        assert delete_resp.status_code == 200

        deleted_item = delete_resp.json()
        logger.info(f"Item deletado retornado: {deleted_item}")
        assert deleted_item["id"] == item["id"]
        assert deleted_item["name"] == item["name"]
        logger.info(f"Item '{item['name']}' removido com sucesso")

<<<<<<< HEAD
    final_list = await async_client.get("/document-types/")
=======
    final_list = await async_client.get("/api/v1/document-types/")
>>>>>>> 584054f2643d394146b28b1a7904c5d83a34115a
    logger.info(f"Response da listagem final após exclusões: status {final_list.status_code}")
    assert final_list.status_code == 200

    final_data = final_list.json()
    logger.info(f"Dados finais após exclusões: {final_data}")
    assert final_data["total"] == 0
    assert final_data["items"] == []
    logger.info("Todos os itens removidos com sucesso. Teste concluído")


async def test_delete_nonexistent_document_type(async_client):
    fake_id = str(uuid.uuid4())
    logger.info(f"Iniciando test_delete_nonexistent_document_type com id falso: {fake_id}")

<<<<<<< HEAD
    resp = await async_client.delete(f"/document-types/{fake_id}")
=======
    resp = await async_client.delete(f"/api/v1/document-types/{fake_id}")
>>>>>>> 584054f2643d394146b28b1a7904c5d83a34115a
    logger.info(f"Response da exclusão de id inexistente: status {resp.status_code}, body: {resp.json()}")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "DocumentType not found"
    logger.info("Confirmação da resposta 404 para exclusão de id inexistente concluída")

    logger.info("Finalizando test_delete_nonexistent_document_type com sucesso")
