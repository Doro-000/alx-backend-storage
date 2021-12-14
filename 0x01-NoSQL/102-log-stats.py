#!/usr/bin/env python3
""" nginx logs to mongo instance parser """

from pymongo import MongoClient, aggregation
from collections import Counter


if __name__ == "__main__":
    """ main process """
    client = MongoClient()
    main = client.logs.nginx
    method_C = {"GET": 0, "POST": 0, "PUT": 0, "PATCH": 0, "DELETE": 0}
    status = main.count_documents({"method": "GET", "path": "/status"})
    print(f"{main.estimated_document_count()} logs")
    print("Methods:")
    for i in method_C:
        check = main.count_documents({"method": i})
        print(f"\tmethod {i}: {check}")
    print(f"{status} status check")
    count = 0
    aggr = [{"$group": {"_id": '$ip', "c": {"$sum": 1}}}, {"$sort": {"c": -1}}]
    db = client.logs
    ip = {x["_id"]: x["c"] for x in db.nginx.aggregate(aggr)}
    print("IPs:")
    for key, value in ip.items():
        if count > 10:
            break
        count += 1
        print(f"\t{key}: {value}")
