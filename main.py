import requests, re, threading
from os import system

# ---------------
# Coded for you by @Plugin / @yu5uy
# First it will ask you for proxy file name for example: proxy.txt
# Then it will ask for post link for example: https://t.me/Avira/14
# Then how many threads you want for example: 350
# Note: Use [ HTTP / HTTPS ] Proxies only!

# Channel: t.me/Avira
# ---------------

system("title " + f"TeleView By @Plugin / @yu5uy")
print('''
   _____     _            _               
  /__   \___| | ___/\   /(_) _____      __
    / /\/ _ \ |/ _ \ \ / / |/ _ \ \ /\ / /
   / / |  __/ |  __/\ V /| |  __/\ V  V / 
   \/   \___|_|\___| \_/ |_|\___| \_/\_/  
         By: [  @Plugin / @yu5uy ]                         

''')
bot = telebot.TeleBot("TOKEN")
@bot.message_handler(commands=['/start']) 
bot.reply_to(msg,"ارسل 1 فراغ رابط المنشور",parse_mode="markdown")
_proxy_file = "proxy.txt"

_threads = int("1000")
link = input(' [/] Enter your url: ').strip().replace('https://', '').replace('http://', '')
main_url = f'https://{link}?embed=1'
views_url = 'https://t.me/v/?views='

proxies_file = open(str(_proxy_file), 'r').read()
proxies = proxies_file.splitlines()
count_proxies = len(proxies)
sent, bad_proxy, done, next_proxy = 0, 0, 0, 0

_headers = {
  'accept-language': 'en-US,en;q=0.9',
  'user-agent': 'Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36',
  'x-requested-with': 'XMLHttpRequest'
}


def tit(): system("title " + f"TeleView By @Plugin / @yu5uy -- Stats: ({done}/{count_proxies}) -- Sent: {sent} -- Bad proxies: {bad_proxy}")


def send_views():
    global sent, bad_proxy, done, next_proxy
    while True:
        try:
            proxy = proxies[next_proxy]
            next_proxy += 1
        except IndexError:
            break
        try:
            session = requests.session()
            session.proxies.update({'http': f'http://{proxy}', 'https': f'http://{proxy}'})
            session.headers.update(_headers)
            main_res = session.get(main_url).text
            _token = re.search('data-view="([^"]+)', main_res).group(1)
            views_req = session.get(views_url + _token)
            print(' [+] View Sent ' + 'Stats Code: '+str(views_req.status_code))
            sent += 1
            done += 1
            bot.reply_to(msg,"يتم الرشق…",parse_mode="markdown")
            tit()

        except requests.exceptions.ConnectionError:
            print(' [x] Bad Proxy: ' + proxy)
            bad_proxy += 1
            done += 1
            tit()


Threads = []
for t in range(_threads):
    x = threading.Thread(target=send_views)
    x.start()
    Threads.append(x)

for Th in Threads:
    Th.join()
