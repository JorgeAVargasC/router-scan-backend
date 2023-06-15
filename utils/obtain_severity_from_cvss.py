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