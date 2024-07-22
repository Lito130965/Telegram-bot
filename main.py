import asyncio
import logging

import aiogram.enums.parse_mode
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from GetMembers import get_chat_members
from config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """ Message that bot will return when user using /start command """
    await message.answer("Hello!")

@dp.message(F.text)
async def message_monitoring(message: types.Message):
    """ If administrator sending a message with '@all' in, the bot will return this message
     without '@all' and tag everyone bellow """
    if '@all' in message.text:
        if message.chat.type == 'group':
            chat_id = message.chat.id
            members = await get_chat_members(chat_id)
            result = ''
            for member in members:
                result += f'[🐜](tg://user?id={str(member.user.id)})'
            await message.answer(message.text.replace('@all', '') + f'\n\n {result}', parse_mode='MarkdownV2')
        else:
            await message.answer('@all command working only in group chat, not in private')
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())



