import json
import datetime


def find_related_documents(documents, labels_to_find, visited=None, depth=0, max_depth=10):
    if visited is None:
        visited = set()
    if depth >= max_depth:
        return []
    related_docs = []
    new_labels_to_find = []

    for doc in documents:
        has_label = False
        for label in labels_to_find:
            if label in doc.get("labels", []):
                has_label = True
                break
        if has_label and doc["hash"] not in visited:
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


if __name__ == "__main__":
    with open("documents.json", "r") as f:
        documents = json.load(f)
    
    initial_labels = [
        {"key": "domain", "value": "app-dev.example.com"}
    ]
    related = find_related_documents(documents, initial_labels)
    
    structured_result = {
        "metadata": {
            "initial_search": initial_labels,
            "total_documents": len(related),
            "timestamp": datetime.datetime.now().isoformat()
        },
        "by_type": {},
        "relationships": []
    }
    
    for doc in related:
        doc_type = doc["type"]
        if doc_type not in structured_result["by_type"]:
            structured_result["by_type"][doc_type] = []
        
        simplified_doc = {
            "hash": doc["hash"],
            "labels": doc.get("labels", []),
            "data": doc.get("document", {})
        }
        structured_result["by_type"][doc_type].append(simplified_doc)
    
    output_file = "structured_related_documents.json"
    with open(output_file, "w") as f:
        json.dump(structured_result, f, indent=4)
    
    print(f"Resultados estruturados salvos em {output_file}")
    print(f"Total de documentos relacionados encontrados: {len(related)}")
    print("Distribuição por tipo:")
    for doc_type, items in structured_result["by_type"].items():
        print(f"- {doc_type}: {len(items)} documentos")