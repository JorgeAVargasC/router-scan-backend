from flask import Flask, jsonify
from flask_cors import CORS

#* ============ (Core functions) ============ *#

from utils.save_results_in_db import save_results_in_db
from utils.scan_for_vulns import scan_for_vulns
from utils.data_adapter import data_adapter
from utils.save_results_as_json import save_results_as_json
from utils.obtain_cve_info_from_api import obtain_cve_info_from_api
from utils.get_default_gateway import get_default_gateway
from utils.db_connection import db_connection
from utils.get_db_results import get_db_results
from utils.obtain_isp_info_from_api import obtain_isp_info_from_api

#* ========= API ========= *#

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/scan')
def scan():
    gateway = get_default_gateway()
    # gateway = get_real_default_gateway_docker()
    
    scan_results = scan_for_vulns(gateway, 'nmap -sV --script vulners')
    save_results_as_json(scan_results, '1-scan_results.json')
    
    scan_results_adapted = data_adapter(scan_results, gateway)
    scan_results_adapted = obtain_isp_info_from_api(scan_results_adapted)
    save_results_as_json(scan_results_adapted, '2-scan_results_adapted.json')

    if len(scan_results_adapted['vulnerabilities']) == 0:
        return jsonify(scan_results_adapted)
    
    scan_results_adapted_cve_info = obtain_cve_info_from_api(scan_results_adapted)  
    
    save_results_as_json(scan_results_adapted_cve_info, '3-scan_results_adapted_cve_info.json')
    
    collection = db_connection()
    save_results_in_db(collection, scan_results_adapted_cve_info)
    
    return jsonify(scan_results_adapted_cve_info)

@app.route('/scan/all')
def getAllScans():
    collection = db_connection()
    results = get_db_results(collection)
    
    return results
    

if __name__ == '__main__':
    app.run(debug=True,port=3000)



