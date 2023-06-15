from utils.obtain_severity_from_cvss import obtain_severity_from_cvss
import requests
import json

def obtain_cve_info_from_api(scan_results_adapted):
    url = 'https://cve.circl.lu/api/cve/'
    
    scan_results_adapted_cve_info = scan_results_adapted
    
    for index, vulnerability in enumerate(scan_results_adapted['vulnerabilities']):
        response = requests.get(f"{url}/{vulnerability['cve']}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(data)
                severity = obtain_severity_from_cvss(data['cvss'])
                scan_results_adapted_cve_info['vulnerabilities'][index]['id'] = data['id']
                scan_results_adapted_cve_info['vulnerabilities'][index]['cvss'] = data['cvss']
                scan_results_adapted_cve_info['vulnerabilities'][index]['severity'] = severity
                scan_results_adapted_cve_info['vulnerabilities'][index]['summary'] = data['summary']
                scan_results_adapted_cve_info['vulnerabilities'][index]['modified'] = data['Modified']
                scan_results_adapted_cve_info['vulnerabilities'][index]['published'] = data['Published']
                scan_results_adapted_cve_info['vulnerabilities'][index]['recommendations'] = data['capec']
            except json.decoder.JSONDecodeError:
                # Manejo del error de decodificación JSON
                # Aquí puedes agregar el código para manejar la situación en la que no se pueda decodificar la respuesta JSON
                pass
            
    return scan_results_adapted_cve_info