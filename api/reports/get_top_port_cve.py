from config.get_db_connection import get_db_connection
from flask import jsonify


def get_top_port_cve():
    try:
        db = get_db_connection()
        collection = db["router_scan_results"]

        pipeline = [
            {"$unwind": "$vulnerabilities"},
            {
                "$group": {
                    "_id": "$vulnerabilities.port",
                    "cve": {"$addToSet": "$vulnerabilities"},
                    "port_count": {"$sum": 1},
                }
            },
            {
                "$addFields": {
                    "cve_count": {"$size": "$cve"},
                    "cve_critical": {
                        "$size": {
                            "$filter": {
                                "input": "$cve",
                                "as": "cve",
                                "cond": {"$eq": ["$$cve.severity", "CRITICAL"]},
                            }
                        }
                    },
                    "cve_high": {
                        "$size": {
                            "$filter": {
                                "input": "$cve",
                                "as": "cve",
                                "cond": {"$eq": ["$$cve.severity", "HIGH"]},
                            }
                        }
                    },
                    "cve_medium": {
                        "$size": {
                            "$filter": {
                                "input": "$cve",
                                "as": "cve",
                                "cond": {"$eq": ["$$cve.severity", "MEDIUM"]},
                            }
                        }
                    },
                    "cve_low": {
                        "$size": {
                            "$filter": {
                                "input": "$cve",
                                "as": "cve",
                                "cond": {"$eq": ["$$cve.severity", "LOW"]},
                            }
                        }
                    },
                    "cve_none": {
                        "$size": {
                            "$filter": {
                                "input": "$cve",
                                "as": "cve",
                                "cond": {"$eq": ["$$cve.severity", "None"]},
                            }
                        }
                    },
                }
            },
            {
                "$project": {
                    "_id": 1,
                    "port": "$_id",
                    "cve": {
                        "cvss": 1,
                        "id": 1,
                        "port": 1,
                        "severity": 1,
                    },
                    "cve_count": 1,
                    "cve_critical": 1,
                    "cve_high": 1,
                    "cve_medium": 1,
                    "cve_low": 1,
                    "cve_none": 1,
                    "port_count": 1,
                }
            },
            {"$sort": {"cve_count": -1}},
        ]

        isp_data = list(collection.aggregate(pipeline))

        return jsonify({"count": len(isp_data), "data": isp_data}), 200

    except Exception as e:
        print(e)

        return jsonify({"message": f"Error: {e}"}), 500
