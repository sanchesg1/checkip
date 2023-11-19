import socket
from ping3 import ping, verbose_ping

def check_ping(host):
    # Realiza un ping a la dirección IP
    try:
        response = ping(host, timeout=1)
        if response is not None:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error al realizar el ping a {host}: {str(e)}")
        return False

def scan_ports(host, ports):
    # Escanea los puertos especificados en la lista "ports"
    open_ports = []
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    return open_ports

def main():
    # lee la lista de ips desde un archivo que tenemos q crear previamente!!!!
    with open('lista_ips.txt', 'r') as file:
        ips = file.read().splitlines()

    # q puertos quiero escanear?
    ports_to_scan = [80, 443, 2000, 8291]

    # aca se crea el txt con el resultado de las ip
    output_file = open('ips_resultado.txt', 'w')

    for ip in ips:
        # hace ping
        if check_ping(ip):
            # si el ping da ok, scaneo puertos
            open_ports = scan_ports(ip, ports_to_scan)
#aca yo le agregue unos comentarios para saber el xq no se agrego alguna ip a la lista por x motivo, literalmente se podria ampliar/mejorar pero me da paja jeje, por ej para que por cada puierto q no responda que tire otro comment, pero fuckit
            if open_ports:
                print(f"La IP {ip} responde al ping y tiene puertos abiertos: {', '.join(map(str, open_ports))}")
                output_file.write(f"{ip}\n")
            else:
                print(f"La IP {ip} responde al ping pero no tiene puertos abiertos")
        else:
            print(f"La IP {ip} no responde al ping")

    output_file.close()
    print("se guardo todo en el txt de ips_resultado.txt")

if __name__ == "__main__":
    main()
