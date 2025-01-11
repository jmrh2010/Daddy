from telethon import TelegramClient, events, Button
from telethon.tl.functions.channels import GetParticipantsRequest, GetFullChannelRequest
from telethon.tl.types import ChannelParticipantsSearch, ChatAdminRights
import datetime
import os

token = ("7708671431:AAFaZYNrCFWm0quZ5Coe284jTxzqnfk-coU")
api_id = ("27430835")  # أضف ID الخاص بك هنا
api_hash = ("99a495c31546000c0768945e6d1e8953")  # أضف API Hash الخاص بك هنا

client = TelegramClient("L7N", api_id, api_hash).start(bot_token=token)

user_state = {}

async def removeall(username, count=None):
    if not username or not username.startswith('@'):
        return "- ارسل يوزر القناة مع **(@)**"

    try:
        channel = await client.get_entity(username)
        memsCh = await client(GetParticipantsRequest(
            channel, ChannelParticipantsSearch(''), 0, 100, hash=0
        ))

        users = memsCh.users
        up = 0

        for user in users:
            if count is not None and up >= count:
                break
            try:
                memCh = await client.get_permissions(channel, user.id)
                if not isinstance(memCh, ChatAdminRights):
                    await client.kick_participant(channel, user.id)
                    up += 1
                else:
                    pass
            except:
                continue
        
        return f"**- تم حذف :** `{up}` **من الاعضاء !**"
    except Exception as e:
        return str(e)

async def informationCh(username):
    if not username or not username.startswith('@'):
        return "- ارسل يوزر القناة مع **(@)**"

    try:
        channel = await client.get_entity(username)
        information = await client(GetFullChannelRequest(channel))
        name = information.chats[0].title
        
        participants_count = information.full_chat.participants_count
        if "@" in username:
            username = username.split("@")[1]
        return (
            f"""اسم القناة: [{name}](t.me/{username})
عدد الأعضاء: {participants_count}"""
        )
    except Exception as e:
        return str(e)

@client.on(events.NewMessage(pattern='/o'))
async def start(event):
    user_state[event.sender_id] = ""
    await event.respond(
        "- اهلا بك في بوت تفليش القنوات عن طريق توكن البوت ! ** اختر من الازرار :**",
        buttons=[
            [Button.inline('حذف عدد من الاعضاء')],
            [Button.inline('حذف كل الأعضاء')],
            [Button.inline('جلب معلومات القنوات')],
            [Button.inline('عرض الوقت')],
            [Button.url('مبرمج البوت', 'https://t.me/U_1_S')],
            [Button.url('قناة البرمجة', 'https://t.me/R_C_H')]
        ]
    )

@client.on(events.CallbackQuery(data='حذف عدد من الاعضاء'))
async def mem(event):
    user_state[event.sender_id] = "num"
    await event.respond("**- ارسل عدد الاعضاء الذي تريد حذفهم**")

@client.on(events.CallbackQuery(data='حذف كل الأعضاء'))
async def prompt_channel_for_all(event):
    user_state[event.sender_id] = "removeall"
    await event.respond("**أدخل معرف القناة لحذف جميع الأعضاء:**")

@client.on(events.CallbackQuery(data='جلب معلومات القنوات'))
async def prompt_channel_info(event):
    user_state[event.sender_id] = "chinfo"
    await event.respond("**أدخل معرف القناة للحصول على معلوماتها:**")

@client.on(events.CallbackQuery(data='عرض الوقت'))
async def show_time(event):
    times = datetime.datetime.now().strftime("%I:%M:%S")
    await event.respond(f"**- الوقت الان :** `{times}`")

@client.on(events.NewMessage)
async def handle_messages(event):
    user_id = event.sender_id
    user_input = event.message.text

    if user_id in user_state:
        state = user_state[user_id]

        if state == "num" and user_input.isdigit():
            user = int(user_input)
            user_state[user_id] = {'action': 'remove_some', 'count': user}
            await event.respond("- ارسل يوزر القناة مع **(@)**")
        
        elif state == "removeall" and user_input.startswith('@'):
            username = user_input
            response = await removeall(username)
            await event.respond(response)
            
        elif state == "chinfo" and user_input.startswith('@'):
            username = user_input
            info = await informationCh(username)
            await event.respond(info, link_preview=False)
            user_state.pop(user_id, None)
        
        elif isinstance(state, dict) and state.get('action') == 'remove_some' and user_input.startswith('@'):
            channel_username = user_input
            num = state.get('count')
            response = await removeall(channel_username, num)
            await event.respond(response)

client.run_until_disconnected()
