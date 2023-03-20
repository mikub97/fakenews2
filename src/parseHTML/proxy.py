import optparse
import os, urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup

from src.parseHTML.anonimBrowser import anonimBrowser


def checkProxy(browser, printing=False):
    url = 'https://www.iplocation.net/find-ip-address'
    page = browser.open(url)
    soup = BeautifulSoup(page.read(), features="html5lib")
    table = soup.find_all('div', attrs={'class': 'col col_12_of_12'})[1]
    dict = {}
    names = table.findAll('th');
    values = table.findAll('td');
    i = 0
    for name in names:
        if name.text.encode('ascii', 'ignore') == 'IP Address':
            dict['IP Address'] = values[i].text.encode('ascii', 'ignore').replace(' [Hide this IP with VPN]', '')
        else:
            dict[name.text.encode('ascii', 'ignore')] = values[i].text.encode('ascii', 'ignore')
        i = i + 1
    if printing:
        for key, val in list(dict.items()):
            if (key.__len__() != 0):
                print((key + " - " + val))

    boolean = False
    for settings in browser.proxies:
        if (dict['IP Address'] == cutPortNumber(settings['http'])):
            return True
        else:
            return False


def cutPortNumber(string):
    pos = string.find(':')
    return string[:-(len(string) - pos)]


def main():
    parser = optparse.OptionParser('usage%prog ' + '-u <target url>')
    parser.add_option('-u', dest='address', type='string', help='specify proxy server')
    (options, args) = parser.parse_args()
    addr = options.address
    if (addr == None):
        print((parser.usage))
    else:
        hideme = {'https': addr, 'http': addr}
        ab = anonimBrowser([hideme])
        b=True
        try:
            b = checkProxy(browser=ab, printing=True)
            if not b:
                print('[-] Server Proxy is not working')
            else:
                print('[+] Everything is correct. Server Proxy is working')
        except Exception as e:
            print('[-] Server Proxy is not working')


if __name__ == '__main__':
    main()
