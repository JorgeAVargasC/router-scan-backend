from flask import jsonify

def get_db_results(collection):
    # Obtiene todos los documentos de la colección
    cursor = collection.find()

    # Convierte el cursor a una lista de diccionarios
    data = [doc for doc in cursor]

    for doc in data:
            if '_id' in doc:
                doc['_id'] = str(doc['_id'])
    
    # Serializa los documentos a JSON
    
    data.sort(key=lambda x: x['timezone']['current_time'], reverse=True)

    return jsonify(data), 200
  