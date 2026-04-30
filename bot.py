import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = "@yourchannel"
ADMIN_ID = 123456789  # փոխի քո Telegram ID-ով

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

user_links = {}
users = set()  # user-ների պահում

# ✅ join check
async def is_joined(user_id):
    try:
        member = await bot.get_chat_member(CHANNEL, user_id)
        return member.status != "left"
    except:
        return False

# 🚀 START (նկարով)
@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    users.add(message.from_user.id)

    photo_url = "https://i.imgur.com/yourimage.jpg"  # քո նկարի link

    text = """🚀 Multi Downloader Bot

📥 Download from:
• YouTube
• TikTok
• Instagram

👇 Ուղարկի link"""

    await bot.send_photo(
        message.chat.id,
        photo=photo_url,
        caption=text
    )

# 📩 link handler
@dp.message_handler()
async def handle_msg(message: types.Message):
    users.add(message.from_user.id)

    if not await is_joined(message.from_user.id):
        kb = InlineKeyboardMarkup().add(
            InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{CHANNEL[1:]}")
        )
        await message.reply("Մուտք գործիր channel 👇", reply_markup=kb)
        return

    if "http" in message.text:
        user_links[message.from_user.id] = message.text

        kb = InlineKeyboardMarkup()
        kb.add(
            InlineKeyboardButton("🎵 MP3", callback_data="mp3"),
            InlineKeyboardButton("🎬 Video", callback_data="video")
        )

        await message.reply("Ընտրիր 👇", reply_markup=kb)
    else:
        await message.reply("Ուղարկի link 🙂")

# ⬇️ download
@dp.callback_query_handler()
async def download(call: types.CallbackQuery):
    url = user_links.get(call.from_user.id)

    if not url:
        await call.message.reply("Սխալ 😕")
        return

    msg = await call.message.reply("Քաշում եմ... ⏳")

    try:
        if call.data == "mp3":
            cmd = f'yt-dlp -x --audio-format mp3 --ffmpeg-location /usr/bin -o "%(title)s.%(ext)s" "{url}"'
        else:
            cmd = f'yt-dlp -f "best[ext=mp4][filesize<50M]" -o "%(title)s.%(ext)s" "{url}"'

        os.system(cmd)

        for file in os.listdir():
            if file.endswith((".mp3", ".mp4", ".mkv")):
                with open(file, "rb") as f:
                    await call.message.reply_document(f)
                os.remove(file)

    except:
        await call.message.reply("Սխալ ❌")

    await msg.delete()

# 📣 BROADCAST
@dp.message_handler(commands=["broadcast"])
async def broadcast(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    text = message.get_args()

    if not text:
        await message.reply("Գրի տեքստը 🙂")
        return

    count = 0

    for user_id in users:
        try:
            await bot.send_message(user_id, text)
            count += 1
        except:
            pass

    await message.reply(f"Ուղարկվեց {count} մարդուն ✅")

# 🚀 start
if __name__ == "__main__":
    executor.start_polling(dp)
