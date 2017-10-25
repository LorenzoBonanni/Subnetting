from sys import exit
import re


def main():
    ip = "199.10.10.0"
    if re.match('(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])', ip):
        ip = ip.split('.')
        subnet = 6
        host = 8
        # class A
        if 0 < int(ip[0]) < 127:
            # ip, subnet, host, bits, pos host
            lista_ip = func(ip, subnet, host, 24, 1)
            lista_ip = decimal_ip(lista_ip, 1)
        # class B
        elif 128 < int(ip[0]) < 191:
            # ip, subnet, host, bits, pos host
            lista_ip = func(ip, subnet, host, 16, 2)
            lista_ip = decimal_ip(lista_ip, 2)
        # class C
        elif 192 < int(ip[0]) < 223:
            # ip, subnet, host, bits, pos host
            lista_ip = func(ip, subnet, host, 8, 3)
            lista_ip = decimal_ip(lista_ip, 3)
        elif len(ip) > 4 or len(ip) < 4:
            print("invalid ip address")
            exit()
        else:
            print("invalid ip address")
            exit()
        for ip in lista_ip:
            print(ip)
    else:
        print("invalid ip address")
        exit()


def func(ip, subnet, host, bits, pos):
    sub_bits = 0
    lista_sub = []
    lista_host = []
    lista_ip = []
    possibility = False
    # check if the number of subnet requested is possible
    # if possible it finds the number of bits for subnets
    for nb in range(0, bits):
        # the number of possible subnets
        num = 2 ** nb
        # the number match the required number
        if num >= subnet:
            sub_bits = nb
            possibility = True
            break
    # possibility false
    if not possibility:
        print("the number of subnet is too big for the ip address")
        exit()
    possibility = False
    # check if the number of hosts requested is possible and compatible with subnet number
    # if possible it finds the number of bits for hosts
    for nb in range(0, bits - sub_bits):
        # the number of possible hosts
        num = (2 ** nb) - 2
        # the number match the required number
        if num >= host:
            host_bits = nb
            possibility = True
            break
    if not possibility:
        print("the number of hosts is too big for the ip address \nor incopatible with the number of subnet")
        exit()
    sub_and_host = ""
    # set the host bits to 0
    for i in range(pos, 4):
        ip[i] = '0' * 8
    # get only the subnet + hosts bits
    for i in range(pos, 4):
        sub_and_host += ip[i]
    # number of subnets
    sub_n = subnet
    # number of hosts
    host_n = host
    subnet = sub_and_host[0:sub_bits]
    # take the string of hosts from sub_and_host
    host = sub_and_host[sub_bits:host_bits]
    # get a list of the bits of each subnet
    lista_sub = get_subnets(subnet, sub_bits, lista_sub)[0:sub_n]
    # get a list of the bits of each host
    lista_host = get_hosts(host, bits, sub_bits, lista_host)[0:host_n]
    for i in range(len(ip)):
        if int(ip[i]) == 0:
            del ip[i]
    lista_ip = generate_addresses(lista_sub, lista_host, ip)
    return lista_ip


# translate the binary ip addresses to decimal
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


# return a list of all subnets makable with sub_bits
def get_subnets(subnet, sub_bits, lista_sub):
    possibility = True
    while subnet != ('1' * sub_bits):
        # add to subnet(bin) 1(bin)
        subnet = bin(int(subnet, 2) + int('1', 2))[2:]
        if possibility:
            possibility = False
            # remove from subnet(bin) 1(bin)
            subnet = bin(int(subnet, 2) - int('1', 2))[2:]
        while len(subnet) != sub_bits:
            # divide subnet in characters and put each character in a position
            subnet = list(subnet)
            # add 0 to reach the number of bits of subnet
            subnet.insert(0, '0')
            # campact all into a string
            subnet = ''.join(str(e) for e in subnet)
        # add subnet number(bin) to the list
        lista_sub.append(subnet)
    return lista_sub


# return a list of all hosts makable with bits - sub_bits
def get_hosts(host, bits, sub_bits, lista_host):
    while host != '1' * (bits - sub_bits):
        # add to host(bin) 1(bin)
        host = bin(int(host, 2) + int('1', 2))[2:]
        while len(host) != bits - sub_bits:
            # divide host in characters and put each character in a position
            host = list(host)
            # add 0 to reach the number of bits of host
            host.insert(0, '0')
            # campact all into a string
            host = ''.join(str(e) for e in host)
        # add subnet number(bin) to the list
        lista_host.append(host)
    return lista_host


# generate all ip address in binary
def generate_addresses(lista_sub, lista_host, ip):
    lista_ip = []
    # take each subnet from lista_sub
    for sub in lista_sub:
        # take each subnet from lista_host
        for host in lista_host:
            # reset ip2 to avoid more ip in the same string
            ip2 = ''
            stringa = sub + host
            if len(stringa) == 8:
                # add to the ip the string of subnet and host
                ip.append(stringa)
                # compact all into a string
                ip2 = '.'.join(str(e) for e in ip)
            # if lenght of stringa is more than 8 divide stringa in parts of 8 bits
            elif len(stringa) == 16:
                # divide stringa 8 by 8
                part1 = stringa[0:8]
                part2 = stringa[8:16]
                # add to the ip the string of subnet and host
                ip.append(part1)
                ip.append(part2)
                # compact all into a string
                ip2 = '.'.join(str(e) for e in ip)
            # if lenght of stringa is more than 8 divide stringa in parts of 8 bits
            else:
                # divide stringa 8 by 8
                part1 = stringa[0:8]
                part2 = stringa[8:16]
                part3 = stringa[16:32]
                # add to the ip the string of subnet and host
                ip.append(part1)
                ip.append(part2)
                ip.append(part3)
                # compact all into a string
                ip2 = '.'.join(str(e) for e in ip)
            # add the ip address to the list
            lista_ip.append(ip2)
            print(ip[len(ip) - 1])
            # delete the string of subnet and host from ip
            del ip[len(ip) - 1]
    return lista_ip


if __name__ == '__main__':
    main()
