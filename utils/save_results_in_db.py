def save_results_in_db(collection, data):
    try:
        # Convert data to a dictionary and remove the _id field
        data_dict = dict(data)
        data_dict.pop('_id', None)

        id = collection.insert_one(data_dict)

    except Exception as e:
        print(e)