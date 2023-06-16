from bson import json_util

def get_db_results(collection):
    # Obtiene todos los documentos de la colección
    cursor = collection.find()

    # Convierte el cursor a una lista de diccionarios
    data = [doc for doc in cursor]

    # Serializa los documentos a JSON
    json_data = json_util.dumps(data)

    print(json_data)

    return json_data
  