from config.get_db_connection import get_db_connection
from flask import jsonify


def get_top_isp():
    try:
        db = get_db_connection()
        collection = db["router_scan_results"]

        # * ==================== (ISP) ===================== *#

        unique_isp = collection.distinct("isp")

        isp_data = {}
        for isp in unique_isp:
            isp_data[isp] = 0

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
            {"$unwind": "$root.connection"},
            {"$group": {"_id": "$root.connection.isp", "count": {"$sum": 1}}},
            {
                "$sort": {
                    "count": -1,
                }
            },
        ]

        isp_data = list(collection.aggregate(pipeline))
        # isp_data.sort(key=lambda x: x["count"], reverse=True)

        return (
            jsonify(
                {"count": len(isp_data), "data": isp_data},
            ),
            200,
        )

    except Exception as e:
        print(e)
        return jsonify({"message": "Error"}), 500
