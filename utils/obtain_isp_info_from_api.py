import requests
import json

def obtain_isp_info_from_api(scan_results_adapted):
    url = 'https://ipwho.is/'
    
    scan_results_adapted_isp_info = scan_results_adapted
    
    response = requests.get(f"{url}")
    
    if response.status_code == 200:
        try:
            data = response.json()
            print(data)
            scan_results_adapted_isp_info['ip'] = data['ip']
            scan_results_adapted_isp_info['continent'] = data['continent']
            scan_results_adapted_isp_info['continent_code'] = data['continent_code']
            scan_results_adapted_isp_info['country'] = data['country']
            scan_results_adapted_isp_info['country_code'] = data['country_code']
            scan_results_adapted_isp_info['region'] = data['region']
            scan_results_adapted_isp_info['region_code'] = data['region_code']
            scan_results_adapted_isp_info['city'] = data['city']
            scan_results_adapted_isp_info['latitude'] = data['latitude']
            scan_results_adapted_isp_info['longitude'] = data['longitude']
            scan_results_adapted_isp_info['flag'] = data['flag']
            scan_results_adapted_isp_info['connection'] = data['connection']
            scan_results_adapted_isp_info['timezone'] = data['timezone']
             
        except json.decoder.JSONDecodeError:
            # Manejo del error de decodificación JSON
            # Aquí puedes agregar el código para manejar la situación en la que no se pueda decodificar la respuesta JSON
            pass
            
    return scan_results_adapted_isp_info