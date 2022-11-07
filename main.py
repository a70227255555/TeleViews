try:
	import requests,os,sys,logging,telethon, re, threading
	from telethon import events, Button, TelegramClient
except ImportError as e:
	os.system('pip install requests')
	os.system('pip install telethon=1.21.1')
try:os.system('pip install requests')
except:pass

logging.basicConfig(level=logging.INFO)

try:
    API_ID = int(os.environ.get("API_ID", 6))
    API_HASH = os.environ.get("API_HASH", None)
    TOKEN = os.environ.get("TOKEN", None)
except ValueError:
    print("You forgot to fullfill vars")
    print("Bot is quitting....")
    exit()
except Exception as e:
    print(f"Error - {str(e)}")
    print("Bot is quitting.....")
    exit()
except ApiIdInvalidError:
    print("Your API_ID or API_HASH is Invalid.")
    print("Bot is quitting.")
    exit()

bot = TelegramClient('bin', API_ID, API_HASH)
bin = bot.start(bot_token=TOKEN)
@bin.on(events.NewMessage(pattern="^[!?/]start$"))
link = input(' [/] Enter your url: ').strip().replace('https://', '').replace('http://', '')

_proxy_file = "proxy.txt"
_threads = int("1000")

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




async def start(event):
    if event.is_group:
        await event.reply("**Bin-Checker is Alive**")
        return
    await event.reply(f"**Heya {event.sender.first_name}**\nIts a Bin-Checker Bot To Check Your Bins Are Valid Or Not.", buttons=[
    [Button.url("Mʏ Sᴏᴜʀᴄᴇ Cᴏᴅᴇ", "https://t.me/SidraTools")]
    ])

@bin.on(events.NewMessage(pattern="^[!?/]help$"))

async def tit(): system("title " + f"TeleView By @Plugin / @yu5uy -- Stats: ({done}/{count_proxies}) -- Sent: {sent} -- Bad proxies: {bad_proxy}")

async def help(event):
    text = """
**Welcome to HelpMenu:**

- /start - To Start Me :)
- /help - To Get Help Menu
- /bin - To check is your bin valid or not
"""
    await event.reply(text, buttons=[[Button.url("Mʏ Sᴏᴜʀᴄᴇ Cᴏᴅᴇ", "https://github.com/TgxBotz/Bin-Checker")]])

@bin.on(events.NewMessage(pattern="^[!?/]bin"))
async def send_views():
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
