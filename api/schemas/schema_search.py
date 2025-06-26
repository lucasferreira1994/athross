from pydantic import BaseModel
from typing import List, Dict, Union
from datetime import datetime
from api.schemas.schema_label import LabelBase


class DocumentSearch(BaseModel):
    document_uuid: str
    labels: List[LabelBase]

    
class Label(BaseModel):
    key: str
    value: str


class DocumentMetadata(BaseModel):
    initial_labels: List[Label]
    total_documents: int
    document_types: List[str]
    timestamp: datetime


class RawDocument(BaseModel):
    name: str
    domain: str
    requires: List[str]


class DocumentItem(BaseModel):
    hash: str
    type: str
    created_by: str
    labels: List[Label]
    document: RawDocument


class DocumentSearchResponseFlat(BaseModel):
    metadata: DocumentMetadata
    documents: List[DocumentItem]

    class ConfigDict:
        schema_extra = {
            "example": {
                "metadata": {
                    "initial_labels": [
                        {"key": "domain", "value": "app-dev.example.com"}
                    ],
                    "total_documents": 1,
                    "document_types": ["app"],
                    "timestamp": "2025-06-23T17:05:11.243798"
                },
                "documents": [
                    {
                        "hash": "8f0c5025bfc99ae58cf883ce32e92894",
                        "type": "app",
                        "created_by": "data-fake",
                        "labels": [
                            {"key": "ipv4", "value": "10.0.250.1"},
                            {"key": "domain", "value": "app-dev.example.com"}
                        ],
                        "document": {
                            "name": "app-dev",
                            "domain": "app-dev.example.com",
                            "requires": [
                                "database-dev.example.com",
                                "queue-dev.example.com",
                                "s3-dev.example.com",
                                "web-dev.example.com"
                            ]
                        }
                    }
                ]
            }
        }


class DocumentSearchResponseByType(BaseModel):
    metadata: DocumentMetadata
    documents_by_type: Dict[str, List[DocumentItem]]

    class ConfigDict:
        schema_extra = {
            "example": {
                "metadata": {
                    "initial_labels": [
                        {"key": "domain", "value": "app-dev.example.com"}
                    ],
                    "total_documents": 1,
                    "document_types": ["app"],
                    "timestamp": "2025-06-23T17:05:11.243798"
                },
                "documents_by_type": {
                    "app": [
                        {
                            "hash": "8f0c5025bfc99ae58cf883ce32e92894",
                            "type": "app",
                            "created_by": "data-fake",
                            "labels": [
                                {"key": "ipv4", "value": "10.0.250.1"},
                                {"key": "domain", "value": "app-dev.example.com"},
                                {"key": "database", "value": "database-dev.example.com"}
                            ],
                            "document": {
                                "name": "app-dev",
                                "domain": "app-dev.example.com",
                                "requires": [
                                    "database-dev.example.com",
                                    "queue-dev.example.com",
                                    "s3-dev.example.com",
                                    "web-dev.example.com"
                                ]
                            }
                        }
                    ]
                }
            }
        }

DocumentSearchResponse = Union[DocumentSearchResponseFlat, DocumentSearchResponseByType]