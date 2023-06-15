import json

def save_results_as_json(data,name):
    with open(name, 'w') as outfile:
        json.dump(data, outfile, indent=2)