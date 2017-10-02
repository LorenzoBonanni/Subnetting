from re import split
from sys import exit


def main():
    ip = "199.10.10.0"
    ip = ip.split('.')
    subnet = 6
    host = 8
    # class A
    if 0 < int(ip[0]) < 127:
        lista_ip = func(ip, subnet, host, 24, 1)
        ips = decimal_ip(lista_ip, 1)
    # class B
    elif 128 < int(ip[0]) < 191:
        lista_ip = func(ip, subnet, host, 16, 2)
        ips = decimal_ip(lista_ip, 2)
    # class C
    elif 192 < int(ip[0]) < 223:
        lista_ip = func(ip, subnet, host, 8, 3)
        ips = decimal_ip(lista_ip, 3)
    elif len(ip) > 4 or len(ip) < 4:
        print("invalid ip address")
        exit()
    else:
        print("invalid ip address")
        exit()
    for ip in ips:
        print(ip)

def func(ip, subnet, host, bits, pos):
    sub_bits = 0
    lista_sub = []
    lista_host = []
    lista_ip = []
    possibility = False
    for nb in range(0, bits):
        num = 2 ** nb
        if num > subnet:
            sub_bits = nb
            possibility = True
            break
    if not possibility:
        print("the number of subnet is too big for the ip address")
        exit()

    possibility = False
    for nb in range(0, bits - sub_bits):
        num = (2 ** nb) - 2
        if num > host:
            host_bits = nb
            possibility = True
            break
    if not possibility:
        print("the number of hosts is too big for the ip address \nor incopatible with the number of subnet")
        exit()
    subEhost = ""
    for i in range(pos, 4):
        ip[i] = '0' * 8
    for i in range(pos, 4):
        subEhost += ip[i]
    sub_n = subnet
    host_n = host
    subnet = subEhost[0:sub_bits]
    host = subEhost[sub_bits:host_bits]
    possibility = True
    while not (subnet == '1' * sub_bits):
        subnet = bin(int(subnet, 2) + int('1', 2))[2:]
        if possibility:
            possibility = False
            subnet = bin(int(subnet, 2) - int('1', 2))[2:]
        while not (len(subnet) == sub_bits):
            subnet = list(subnet)
            subnet.insert(0, '0')
            subnet = ''.join(str(e) for e in subnet)
        lista_sub.append(subnet)

    while not (host == '1' * (bits - sub_bits)):
        host = bin(int(host, 2) + int('1', 2))[2:]
        while not (len(host) == bits - sub_bits):
            host = list(host)
            host.insert(0, '0')
            host = ''.join(str(e) for e in host)
        lista_host.append(host)
    lista_host = lista_host[0:host_n]
    lista_sub = lista_sub[0:sub_n]
    for i in range(len(ip)):
        if int(ip[i]) == 0:
            del ip[i]
    for subs in lista_sub:
        for hosts in lista_host:
            ip2 = ''
            stringa = subs + hosts
            if len(stringa) == 8:
                ip.append(stringa)
                ip2 = '.'.join(str(e) for e in ip)
            # se maggiore spezzala di 8 in 8
            elif len(stringa) == 16:
                part1 = stringa[0:8]
                part2 = stringa[8:16]
                ip.append(part1)
                ip.append(part2)
                ip2 = '.'.join(str(e) for e in ip)
            else:
                part1 = stringa[0:8]
                part2 = stringa[8:16]
                part3 = stringa[16:32]
                ip.append(part1)
                ip.append(part2)
                ip.append(part3)
                ip2 = '.'.join(str(e) for e in ip)
            lista_ip.append(ip2)
            del ip[len(ip) - 1]
    return lista_ip

    print('host ', lista_host)
    print('sub ', lista_sub)


def decimal_ip(lista_ip, pos):
    ips = []
    for ip in lista_ip:
        ind_ip = ip.split('.')
        for i in range(3, pos-1, -1):
            num = ind_ip.pop(i)
            num = int(num, 2)
            ind_ip.insert(i, num)
            ind_ip = '.'.join(str(e) for e in ind_ip)
            ips.append(ind_ip)
    return ips


if __name__ == '__main__':
    main()
