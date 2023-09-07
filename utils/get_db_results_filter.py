from flask import jsonify,request

def get_db_results_filter(collection):
    try:
        asn = request.get_json()['asn'] if 'asn' in request.get_json() else None
        userId = request.get_json()['userId'] if 'userId' in request.get_json() else None
        
        # Define un filtro basado en el ASN
        filter_query = {'connection.asn': {'$in': asn}} if asn else None
        
        filter_query_userId = {'userId': userId} if userId else None

        # projection = {'_id': 1, 'connection': 1}

        # Busca documentos que coincidan con el filtro en la colección
        cursor = collection.find(filter_query) if asn else collection.find(filter_query_userId)

        # Convierte el cursor a una lista de diccionarios
        data = [doc for doc in cursor]
        
        # Convierte los ObjectId a cadenas antes de serializar a JSON
        for doc in data:
            if '_id' in doc:
                doc['_id'] = str(doc['_id'])
                

        # sort data by date 
        
        data.sort(key=lambda x: x['timezone']['current_time'], reverse=True)

        return jsonify({
            "total": len(data),
            "data": data
            }), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'Error al obtener resultados con filtro'}), 500
  