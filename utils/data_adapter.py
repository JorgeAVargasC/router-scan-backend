def data_adapter(scan_results,gateway,userId):
    # mac = scan_results['scan'][gateway]['addresses']['mac']
    mac = scan_results['scan'][gateway]['addresses']['mac'] if 'mac' in scan_results['scan'][gateway]['addresses'] else '00:00:00:00:00:00' 
    tcp_ports = scan_results['scan'][gateway]['tcp']
    result = []

    for port in tcp_ports.keys():
        if 'script' in tcp_ports[port]:
            if 'vulners' in tcp_ports[port]['script']:
                vulners = tcp_ports[port]['script']['vulners'].split('\n')
                for index, vuln in enumerate(vulners):
                    if (('CVE' in vuln)):
                        if(':' not in vuln.split('\t')[1]):
                            result.append({
                                'cve': vulners[index].split('\t')[1],
                                'port': port
                            })
                        
    scan_results_adapted = {
        'userId': userId,
        'vendor': scan_results['scan'][gateway]['vendor'][mac] if mac in scan_results['scan'][gateway]['vendor'] else 'Unknown',
        'vulnerabilities': result
    }
    
    return scan_results_adapted