import qrcode
import os
import re
def ssidgen():
    os.system("ls -l /etc/NetworkManager/system-connections/")
    catt = input("Enter wifiName:")
    os.system(f" sudo cat /etc/NetworkManager/system-connections/{catt} > /tmp/wifi.txt",)
    f = open("/tmp/wifi.txt",'r')
    with f as open_file:
        data = open_file.read()
        reg = []
        reg = re.findall(r'ssid=.*',data)
        for i in reg:
            #print (i)
            return i
        return ssidgen()
def pskgen():
    # os.system("ls -l /etc/NetworkManager/system-connections/")
    # catt = input("Enter wifiName:")
    # os.system(f" sudo cat /etc/NetworkManager/system-connections/{catt} > /tmp/wifi.txt",)
    f = open("/tmp/wifi.txt",'r')
    with f as open_file:
        data = open_file.read()
        reg = []
        reg = re.findall(r'psk=.*',data)
        for i in reg:
            #print (i)
            return i
        return pskgen()
def authtype():
    # os.system("ls -l /etc/NetworkManager/system-connections/")
    # catt = input("Enter wifiName:")
    # os.system(f" sudo cat /etc/NetworkManager/system-connections/{catt} > /tmp/wifi.txt",)
    f = open("/tmp/wifi.txt",'r')
    with f as open_file:
        data = open_file.read()
        reg = []
        reg = re.findall(r'key-mgmt=.*',data)
        for i in reg:
            #print (i)
            return i
        return authtype()
