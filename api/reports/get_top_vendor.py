from config.get_db_connection import get_db_connection
from flask import jsonify


def get_top_vendor():
    try:
        db = get_db_connection()
        collection = db["router_scan_results"]

        # * ==================== (VENDOR) ===================== *#

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
            {
                "$group": {
                    "_id": "$root.vendor",
                    "count": {"$sum": 1},
                }
            },
            {
                "$sort": {
                    "count": -1,
                }
            },
        ]

        vendors_data = list(collection.aggregate(pipeline))
        # vendors_data.sort(key=lambda x: x["count"], reverse=True)

        return (
            jsonify(
                {"count": len(vendors_data), "data": vendors_data},
            ),
            200,
        )

    except Exception as e:
        print(e)
        return jsonify({"message": "Error"}), 500
