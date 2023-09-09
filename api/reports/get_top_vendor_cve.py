# from config.get_db_connection import get_db_connection
# from flask import jsonify


# def get_top_vendor_cve():
#     try:
#         db = get_db_connection()
#         collection = db["router_scan_results"]

#         # * ==================== (VENDOR) ===================== *#

#         unique_vendors = collection.distinct("vendor")

#         vendors_data = {}
#         for vendor in unique_vendors:
#             vendors_data[vendor] = 0

#         pipeline = [
#             {
#                 "$group": {
#                     "_id": "$ip",
#                     "ip_count": {"$sum": 1},
#                     "root": {"$addToSet": "$$ROOT"},
#                 }
#             },
#             {"$match": {"ip_count": 1}},
#             {"$unwind": "$root"},
#             {
#                 "$group": {
#                     "_id": "$root.vendor",
#                     "vendor_count": {"$sum": 1},
#                     "cve": {"$addToSet": "$root.vulnerabilities.id"},

#                 }
#             },
#             {
#                 "$project": {
#                     "_id": 1,
#                     "vendor_count": 1,
#                     "cve": {
#                         "$reduce": {
#                             "input": "$cve",
#                             "initialValue": [],
#                             "in": {"$setUnion": ["$$value", "$$this"]},
#                         }
#                     },
#                     "cve_count": {
#                         "$size": {
#                             "$reduce": {
#                                 "input": "$cve",
#                                 "initialValue": [],
#                                 "in": {"$setUnion": ["$$value", "$$this"]},
#                             }
#                         }
#                     },
#                 }
#             },
#             {
#                 "$sort": {
#                     "cve_count": -1,
#                 }
#             },
#         ]

#         vendors_data = list(collection.aggregate(pipeline))

#         return (
#             jsonify(
#                 {"count": len(vendors_data), "data": vendors_data},
#             ),
#             200,
#         )

#     except Exception as e:
#         print(e)
#         return jsonify({"message": f"Error: {e}" }), 500


# * NEW

from config.get_db_connection import get_db_connection
from flask import jsonify


def get_top_vendor_cve():
    try:
        db = get_db_connection()
        collection = db["router_scan_results"]

        # Obtener los datos únicos de los proveedores (vendors)
        unique_vendors = collection.distinct("vendor")

        vendors_data = {}
        for vendor in unique_vendors:
            vendors_data[vendor] = []

        pipeline = [
            {
                "$group": {
                    "_id": "$ip",
                    "ip_count": {"$sum": 1},
                    "root": {"$addToSet": "$$ROOT"},
                }
            },
            {"$match": {"ip_count": 1}},
            {"$unwind": "$root"},
            {
                "$group": {
                    "_id": "$root.vendor",
                    "vendor_count": {"$sum": 1},
                    "cve": {"$addToSet": "$root.vulnerabilities"},
                }
            },
            {
                "$project": {
                    "_id": 1,
                    "vendor_count": 1,
                    "cve": {
                        "$reduce": {
                            "input": "$cve",
                            "initialValue": [],
                            "in": {"$setUnion": ["$$value", "$$this"]},
                        }
                    },
                }
            },
            {
                "$unset": "cve.recommendations",  # Elimina la clave "recommendations" del campo "cve"
            },
            {
                "$unset": "cve.summary",
            },
            {
                "$unset": "cve.published",
            },
            {
                "$unset": "cve.modified",
            },
            {
                "$sort": {
                    "vendor_count": -1,
                }
            },
        ]

        vendors_data = list(collection.aggregate(pipeline))

        return jsonify({"count": len(vendors_data), "data": vendors_data}), 200

    except Exception as e:
        print(e)

        return jsonify({"message": f"Error: {e}"}), 500
