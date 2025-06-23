import json
import datetime
from collections import defaultdict
from typing import List, Dict, Set, Optional, Union, Any, DefaultDict

Document = Dict[str, Any]
Label = Dict[str, str]
DocumentsList = List[Document]
LabelsList = List[Label]
RelationsList = List[Dict[str, Union[str, List[str]]]]
NetworkDict = Dict[str, List[Dict[str, str]]]


def find_related_documents(
        documents: DocumentsList,
        labels_to_find: LabelsList,
        visited: Optional[Set[str]] = None,
        depth: int = 0,
        max_depth: int = 10
    ) -> DocumentsList:

    if visited is None:
        visited = set()
    if depth >= max_depth:
        return []
    related_docs = []
    new_labels_to_find = []

    for doc in documents:
        has_all_labels = all(
            any(label == l for l in doc.get("labels", []))
            for label in labels_to_find
        )
        
        if has_all_labels and doc["hash"] not in visited:
            related_docs.append(doc)
            visited.add(doc["hash"])
            new_labels_to_find.extend(doc.get("labels", []))

    if new_labels_to_find and depth < max_depth:
        deeper_docs = find_related_documents(
            documents, 
            new_labels_to_find, 
            visited, 
            depth + 1, 
            max_depth
        )
        related_docs.extend(deeper_docs)
    
    return related_docs


def generate_relations_json(
        documents: DocumentsList,
        initial_labels: LabelsList,
        output_file: str = "relations.json"
    ) -> Dict[str, Union[Dict[str, Any], DefaultDict[str, List[Document]], RelationsList, NetworkDict]]:
    
    related_docs = find_related_documents(documents, initial_labels)
    
    docs_by_type = defaultdict(list)
    for doc in related_docs:
        docs_by_type[doc["type"]].append(doc)
    
    relations = []
    for doc in related_docs:
        if "document" in doc and "requires" in doc["document"]:
            relations.append({
                "source": doc["document"].get("name", doc["hash"]),
                "targets": doc["document"]["requires"],
                "type": "dependency"
            })
    
    result = {
        "metadata": {
            "initial_labels": initial_labels,
            "total_documents": len(related_docs),
            "document_types": list(docs_by_type.keys()),
            "timestamp": datetime.datetime.now().isoformat()
        },
        "documents_by_type": docs_by_type,
        "relations": relations,
        "network": {
            "nodes": [],
            "links": []
        }
    }
    
    nodes = set()
    for doc in related_docs:
        node_id = doc.get("document", {}).get("name", doc["hash"])
        nodes.add((node_id, doc["type"]))
        
        for label in doc.get("labels", []):
            if label["key"] in ["database", "queue", "s3", "web"]:
                result["network"]["links"].append({
                    "source": node_id,
                    "target": label["value"],
                    "type": "uses"
                })
    
    result["network"]["nodes"] = [{"id": n[0], "type": n[1]} for n in nodes]
    
    with open(output_file, "w") as f:
        json.dump(result, f, indent=4)
    
    return result


