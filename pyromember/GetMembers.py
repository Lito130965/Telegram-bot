import json

from pyrogram import Client
from pyrogram import utils
from config import BOT_TOKEN, api_hash, api_id

bot_token = BOT_TOKEN


def get_peer_type_new(peer_id: int) -> str:
    """ Fix for pyrogram (Invalid chat ID) """
    peer_id_str = str(peer_id)
    if not peer_id_str.startswith("-"):
        return "user"
    elif peer_id_str.startswith("-100"):
        return "channel"
    else:
        return "chat"


utils.get_peer_type = get_peer_type_new

app = Client('LTest', bot_token=bot_token, api_id=api_id, api_hash=api_hash, in_memory=True)


async def start_app():
    try:
        await app.start()
    except:
        pass


async def get_chat_members(chat_id) -> list:
    """ This function return list of dicts with users info """
    chat_members = []
    await start_app()
    async for member in app.get_chat_members(chat_id=int(chat_id)):
        if not member.user.is_bot:
            chat_members.append(member.user)
    return chat_members


async def get_chat_member(chat_id, user_id) -> dict:
    """ This function return dict (in str) of user by chat and user ids """
    await start_app()
    result = await app.get_chat_member(chat_id=int(chat_id), user_id=int(user_id))
    return json.loads(str(result.user))
