from config.get_db_connection import get_db_connection
from flask import jsonify


def get_top_cve():
    try:
        db = get_db_connection()
        collection = db["router_scan_results"]

        # * ==================== (CVE) ===================== *#

        pipeline = [
            {
                "$group": {
                    "_id": "$ip",
                    "count": {"$sum": 1},
                    "root": {"$addToSet": "$$ROOT"},
                }
            },
            {"$match": {"count": 1}},
            {"$unwind": "$root"},
            {"$unwind": "$root.vulnerabilities"},
            {
                "$group": {
                    "_id": "$root.vulnerabilities.id",
                    "count": {"$sum": 1},
                }
            },
            {
                "$sort": {
                    "count": -1,
                }
            },
        ]

        cve_data = list(collection.aggregate(pipeline))
        # cve_data.sort(key=lambda x: x["count"], reverse=True)

        return (
            jsonify(
                {"count": len(cve_data), "data": cve_data},
            ),
            200,
        )

    except Exception as e:
        print(e)
        return jsonify({"message": "Error"}), 500
