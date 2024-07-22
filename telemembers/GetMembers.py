from pyrogram import Client
from pyrogram import utils
from config import BOT_TOKEN

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

async def get_chat_members(chat_id) -> list:
    """ This function return all users tag, except bots """
    app = Client('LTest', bot_token=bot_token, in_memory=True)
    chat_members = []
    await app.start()
    async for member in app.get_chat_members(chat_id=int(chat_id)):
        if not member.user.is_bot:
            chat_members.append(f'@{member.user.username}')
    await app.stop()
    return chat_members

