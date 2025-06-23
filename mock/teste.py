import json
import hashlib

documents = []
domain = "example.com"
data_list = [
    {"env": "dev", "network": 0},
    {"env": "stg", "network": 1},
    {"env": "prd", "network": 2},
]

for item in data_list:
    env = item["env"]
    network = f"10.{item['network']}"

    balancer_ip = f"{network}.250.1"
    app_domain = f"app-{env}.{domain}"

    database_ip = f"{network}.100.1"
    queue_ip = f"{network}.100.2"
    s3_ip = f"{network}.100.3"
    web_ip = f"{network}.100.4"

    # dns documentos
    dns_database_document = {
        "hash": hashlib.md5(f"database-{env}".encode()).hexdigest(),
        "type": "dns",
        "created_by": "data-fake",
        "labels": [
            {"key": "ipv4", "value": database_ip},
            {"key": "domain", "value": f"database-{env}.{domain}"},
            {"key": "database", "value": f"database-{env}"},
        ],
        "document": {
            "fqdn": f"database-{env}.{domain}",
            "ipv4": database_ip
        }
    }

    dns_queue_document = {
        "hash": hashlib.md5(f"queue-{env}".encode()).hexdigest(),
        "type": "dns",
        "created_by": "data-fake",
        "labels": [
            {"key": "ipv4", "value": queue_ip},
            {"key": "domain", "value": f"queue-{env}.{domain}"},
            {"key": "queue", "value": f"queue-{env}"},
        ],
        "document": {
            "fqdn": f"queue-{env}.{domain}",
            "ipv4": queue_ip
        }
    }

    dns_s3_document = {
        "hash": hashlib.md5(f"s3-{env}".encode()).hexdigest(),
        "type": "dns",
        "created_by": "data-fake",
        "labels": [
            {"key": "ipv4", "value": s3_ip},
            {"key": "domain", "value": f"s3-{env}.{domain}"},
            {"key": "s3", "value": f"s3-{env}"},
        ],
        "document": {
            "fqdn": f"s3-{env}.{domain}",
            "ipv4": s3_ip
        }
    }

    dns_web_document = {
        "hash": hashlib.md5(f"web-{env}".encode()).hexdigest(),
        "type": "dns",
        "created_by": "data-fake",
        "labels": [
            {"key": "ipv4", "value": web_ip},
            {"key": "domain", "value": f"web-{env}.{domain}"},
            {"key": "web", "value": f"web-{env}"},
        ],
        "document": {
            "fqdn": f"web-{env}.{domain}",
            "ipv4": web_ip
        }
    }

    documents.append(dns_database_document)
    documents.append(dns_queue_document)
    documents.append(dns_s3_document)
    documents.append(dns_web_document)

    # database document
    database_document = {
        "hash": hashlib.md5(f"database-{env}".encode()).hexdigest(),
        "type": "database",
        "created_by": "data-fake",
        "labels": [
            {"key": "ipv4", "value": database_ip},
            {"key": "port", "value": "5432"},
            {"key": "domain", "value": f"database-{env}.{domain}"},
            {"key": "database", "value": f"database-{env}"},
        ],
        "document": {
            "name": f"database-{env}",
            "domain": domain
        }
    }

    # queue documento
    queue_document = {
        "hash": hashlib.md5(f"queue-{env}".encode()).hexdigest(),
        "type": "queue",
        "created_by": "data-fake",
        "labels": [
            {"key": "ipv4", "value": queue_ip},
            {"key": "port", "value": "5672"},
            {"key": "domain", "value": f"queue-{env}.{domain}"},
            {"key": "queue", "value": f"queue-{env}"},
        ]
    }

    # s3 documento
    s3_document = {
        "hash": hashlib.md5(f"s3-{env}".encode()).hexdigest(),
        "type": "s3",
        "created_by": "data-fake",
        "labels": [
            {"key": "ipv4", "value": s3_ip},
            {"key": "domain", "value": f"s3-{env}.{domain}"},
            {"key": "s3", "value": f"s3-{env}"},
        ]
    }

    # web documento
    web_document = {
        "hash": hashlib.md5(f"web-{env}".encode()).hexdigest(),
        "type": "web",
        "created_by": "data-fake",
        "labels": [
            {"key": "ipv4", "value": web_ip},
            {"key": "domain", "value": f"web-{env}.{domain}"},
            {"key": "web", "value": f"web-{env}-name"},
        ]
    }

    documents.append(database_document)
    documents.append(queue_document)
    documents.append(s3_document)
    documents.append(web_document)

    app_document = {
        "hash": hashlib.md5(f"{app_domain}.".encode()).hexdigest(),
        "type": "app",
        "created_by": "data-fake",
        "labels": [
            {"key": "ipv4", "value": balancer_ip},
            {"key": "domain", "value": app_domain},
            {"key": "database", "value": f"database-{env}.{domain}"},
            {"key": "queue", "value": f"queue-{env}.{domain}"},
            {"key": "s3", "value": f"s3-{env}.{domain}"},
            {"key": "web", "value": f"web-{env}.{domain}"}
        ],
        "document": {
            "name": f"app-{env}",
            "domain": app_domain,
            "requires": [
                f"database-{env}.{domain}",
                f"queue-{env}.{domain}",
                f"s3-{env}.{domain}",
                f"web-{env}.{domain}",
            ]
        }
    }

    documents.append(app_document)

    # balancer document
    balancer_document = {
        "hash": hashlib.md5(f"{env}".encode()).hexdigest(),
        "type": "balancer",
        "created_by": "data-fake",
        "labels": [
            {"key": "ipv4", "value": balancer_ip},
        ],
        "document": {
            "name": f"balancer-{env}",
            "ip": balancer_ip
        }

    }
    
    # server
    for app_server in range(1, 4):
        app_name = f"app-{app_server}"
        app_ip = f"{network}.{app_server}"

        hash = hashlib.md5(f"{env}{app_name}{app_ip}".encode()).hexdigest()


        app_server_ip = f"{network}.1.{app_server}"
        # server
        server_document = {
            "hash": hash,
            "type": "server",
            "created_by": "data-fake",
            "labels": [
                {"key": "ipv4", "value": app_server_ip}
            ],
        }

        balancer_document['labels'].append({"key": "ipv4", "value": app_server_ip})

        documents.append(server_document)
    
    documents.append(balancer_document)


with open("documents.json", "w") as f:
    json.dump(documents, f, indent=4)