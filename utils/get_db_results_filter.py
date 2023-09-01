from flask import jsonify,request

def get_db_results_filter(collection):
    try:
        asn = request.get_json()['asn']
        
        # Define un filtro basado en el ASN
        filter_query = {'connection.asn': {'$in': asn}}

        projection = {'_id': 1, 'connection': 1}

        # Busca documentos que coincidan con el filtro en la colección
        cursor = collection.find(filter_query,projection)

        # Convierte el cursor a una lista de diccionarios
        data = [doc for doc in cursor]
        
        # Convierte los ObjectId a cadenas antes de serializar a JSON
        for doc in data:
            if '_id' in doc:
                doc['_id'] = str(doc['_id'])

        return jsonify({
            "total": len(data),
            "data": data
            }), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'Error al obtener resultados con filtro'}), 500
  