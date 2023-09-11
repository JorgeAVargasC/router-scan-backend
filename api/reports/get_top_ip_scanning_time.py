from config.get_db_connection import get_db_connection
from flask import jsonify


def get_top_ip_scanning_time():
    try:
        db = get_db_connection()
        collection = db["router_scan_results"]

        # * ==================== (IP) ===================== *#

        pipeline = [
            {
                "$group": {
                    "_id": "$ip",
                    "scanning_time": {"$first": "$scanningTime"},
                }
            },
            {
                "$sort": {
                    "scanning_time": -1,
                }
            },
        ]

        ip_data = list(collection.aggregate(pipeline))
        # ip_data.sort(key=lambda x: x["count"], reverse=True)

        # calular tiempo promedio de escaneo
        total_time = 0
        for ip in ip_data:
            total_time += ip["scanning_time"]
        avg_time = total_time / len(ip_data)

        return (
            jsonify(
                {"count": len(ip_data), "avg": avg_time, "data": ip_data},
            ),
            200,
        )

    except Exception as e:
        print(e)
        return jsonify({"message": "Error"}), 500
