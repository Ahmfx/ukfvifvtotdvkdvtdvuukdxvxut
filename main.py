from os import system, name, path
from random import choice
from base64 import b64decode
from asyncio import run
from requests import get
from telethon import TelegramClient, errors, functions
from telethon.sessions import StringSession
from telethon.tl.functions.account import CheckUsernameRequest
from telethon.tl.functions.channels import UpdateUsernameRequest, DeleteChannelRequest, CreateChannelRequest
from bs4 import BeautifulSoup as S
import aiohttp
import asyncio

YrUsername = "@arageDoctor" # يوزر حسابك التلي

def usernames():
    k = ''.join(choice('qwertyuiopasdfghjklzxcvbnm') for i in range(1))
    n = ''.join(choice('qwertyuiopasdfghjklzxcvbnm1234567890') for i in range(1))
    c = ''.join(choice('qwertyuiopasdfghjklzxcvbnm1234567890') for i in range(1))
    z = ''.join(choice('qwertyuiopasdfghjklzxcvbnm1234567890') for i in range(1))
    g = ''.join(choice('qwertyuiopasdfghjklzxcvbnm1234567890') for i in range(1))
    _ = ''.join("_")
    e = ''.join(choice('qwertyuiopasdfghjklzxcvbnm') for i in range(1))
    u1 = k + c + e + e + e
    u2 = k + z + z + z + n
    u3 = k + k + k + n + c
    u4 = k + k + k + _ + n
    u5 = k + _ + k + n + n
    u6 = k + k + _ + n + n
    u7 = k + k + n + _ + n
    u7 = k + _ + n + k + n
    u8 = k + n + _ + k + n
    u9 = k + n + k + _ + n
    u10 = k + n + n + k + n + k
    u11 = k + k + k + n + n + n
    u12 = n + k + k + k + ن + k
    u13 = ن + k + k + k + k + ن
    u14 = k + ن + ن + ن + k + k
    u15 = k + k + k + k + ن + ن
    u16 = k + k + k + k + ن + ن
    s = u1,u2,u3,u4,u5,u6,u7,u8,u9,u10,u11,u12,u13,u14,u15,u16
    return choice(s)

async def channels2(client, username):
    async for chat in client.iter_dialogs():
        if chat.name == f'[ {username} ]' and not chat.entity.username:
            await client(DeleteChannelRequest(channel=chat.entity))
            print('- Flood : ' + username + ' .')
            return False
    return True

async def fragment(username):
    proxy = '115.178.54.133:8080'  # ضع عنوان البروكسي هنا
    async with aiohttp.ClientSession(proxy=proxy) as session:
        url = f"https://fragment.com/username/{username}"
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.text()
                soup = S(data, 'html.parser')
                ok = soup.find("meta", property="og:description").get("content")
                if "An auction to get the Telegram" in ok or "Telegram and secure your ownership" in ok or "Check the current availability of" in ok or "Secure your name with blockchain in an ecosystem of 700+ million users" in ok:
                    return True
                elif "is taken" in ok:
                    return "is taken"
                else:
                    return False
            else:
                return False

async def claimed(client, username):
    result = await client(CreateChannelRequest(title=f'{username}', about='', megagroup=False))
    try:
        await client(UpdateUsernameRequest(channel=result.chats[0], username=username))
        await client.send_message(username, f'‹ تم الشخل وحفظ اليوزر ›\n‹ @{username} ›')
        return True
    except Exception as e:
        await client.send_message(YrUsername, f'⌯ Error Message .\nMessage : {e} .')
        return False

async def checker(username, client):
    try:
        check = await client(CheckUsernameRequest(username=username))
        if check:
            print('- Available : ' + username + ' .')
            claimer = await claimed(client, username)
            claim = claimer and (await fragment(username)) == "is taken"
            print('- Claimer ? ' + str(claim) + '\n' + '_ ' * 20)
            await client.send_message(YrUsername, f"‹ New UserName ›\n‹ UserName → @{username} ›\n‹ Claim → {claim} ›")
            flood = await channels2(client, username)
            if not flood:
                with open('flood.txt', 'a') as floodX: floodX.write(username + "\n")
            else:
                print('- Taken : ' + username + ' .')
    except errors.rpcbaseerrors.BadRequestError:
        print('- Error : ' + username + ' .')
        with open("banned4.txt", "a") as file:
            file.write(username + '\n')
    except errors.FloodWaitError as timer:
        print(f'- Flood Account [ {timer.seconds} Seconds ] .')
    except errors.UsernameInvalidError:
        print('- Invalid Username : ' + username + ' .')

async def start(client, username):
    try:
        ok = await fragment(username)
    except:
        return
    try:
        if not ok:
            await checker(username, client)
        elif ok == "is taken":
            print('- Taken : ' + username + ' .')
        else:
            print('- Fragment : ' + username + ' .')
            with open("fragment.txt", "a") as frag_file:
                frag_file.write(username + '\n')
    except Exception as e:
        print(e)

async def clienT():
    global sessionL
    try:
        client = TelegramClient(StringSession(sessionL), "28006651", "cc087eb52f8ec7819703ecd28f600e07")
        await client.start()
        print("Client started successfully")
    except Exception as e:
        print(f"Error starting client: {e}")
        exit()
    system('cls' if name == 'nt' else 'clear')
    return client

async def main():
    client = await clienT()
    if not path.exists('banned4.txt'): open('banned4.txt', 'w').close()
    if not path.exists('flood.txt'): open('flood.txt', 'w').close()
    if not path.exists('fragment.txt'): open('fragment.txt', 'w').close()
    while True:
        username = usernames()
        print(f"Checking username: {username}")
        file1 = open('banned4.txt', 'r').read() or ''
        file2 = open('fragment.txt', 'r').read() or ''
        if username in file1:
            print('- Banned : ' + username + ' .')
            continue
        if username in file2:
            print('- Fragment : ' + username + ' .')
            continue
        await start(client, username)

sessionL = input('[+] Enter Session : ')
run(main())
