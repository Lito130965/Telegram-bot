import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from pyromember.GetMembers import get_chat_members, get_chat_member
from config import BOT_TOKEN
from mongo.mongoDB import insert_member_to_db, get_all_members_from_db, set_emoji_to_user, get_all_members_id_from_db

#logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

members_list = get_all_members_from_db()
members_id_list = [mem_id['id'] for mem_id in get_all_members_id_from_db()]


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """ Message that bot will return when user using /start command """
    #await message.answer("Hello!")
    pass


@dp.message(Command("set_emoji"))
async def set_emoji(message: types.Message):
    """ This command let users set them personal emoji for @all command """
    global members_id_list
    global members_list
    members_list = get_all_members_from_db()
    members_id_list = [mem_id['id'] for mem_id in get_all_members_id_from_db()]
    if message.from_user.id not in members_id_list:
        insert_member_to_db(await get_chat_member(message.chat.id, message.from_user.id))
    try:
        emoji = message.text.split(' ', maxsplit=1)[1][0]
        set_emoji_to_user(int(message.from_user.id), emoji)
        #await message.react('✅')
        members_list = get_all_members_from_db()
        members_id_list = get_all_members_id_from_db()

        await message.reply('Your emoji was changed')
    except IndexError:
        await message.reply('Send the command and an emoji in one line\n'
                            'For example: /set_emoji 🐜')


@dp.message(Command("my_emoji"))
async def get_user_emoji(message: types.Message):
    """ This command return in message user's emoji for @all command """
    global members_list
    global members_id_list
    members_list = get_all_members_from_db()
    members_id_list = [mem_id['id'] for mem_id in get_all_members_id_from_db()]
    if message.from_user.id not in members_id_list:
        await message.reply(f'You have not set emoji\n'
                            f'Standard emoji is 🐜')
        insert_member_to_db(await get_chat_member(message.chat.id, message.from_user.id))
    else:
        for member in members_list:
            if member['id'] == message.from_user.id:
                try:
                    emoji = member['emoji']
                    await message.reply(f'Your emoji is {emoji}')
                    break
                except KeyError:
                    await message.reply(f'Your emoji is 🐜')


@dp.message(F.text)
async def message_monitoring(message: types.Message):
    """ If chat member sending a message with '@all' in, the bot will reply him tagged everyone
     by emoji """
    if '@all' in message.text:
        #if message.chat.type == 'group':
        if True:
            chat_id = message.chat.id
            members = await get_chat_members(chat_id)
            result = ''
            standard_emoji = '🐜'
            global members_list
            global members_id_list
            members_list = get_all_members_from_db()
            members_id_list = [mem_id['id'] for mem_id in get_all_members_id_from_db()]
            for member in members:
                if member.id not in members_id_list:
                    insert_member_to_db(await get_chat_member(message.chat.id, member.id))
                    members_list = get_all_members_from_db()
                    members_id_list = [mem_id['id'] for mem_id in get_all_members_id_from_db()]
                    emoji = standard_emoji

                else:
                    for user in members_list:
                        if int(member.id) == int(user['id']):
                            try:
                                emoji = user['emoji']
                            except KeyError:
                                emoji = standard_emoji
                            break
                result += f'[{emoji}](tg://user?id={str(member.id)})'
            await message.reply(result, parse_mode='MarkdownV2')


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())



