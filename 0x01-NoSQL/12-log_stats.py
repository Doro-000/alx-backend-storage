#!/usr/bin/env python3
""" Python script that provides some stats about Nginx logs stored in MongoDB """

from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient()
    main = client.logs.nginx
    method_C = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    status = main.count_documents({"method": "GET", "path": "/status"})
    print(f"{main.estimated_document_count()} logs")
    print("Methods:")
    for i in method_C:
        check = main.count_documents({"method": i})
        print(f"\tmethod {i}: {check}")
    print(f"{status} status check")
