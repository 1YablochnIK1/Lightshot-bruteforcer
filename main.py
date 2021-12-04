from configparser import ConfigParser
import threading, requests, random, string, sys, os
from time import sleep
import platform

try:
    if platform.system() == 'Windows':
        os.system('cls')
        os.system('title [Lightshot Bruteforcer] by 1YablochniK1 ^| V1.1 ^|')
        os.system("mode CON COLS=55 LINES=30")
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

headers = {
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}

cfg_path = "config.ini"

def red():
    return '\u001b[31;1m'

def green():
    return '\u001b[32;1m'

def reset():
    return '\u001b[0m'

def configC():
    config = ConfigParser()

    config["Lightshot-Bruteforcer"] = {
        "thread_count": "300",
        "save-img_path": "Images",
    }

    with open(cfg_path, "w") as f:
        config.write(f)

    configR()

def configR():
    try:
        global thc
        global saveimg_path

        parser = ConfigParser()
        parser.read(cfg_path)

        try:
            thc = int(parser.get('Lightshot-Bruteforcer', 'thread_count'))
            if thc > 1000:
                thc = 1000
            elif thc == 1000:
                thc = 1000
        except:
            thc = 300
        
        saveimg_path = parser.get('Lightshot-Bruteforcer', 'save-img_path')
        if not os.path.exists(saveimg_path): os.makedirs(saveimg_path)
    except:
        configC()
        configR()

def checkimg(arg):
    if 'image.prntscr' in arg: half_url = 'https://image.prntscr.com/image/'
    elif 'i.imgur' in arg: half_url = 'https://i.imgur.com/'
    r = os.stat(saveimg_path + "/" + arg.replace(half_url, '')[:6] + ".png").st_size
    if r == 6355:
        try:
            dd = saveimg_path + "/" + arg.replace(half_url, '')[:6] + ".png"
            os.remove(dd)
        except:
            pass
    elif r == 503:
        try:
            dd = saveimg_path + "/" + arg.replace(half_url, '')[:6] + ".png"
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
    old = valid + invalid
    sleep(1)
    new = valid + invalid
    return ((new - old) * 60)


def save(arg):
    content = requests.get(arg).content
    if 'image.prntscr' in arg: half_url = 'https://image.prntscr.com/image/'
    elif 'i.imgur' in arg: half_url = 'https://i.imgur.com/'
    with open(saveimg_path + "/" + arg.replace(half_url, '')[:6] + '.png', 'wb') as f: f.write(content)

def main(proxy):
    global valid
    global invalid
    global retries

    code = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
    try:
        check = requests.get(f'https://prnt.sc/{code}', headers = headers, proxies = {'https': 'http://%s' % (proxy)}).text
    except:
        retries += 1
    else:
        if 'name="twitter:image:src" content="' in check and not '0_173a7b_211be8ff' in check and not 'ml3U3Pt' in check:
            if thc > 300:
                lock.acquire(); sys.stdout.write('[%s+++%s] https://prnt.sc/%s\n' % (green(), reset(), code)); lock.release()
            elif thc == 300:
                lock.acquire(); sys.stdout.write('[%s+++%s] https://prnt.sc/%s\n' % (green(), reset(), code)); lock.release()
            else:
                print(f"[+++] https://print.sc/{code}")
            valid += 1
            url = check.split('name="twitter:image:src" content="')[1].split('"/> <meta')[0]
            save(url)
            with open('Image Links.txt', 'a', encoding = 'UTF-8') as f: f.write('https://prnt.sc/%s\n' % (code))
            checkimg(url)
        else:
            if thc > 300:
                lock.acquire(); sys.stdout.write('[%s---%s] https://prnt.sc/%s\n' % (red(), reset(), code)); lock.release()
            elif thc == 300:
                lock.acquire(); sys.stdout.write('[%s---%s] https://prnt.sc/%s\n' % (red(), reset(), code)); lock.release()
            else:
                print(f"[---] https://print.sc/{code}")
            invalid += 1
            #checkimg(url)

configR()

threading.Thread(target = grab_proxies).start()
threading.Thread(target = cpm).start()
sleep(3)

while True:
    if threading.active_count() <= thc:
        try:
            threading.Thread(target = main, args = (proxies[proxy_num],)).start()
            proxy_num += 1
            if proxy_num >= len(proxies):
                proxy_num = 0
        except:
            pass
