import netifaces as ni
import nmap 
import json
import requests
from flask import Flask, jsonify
from flask_cors import CORS
#* ============ (Core functions) ============ *#

def get_default_gateway():
    gateways = ni.gateways()
    gateway = gateways['default'][ni.AF_INET][0]
    print(f"default gateway: { gateway }")
    return gateway

def get_real_default_gateway_docker():
    interfaces = ni.interfaces()
    print (interfaces)
    for interface in interfaces:
        if interface.startswith('eth'):
            iface_data = ni.ifaddresses(interface)
            print (iface_data)
            if ni.AF_INET in iface_data:
                for link in iface_data[ni.AF_INET]:
                    print (link)
                    if 'addr' in link:
                        print (link['addr'])
                        return link['addr']
        

def scan_for_vulns(target,command):
    scanner = nmap.PortScanner()
    scan_results = scanner.scan(hosts=target, arguments=command)
    print(scan_results)
    return scan_results

def data_adapter(scan_results,gateway):
    # mac = scan_results['scan'][gateway]['addresses']['mac']
    mac = scan_results['scan'][gateway]['addresses']['mac'] if 'mac' in scan_results['scan'][gateway]['addresses'] else '00:00:00:00:00:00' 
    tcp_ports = scan_results['scan'][gateway]['tcp']
    result = []

    for port in tcp_ports.keys():
        if 'script' in tcp_ports[port]:
            if 'vulners' in tcp_ports[port]['script']:
                vulners = tcp_ports[port]['script']['vulners'].split('\n')
                for index, vuln in enumerate(vulners):
                    if 'CVE' in vuln:
                        result.append({
                            'cve': vulners[index].split('\t')[1],
                            'port': port
                        })
                        
    scan_results_adapted = {
        'vendor': scan_results['scan'][gateway]['vendor'][mac] if mac in scan_results['scan'][gateway]['vendor'] else 'Unknown',
        'vulnerabilities': result
    }
    
    return scan_results_adapted

def obtain_severity_from_cvss(cvss):
    if cvss == 0.0:
        return 'NONE'
    elif 0.1 <= cvss <= 3.9:
        return 'LOW'
    elif 4 <= cvss <= 6.9:
        return 'MEDIUM'
    elif 7 <= cvss <= 8.9:
        return 'HIGH'
    elif cvss >= 9:
        return 'CRITICAL'

def obtain_cve_info_from_api(scan_results_adapted):
    url = 'https://cve.circl.lu/api/cve/'
    
    scan_results_adapted_cve_info = scan_results_adapted
    
    for index, vulnerability in enumerate(scan_results_adapted['vulnerabilities']):
        response = requests.get(f"{url}/{vulnerability['cve']}")
        data = response.json()
        
        if response.status_code == 200:
            scan_results_adapted_cve_info['vulnerabilities'][index]['id'] = data['id']
            scan_results_adapted_cve_info['vulnerabilities'][index]['cvss'] = data['cvss']
            scan_results_adapted_cve_info['vulnerabilities'][index]['severity'] = obtain_severity_from_cvss(data['cvss'])
            scan_results_adapted_cve_info['vulnerabilities'][index]['summary'] = data['summary']
            scan_results_adapted_cve_info['vulnerabilities'][index]['modified'] = data['Modified']
            scan_results_adapted_cve_info['vulnerabilities'][index]['published'] = data['Published']
            scan_results_adapted_cve_info['vulnerabilities'][index]['recommendations'] = data['capec']
            
    return scan_results_adapted_cve_info

def save_results_as_json(data,name):
    with open(name, 'w') as outfile:
        json.dump(data, outfile, indent=2)

#* ========= API ========= *#

app = Flask(__name__)
CORS(app)

gateway = get_real_default_gateway_docker()

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/scan')
def scan():
    gateway = get_default_gateway()
    # gateway = get_real_default_gateway_docker()
    
    scan_results = scan_for_vulns(gateway, 'nmap -sV --script vulners')
    save_results_as_json(scan_results,'1-scan_results.json')
    
    scan_results_adapted = data_adapter(scan_results,gateway)
    save_results_as_json(scan_results_adapted, '2-scan_results_adapted.json')

    if len(scan_results_adapted['vulnerabilities']) == 0:
        return jsonify(scan_results_adapted)
    
    scan_results_adapted_cve_info = obtain_cve_info_from_api(scan_results_adapted) 
    save_results_as_json(scan_results_adapted_cve_info, '3-scan_results_adapted_cve_info.json')
    
    return jsonify(scan_results_adapted_cve_info)

if __name__ == '__main__':
    app.run(debug=True)



