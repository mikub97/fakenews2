import optparse
import os, urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
from src.parseHTML.anonimBrowser import anonimBrowser


def viewPage(browser,url):
    page = browser.open(url)
    source_code = page.read()
    print(source_code)

def printLinks(url):
    ab = anonimBrowser()
    ab.anonymize()
    page = ab.open(url)
    html = page.read()
    try:
        print('\n[+] Printing Links from BeautifulSoup')
        soup = BeautifulSoup(html,features="html5lib")
        links = soup.findAll(name='a')
        for link in links:
            if link.has_attr('href'):
                print(link['href'])
    except:
        pass;

def mirrorImages(url,dir):
    ab = anonimBrowser()
    ab.anonymize()
    html = ab.open(url)
    soup = BeautifulSoup(html,features='html5lib')
    image_tags = soup.findAll('img')
    for image in image_tags:
        filename = image['src'].lstrip('http://')
        print(( image['src']))
        filename = os.path.join(dir,filename.replace('/','_'))
        print('[+] Saving '+ str(filename))
        data = ab.open(image['src']).read()
        ab.back()
        save = open(filename,'wb')
        save.write(data)
        save.close()

def checkProxy(browser,printing=False):
    url = 'https://www.iplocation.net/find-ip-address'
    page = browser.open(url)
    soup = BeautifulSoup(page.read(),features="html5lib")
    table = soup.find_all('div', attrs={'class': 'col col_12_of_12'})[1]
    dict = {}
    names = table.findAll('th');
    values = table.findAll('td');
    i=0
    for name in names:
        if name.text.encode('ascii', 'ignore') == 'IP Address':
            dict['IP Address'] = values[i].text.encode('ascii','ignore').replace(' [Hide this IP with VPN]', '')
        else :
            dict[name.text.encode('ascii', 'ignore')] = values[i].text.encode('ascii', 'ignore')
        i=i+1
    if printing:
        for key, val in list(dict.items()):
            if (key.__len__() != 0):
                print(key + " - " + val)

    boolean = False
    for settings in browser.proxies:
        if (dict['IP Address'] == cutPortNumber(settings['http'])):
            boolean = True

    if (not boolean):
        return boolean

    cookie_tmp = 'COOKIE'
    for attempt in range(1,5):
        browser.anonymize()
        browser.clear_cookies()
        browser.open('http://kittenwar.com')
        for cookie in ab.cookiejar:
            boolean = (str(cookie) != cookie_tmp)
            cookie_tmp=str(cookie)
            if not boolean:
                return boolean
    return True



def cutPortNumber(string):
    pos = string.find(':')
    return string[:-(len(string)-pos)]


hideMeProxy = {'https': '189.1.16.162:23500','http': '189.1.16.162:23500'}
hideMeProxy1 = {'https': '85.114.142.173:3128','http': '85.114.142.173:3128'}
ab = anonimBrowser([hideMeProxy,hideMeProxy1])

def main():
    parser = optparse.OptionParser('usage%prog ' + '-u <target url> -d <destination directory>')
    parser.add_option('-u',dest = 'tgtURL', type='string',help='specify target url')
    parser.add_option('-d',dest = 'dir',type='string', help = 'specify destinantion directory')
    (options, args) = parser.parse_args()
    url = options.tgtURL
    dir = options.dir
    if(url == None) or dir ==None:
        print((parser.usage))
    else:
        printLinks(url)
        try:
            mirrorImages(url,dir)
        except Exception as e :
            print('[-] Error Mirroring Images.')
            print('[-] ' + str(e))
if __name__ == '__main__':
    main()
print(checkProxy(ab))
