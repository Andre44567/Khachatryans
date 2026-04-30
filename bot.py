import os
import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

users = set()

@dp.message()
async def handler(message: types.Message):
    text = message.text or ""
    users.add(message.chat.id)

    # START
    if text.startswith("/start"):
        return await message.answer(
            "👋 Բարի գալուստ\nՈւղարկի link"
        )

    # TIKTOK
    if "tiktok.com" in text:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://tikwm.com/api/?url=" + text) as res:
                    data = await res.json()

            video = data["data"]["play"]
            return await message.answer_video(video)
        except:
            return await message.answer("❌ TikTok error")

    # YOUTUBE
    if "youtube.com" in text or "youtu.be" in text:
        link = "https://api.vevioz.com/api/button/mp3?url=" + text
        return await message.answer(link)

    await message.answer("📩 Ուղարկի link")

async def main():
    await dp.start_polling(bot)

asyncio.run(main())
