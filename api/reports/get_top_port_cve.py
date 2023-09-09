from config.get_db_connection import get_db_connection
from flask import jsonify


def get_top_port_cve():
    try:
        db = get_db_connection()
        collection = db["router_scan_results"]

        pipeline = [
            {
                "$unwind": "$vulnerabilities"
            },
            {
                "$group": {
                    "_id": {
                        "ip": "$ip",
                        "port": "$vulnerabilities.port"
                    },
                    "count": {"$sum": 1}
                }
            },
            {
                "$group": {
                    "_id": "$_id.port",
                    "total_vulnerabilities": {"$sum": "$count"}
                }
            },
        ]

        isp_data = list(collection.aggregate(pipeline))

        return jsonify({"count": len(isp_data), "data": isp_data}), 200

    except Exception as e:
        print(e)

        return jsonify({"message": f"Error: {e}"}), 500
