import nmap 

def scan_for_vulns(target,command):
    scanner = nmap.PortScanner()
    scan_results = scanner.scan(hosts=target, arguments=command)
    print(scan_results)
    return scan_results