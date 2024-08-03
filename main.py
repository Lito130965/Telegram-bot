import asyncio
import logging
import random

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from pyromember.GetMembers import get_chat_members, get_chat_member
from config import BOT_TOKEN
from mongo.mongoDB import *

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

members_list = get_all_members_from_db()
members_id_list = [mem_id['id'] for mem_id in get_all_members_id_from_db()]


@dp.message(Command("info"))
async def cmd_start(message: types.Message):
    """ Message that bot will return when user using /info command """
    await message.answer("Hello everyone! \n"
                         "This bot was made for easy mention members from chat with some extra features:\n"
                         "/all - to mention all\n"
                         "/set_emoji - to set your personal emoji\n"
                         "/my_emoji - to check your emoji\n"
                         "/ignore - to enable or disable ignore mode*\n\n"
                         "*The bot will not to tag you when /all command works")


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


@dp.message(Command('all'))
async def all_command(message: types.Message):
    """ If chat member sending /all in chat, the bot will reply him tagged everyone
     by emoji """
    chat_id = message.chat.id
    members = await get_chat_members(chat_id)
    result = ''
    standard_emoji = '🐜'
    global members_list
    global members_id_list
    members_list = get_all_members_from_db()
    members_id_list = [mem_id['id'] for mem_id in get_all_members_id_from_db()]
    for member in members:
        emoji = None
        if member.id not in members_id_list:
            insert_member_to_db(await get_chat_member(message.chat.id, member.id))
            members_list = get_all_members_from_db()
            members_id_list = [mem_id['id'] for mem_id in get_all_members_id_from_db()]
            emoji = standard_emoji

        else:
            for user in members_list:
                try:
                    if user['ignore_mode'][str(message.chat.id)] == 1:
                        continue
                except KeyError:
                    pass
                if int(member.id) == int(user['id']):
                    try:
                        emoji = user['emoji']
                    except KeyError:
                        emoji = standard_emoji
                    break
        if emoji is not None:
            result += f'[{emoji}](tg://user?id={str(member.id)})'
    if result == '':
        await message.answer('Nobody was tagged')
    else:
        await message.answer(result, parse_mode='MarkdownV2')
        await message.react([{'type': 'emoji', 'emoji': random.choice(['🫡', '👍', '👌', '❤️', '🔥'])}])


@dp.message(Command('ignore'))
async def enable_or_disable_ignore(message: types.Message):
    """ With this command chat members can enable or disable ignor mode for chat """
    global members_id_list
    global members_list
    if message.from_user.id not in members_id_list:
        user = await get_chat_member(message.chat.id, message.from_user.id)
        insert_member_to_db(user)
        members_list = get_all_members_from_db()
        members_id_list = [mem_id['id'] for mem_id in get_all_members_id_from_db()]
        mode = 1
        await message.reply('Ignore mode was enabled for this chat')
    else:
        member_info = get_member_from_db(message.from_user.id)
        try:
            if member_info['ignore_mode'][str(message.chat.id)] == 0:
                mode = 1
                await message.reply('Ignore mode was enabled for this chat')
            else:
                mode = 0
                await message.reply('Ignore mode was disabled for this chat')
        except KeyError:
            mode = 1
            await message.reply('Ignore mode was enable for this chat')
    change_ignore_mode(user_id=message.from_user.id, chat_id=str(message.chat.id), mode=mode)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())



