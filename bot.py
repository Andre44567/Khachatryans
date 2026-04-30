import os
import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

users = set()

# ===== START =====
@dp.message(CommandStart())
async def start(message: types.Message):
    users.add(message.chat.id)

    await message.answer_photo(
        photo="https://telegra.ph/file/6e7f0f9c1c2c3d4e5f6a7.jpg",  # քո նկար
        caption=(
            "👋 Բարի գալուստ\n\n"
            "📥 Ուղարկի link:\n"
            "• TikTok 🎥\n"
            "• YouTube 🎵\n"
            "• Instagram 📸\n\n"
            "📢 /broadcast text"
        )
    )

# ===== MESSAGE =====
@dp.message()
async def handler(message: types.Message):
    text = message.text or ""
    users.add(message.chat.id)

    # ===== BROADCAST =====
    if text.startswith("/broadcast "):
        msg = text.replace("/broadcast ", "")

        for user in users:
            try:
                await bot.send_message(user, msg)
            except:
                pass

        return await message.answer("✅ Ուղարկվեց բոլորին")

    # ===== TIKTOK =====
    if "tiktok.com" in text:
        try:
            url = text

            if "vt.tiktok.com" in text:
                async with aiohttp.ClientSession() as session:
                    async with session.get(text, allow_redirects=True) as res:
                        url = str(res.url)

            async with aiohttp.ClientSession() as session:
                async with session.get("https://tikwm.com/api/?url=" + url) as res:
                    data = await res.json()

            video = data["data"]["play"]

            return await message.answer_video(video, caption="🎥 TikTok")

        except:
            return await message.answer("❌ TikTok error")

    # ===== INSTAGRAM =====
    if "instagram.com" in text:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://igram.world/api/ig?url=" + text) as res:
                    data = await res.json()

            video = data["result"][0]["url"]

            return await message.answer_video(video, caption="📸 Instagram")

        except:
            return await message.answer("❌ Instagram error")

    # ===== YOUTUBE =====
    if "youtube.com" in text or "youtu.be" in text:
        link = "https://api.vevioz.com/api/button/mp3?url=" + text

        return await message.answer(
            "🎵 Քաշելու համար սեղմի 👇\n" + link
        )

    # ===== DEFAULT =====
    await message.answer("📩 Ուղարկի link կամ գրի /start")

# ===== RUN =====
async def main():
    await dp.start_polling(bot)

asyncio.run(main())
