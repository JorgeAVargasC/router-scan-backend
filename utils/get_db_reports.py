from flask import jsonify


def get_db_reports(collection):
    try:
        # * ==================== (CVE) ===================== *#
        unique_cves = collection.distinct('vulnerabilities.cve')

        cve_counts = {}
        for cve in unique_cves:
            cve_counts[cve] = 0

        # Agregar una etapa de agregación para contar las repeticiones de cada CVE
        pipeline = [
            {
                '$group': {
                    '_id': '$ip',  # Agrupa por IP
                    # Cuenta cuántas veces se repite cada IP única
                    'count': {'$sum': 1},
                    # Agrega los documentos únicos a un conjunto
                    'unique_docs': {'$addToSet': '$$ROOT'}
                }
            },
            {
                '$match': {
                    # Filtra solo las IP que aparecen una vez (únicas)
                    'count': 1
                }
            },
            {
                '$unwind': '$unique_docs'  # Descomponer los documentos únicos
            },
            {
                '$unwind': '$unique_docs.vulnerabilities'  # Descomponer las vulnerabilidades
            },
            {
                '$group': {
                    '_id': '$unique_docs.vulnerabilities.id',  # Agrupa por CVE
                    # Cuenta cuántas veces se repite cada CVE
                    'count': {'$sum': 1}
                }
            }
        ]

        # Actualizar el diccionario de conteo con los resultados de la agregación
        cve_counts = list(collection.aggregate(pipeline))
        
        # Ordenar los resultados por el conteo de CVEs
        cve_counts.sort(key=lambda x: x['count'], reverse=True)
        
        
        # * ==================== (VENDOR) ===================== *#
        
        unique_vendors = collection.distinct('vulnerabilities.vendor')
        
        vendor_counts = {}
        for vendor in unique_vendors:
            vendor_counts[vendor] = 0
            
        pipeline = [
            {
                '$group': {
                    '_id': '$ip',  # Agrupa por IP
                    # Cuenta cuántas veces se repite cada IP única
                    'count': {'$sum': 1},
                    # Agrega los documentos únicos a un conjunto
                    'unique_docs': {'$addToSet': '$$ROOT'}
                }
            },
            {
                '$match': {
                    # Filtra solo las IP que aparecen una vez (únicas)
                    'count': 1
                }
            },
            {
                '$unwind': '$unique_docs'  # Descomponer los documentos únicos
            },
            {
                '$group': {
                    '_id': '$unique_docs.vendor',  # Agrupa por CVE
                    # Cuenta cuántas veces se repite cada CVE
                    'count': {'$sum': 1}
                }
            }
        ]
        
        vendor_counts = list(collection.aggregate(pipeline))
        
        # Ordenar los resultados por el conteo
        vendor_counts.sort(key=lambda x: x['count'], reverse=True)
        
        
        
        
        # * ==================== (ISP) ===================== *#
        
        unique_isp = collection.distinct('isp')
        
        isp_counts = {}
        for isp in unique_isp:
            isp_counts[isp] = 0
            
        pipeline = [
            {
                '$group': {
                    '_id': '$ip',  # Agrupa por IP
                    # Cuenta cuántas veces se repite cada IP única
                    'count': {'$sum': 1},
                    # Agrega los documentos únicos a un conjunto
                    'unique_docs': {'$addToSet': '$$ROOT'}
                }
            },
            {
                '$match': {
                    # Filtra solo las IP que aparecen una vez (únicas)
                    'count': 1
                }
            },
            {
                '$unwind': '$unique_docs'  # Descomponer los documentos únicos
            },
            {
                '$unwind': '$unique_docs.connection'  # Descomponer connection
            },
            {
                '$group': {
                    '_id': '$unique_docs.connection.isp',  # Agrupa por CVE
                    # Cuenta cuántas veces se repite cada CVE
                    'count': {'$sum': 1}
                }
            }
        ]
        
        isp_counts = list(collection.aggregate(pipeline))
        
        # Ordenar los resultados por el conteo
        isp_counts.sort(key=lambda x: x['count'], reverse=True)
        
        
        return jsonify({
            # "ips": ip_counts,
            "cve": {
                "count": len(cve_counts),
                "data": cve_counts
            },
            "vendor": {
                "count": len(vendor_counts),
                "data": vendor_counts
            },
            "isp" : {
                "count": len(isp_counts),
                "data": isp_counts
            }
            # "reports": data
        }), 200

    except Exception as e:
        print(e)
        return jsonify({'error': 'Error al obtener resultados con filtro'}), 500
