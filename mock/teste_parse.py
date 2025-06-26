import json
import datetime
from collections import defaultdict

def find_related_documents(documents, labels_to_find, visited=None, depth=0, max_depth=10):
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


def generate_relations_json(documents, initial_labels, output_file="relations.json", by_type=True):
    related_docs = find_related_documents(documents, initial_labels)
    
    result = {
        "metadata": {
            "initial_labels": initial_labels,
            "total_documents": len(related_docs),
            "timestamp": datetime.datetime.now().isoformat()
        }
    }
    
    if by_type:
        docs_by_type = defaultdict(list)
        for doc in related_docs:
            docs_by_type[doc["type"]].append(doc)
        result["documents_by_type"] = docs_by_type
        result["metadata"]["document_types"] = list(docs_by_type.keys())
    else:
        result["documents"] = related_docs
    
    with open(output_file, "w") as f:
        json.dump(result, f, indent=4)
    
    return result



if __name__ == "__main__":
    import datetime
    name = f"documents_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    path = "/home/alisson/projetos/athross/athross/mock/documents.json"
    with open(path, "r") as f:
        documents = json.load(f)
    
    initial_labels = [
        {"key": "domain", "value": "app-dev.example.com"}
    ]
    
    result = generate_relations_json(
        documents=documents,
        initial_labels=initial_labels,
        output_file=name    )
    