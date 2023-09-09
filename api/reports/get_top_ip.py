from config.get_db_connection import get_db_connection
from flask import jsonify


def get_top_ip():
    try:
        db = get_db_connection()
        collection = db["router_scan_results"]

        # * ==================== (IP) ===================== *#

        pipeline = [
            {
                "$group": {
                    "_id": "$ip",
                    "count": {"$sum": 1},
                }
            },
            {
                "$sort": {
                    "count": -1,
                }
            },
        ]

        ip_data = list(collection.aggregate(pipeline))
        # ip_data.sort(key=lambda x: x["count"], reverse=True)

        return (
            jsonify(
                {"count": len(ip_data), "data": ip_data},
            ),
            200,
        )

    except Exception as e:
        print(e)
        return jsonify({"message": "Error"}), 500
