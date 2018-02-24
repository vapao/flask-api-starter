import ipaddress


def ip_validator(*address):
    try:
        for ip in address:
            ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False
