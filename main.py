import os
import re
import sys
import m3u8
import json
import time
import pytz
import asyncio
import requests
import subprocess
import urllib
import urllib.parse
import yt_dlp
import tgcrypto
import cloudscraper
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64encode, b64decode
from logs import logging
from bs4 import BeautifulSoup
import saini as helper
from utils import progress_bar
from vars import API_ID, API_HASH, BOT_TOKEN, OWNER, CREDIT, AUTH_USERS
from aiohttp import ClientSession
from subprocess import getstatusoutput
from pytube import YouTube
from aiohttp import web
import random
from pyromod import listen
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import aiohttp
import aiofiles
import zipfile
import shutil
import ffmpeg

# Initialize the bot
bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

cookies_file_path = os.getenv("cookies_file_path", "youtube_cookies.txt")
api_url = "http://master-api-v3.vercel.app/"
api_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNzkxOTMzNDE5NSIsInRnX3VzZXJuYW1lIjoi4p61IFtvZmZsaW5lXSIsImlhdCI6MTczODY5MjA3N30.SXzZ1MZcvMp5sGESj0hBKSghhxJ3k1GTWoBUbivUe1I"
token_cp = "eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJpZCI6MTU0MTcxNTczLCJvcmdJZCI6NTY4ODI5LCJ0eXBlIjoxLCJtb2JpbGUiOiI5MTk5NTU1Mzk5MjkiLCJuYW1lIjoiU2hpdmFuc2giLCJlbWFpbCI6Imh0bTdkYjZyc2JAb2Frb24uY29tIiwiaXNGaXJzdExvZ2luIjp0cnVlLCJkZWZhdWx0TGFuZ3VhZ2UiOiJFTiIsImNvdW50cnlDb2RlIjoiSU4iLCJpc0ludGVybmF0aW9uYWwiOjAsImlzRGl5Ijp0cnVlLCJsb2dpblZpYSI6Ik90cCIsImZpbmdlcnByaW50SWQiOiJkNzkxMTExMjBlNTg0MzkzYjYxNjhkZDBlNGEwYzQ4ZiIsImlhdCI6MTc1MDI1NTQ5NiwiZXhwIjoxNzUwODYwMjk2fQ.HhGiHsaf9mCfdHwbCLvAk4VZUPOwWp4Fqt2iWt_U7_Dpb0bW0GW444Ua4k3F3t4f"
adda_token = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJkcGthNTQ3MEBnbWFpbC5jb20iLCJhdWQiOiIxNzg2OTYwNSIsImlhdCI6MTc0NDk0NDQ2NCwiaXNzIjoiYWRkYTI0Ny5jb20iLCJuYW1lIjoiZHBrYSIsImVtYWlsIjoiZHBrYTU0NzBAZ21haWwuY29tIiwicGhvbmUiOiI3MzUyNDA0MTc2IiwidXNlcklkIjoiYWRkYS52MS41NzMyNmRmODVkZDkxZDRiNDkxN2FiZDExN2IwN2ZjOCIsImxvZ2luQXBpVmVyc2lvbiI6MX0.0QOuYFMkCEdVmwMVIPeETa6Kxr70zEslWOIAfC_ylhbku76nDcaBoNVvqN4HivWNwlyT0jkUKjWxZ8AbdorMLg"
photologo = 'https://tinypic.host/images/2025/02/07/DeWatermark.ai_1738952933236-1.png' #https://envs.sh/GV0.jpg
photoyt = 'https://tinypic.host/images/2025/03/18/YouTube-Logo.wine.png' #https://envs.sh/GVi.jpg
photocp = 'https://tinypic.host/images/2025/03/28/IMG_20250328_133126.jpg'
photozip = 'https://envs.sh/cD_.jpg'


# Inline keyboard for start command
BUTTONSCONTACT = InlineKeyboardMarkup([[InlineKeyboardButton(text="📞 Contact", url="https://t.me/i_am_back143")]])
keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="👨‍💻 🌐 OWNER ID 🌐", url="https://t.me/Strangerboy27_bot_strangerboy"),
            InlineKeyboardButton(text="🛠️ GROUP 🙋‍♂️", url="https://t.me/+aBB53vou0Z5hZWI1"),
        ],
        [
            InlineKeyboardButton(text="💠 CRUSH 💠", url="https://i.ibb.co/ccV44ZRS/STRANGER-BOY.jpg"),
        ],[
            InlineKeyboardButton(text=" 💠 INSTAGRAM🙋‍♂️💠", url="https://www.instagram.com/reel/DKfu0A0tSHO/?igsh=MzRlODBiNWFlZA=="),
        ],
    ]
)


# Image URLs for the random image feature
image_urls = [
    "https://envs.sh/wt.jpg",
    "https://envs.sh/wu.jpg",
    "https://envs.sh/w2.jpg",
    "https://envs.sh/wd.jpg",
    "https://i.ibb.co/ccV44ZRS/STRANGER-BOY.jpg",
    "https://i.ibb.co/0p3pmkwn/Angel.jpg",
    "https://i.ibb.co/7xm7cXyg/STRANGER-BOY.jpg",
    "https://i.ibb.co/wryWJwn5/STRANGER-BOY.jpg",
    "https://i.ibb.co/pCtQngf/STRANGER-BOY.jpg",
    "https://i.ibb.co/gMJHZgz4/STRANGER-BOY.jpg",
    "https://i.ibb.co/ZRvCxd5g/STRANGER-BOY.jpg",
    # Add more image URLs as needed
]

@bot.on_message(filters.command("addauth") & filters.private)
async def add_auth_user(client: Client, message: Message):
    if message.chat.id != OWNER:
        return await message.reply_text("You are not authorized to use this command.")
    
    try:
        new_user_id = int(message.command[1])
        if new_user_id in AUTH_USERS:
            await message.reply_text("User ID is already authorized.")
        else:
            AUTH_USERS.append(new_user_id)
            await message.reply_text(f"User ID {new_user_id} added to authorized users.")
    except (IndexError, ValueError):
        await message.reply_text("Please provide a valid user ID.")

@bot.on_message(filters.command("users") & filters.private)
async def list_auth_users(client: Client, message: Message):
    if message.chat.id != OWNER:
        return await message.reply_text("You are not authorized to use this command.")
    
    user_list = '\n'.join(map(str, get_all_user_ids()))  # Get user IDs from MongoDB
    await message.reply_text(f"Authorized Users:\n{user_list}")

@bot.on_message(filters.command("rmauth") & filters.private)
async def remove_auth_user(client: Client, message: Message):
    if message.chat.id != OWNER:
        return await message.reply_text("You are not authorized to use this command.")
    
    try:
        user_id_to_remove = int(message.command[1])
        if user_id_to_remove not in AUTH_USERS:
            await message.reply_text("User ID is not in the authorized users list.")
        else:
            AUTH_USERS.remove(user_id_to_remove)
            await message.reply_text(f"User ID {user_id_to_remove} removed from authorized users.")
    except (IndexError, ValueError):
        await message.reply_text("Please provide a valid user ID.")
    
        
@bot.on_message(filters.command("cookies") & filters.private)
async def cookies_handler(client: Client, m: Message):
    await m.reply_text(
        "Please upload the cookies file (.txt format).",
        quote=True
    )

    try:
        # Wait for the user to send the cookies file
        input_message: Message = await client.listen(m.chat.id)

        # Validate the uploaded file
        if not input_message.document or not input_message.document.file_name.endswith(".txt"):
            await m.reply_text("Invalid file type. Please upload a .txt file.")
            return

        # Download the cookies file
        downloaded_path = await input_message.download()

        # Read the content of the uploaded file
        with open(downloaded_path, "r") as uploaded_file:
            cookies_content = uploaded_file.read()

        # Replace the content of the target cookies file
        with open(cookies_file_path, "w") as target_file:
            target_file.write(cookies_content)

        await input_message.reply_text(
            "✅ Cookies updated successfully.\n📂 Saved in `youtube_cookies.txt`."
        )

    except Exception as e:
        await m.reply_text(f"⚠️ An error occurred: {str(e)}")

@bot.on_message(filters.command(["t2t"]))
async def text_to_txt(client, message: Message):
    user_id = str(message.from_user.id)
    # Inform the user to send the text data and its desired file name
    editable = await message.reply_text(f"<blockquote>Welcome to the Text to .txt Converter!\nSend the **text** for convert into a `.txt` file.</blockquote>")
    input_message: Message = await bot.listen(message.chat.id)
    if not input_message.text:
        await message.reply_text("🚨 **error**: Send valid text data")
        return

    text_data = input_message.text.strip()
    await input_message.delete()  # Corrected here
    
    await editable.edit("**🔄 Send file name or send /d for filename**")
    inputn: Message = await bot.listen(message.chat.id)
    raw_textn = inputn.text
    await inputn.delete()  # Corrected here
    await editable.delete()

    if raw_textn == '/d':
        custom_file_name = 'txt_file'
    else:
        custom_file_name = raw_textn

    txt_file = os.path.join("downloads", f'{custom_file_name}.txt')
    os.makedirs(os.path.dirname(txt_file), exist_ok=True)  # Ensure the directory exists
    with open(txt_file, 'w') as f:
        f.write(text_data)
        
    await message.reply_document(document=txt_file, caption=f"`{custom_file_name}.txt`\n\nYou can now download your content! 📥")
    os.remove(txt_file)

# Define paths for uploaded file and processed file
UPLOAD_FOLDER = '/path/to/upload/folder'
EDITED_FILE_PATH = '/path/to/save/edited_output.txt'

@bot.on_message(filters.command(["y2t"]))
async def youtube_to_txt(client, message: Message):
    user_id = str(message.from_user.id)
    
    editable = await message.reply_text(
        f"Send YouTube Website/Playlist link for convert in .txt file"
    )

    input_message: Message = await bot.listen(message.chat.id)
    youtube_link = input_message.text.strip()
    await input_message.delete(True)
    await editable.delete(True)

    # Fetch the YouTube information using yt-dlp with cookies
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'skip_download': True,
        'force_generic_extractor': True,
        'forcejson': True,
        'cookies': 'youtube_cookies.txt'  # Specify the cookies file
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            result = ydl.extract_info(youtube_link, download=False)
            if 'entries' in result:
                title = result.get('title', 'youtube_playlist')
            else:
                title = result.get('title', 'youtube_video')
        except yt_dlp.utils.DownloadError as e:
            await message.reply_text(
                f"<pre><code>🚨 Error occurred {str(e)}</code></pre>"
            )
            return

    # Extract the YouTube links
    videos = []
    if 'entries' in result:
        for entry in result['entries']:
            video_title = entry.get('title', 'No title')
            url = entry['url']
            videos.append(f"{video_title}: {url}")
    else:
        video_title = result.get('title', 'No title')
        url = result['url']
        videos.append(f"{video_title}: {url}")

    # Create and save the .txt file with the custom name
    txt_file = os.path.join("downloads", f'{title}.txt')
    os.makedirs(os.path.dirname(txt_file), exist_ok=True)  # Ensure the directory exists
    with open(txt_file, 'w') as f:
        f.write('\n'.join(videos))

    # Send the generated text file to the user with a pretty caption
    await message.reply_document(
        document=txt_file,
        caption=f'<a href="{youtube_link}">__**Click Here to Open Link**__</a>\n<pre><code>{title}.txt</code></pre>\n'
    )

    # Remove the temporary text file after sending
    os.remove(txt_file)


m_file_path= "main.py"
@bot.on_message(filters.command("rjgetcookies") & filters.private)
async def getcookies_handler(client: Client, m: Message):
    try:
        # Send the cookies file to the user
        await client.send_document(
            chat_id=m.chat.id,
            document=cookies_file_path,
            caption="Here is the `youtube_cookies.txt` file."
        )
    except Exception as e:
        await m.reply_text(f"⚠️ An error occurred: {str(e)}")     
@bot.on_message(filters.command("rjmfile") & filters.private)
async def getcookies_handler(client: Client, m: Message):
    try:
        await client.send_document(
            chat_id=m.chat.id,
            document=m_file_path,
            caption="Here is the `main.py` file."
        )
    except Exception as e:
        await m.reply_text(f"⚠️ An error occurred: {str(e)}")

@bot.on_message(filters.command(["stop"]) )
async def restart_handler(_, m):
    if m.chat.id not in AUTH_USERS:
        print(f"User ID not in AUTH_USERS", m.chat.id)
        await bot.send_message(
            m.chat.id, 
            f"<blockquote>__**Oopss! You are not a Premium member**__\n"
            f"__**PLEASE /upgrade YOUR PLAN**__\n"
            f"__**Send me your user id for authorization**__\n"
            f"__**Your User id** __- `{m.chat.id}`</blockquote>\n\n"
        )
    else:
        await m.reply_text("🚦**STOPPED**🚦", True)
        os.execl(sys.executable, sys.executable, *sys.argv)
        

@bot.on_message(filters.command("start"))
async def start(bot, m: Message):
    user = await bot.get_me()
    mention = user.mention
    start_message = await bot.send_message(
        m.chat.id,
        f"🌟 Welcome {m.from_user.first_name}! 🌟\n\n"
    )

    await asyncio.sleep(1)
    await start_message.edit_text(
        f"🌟 Welcome {m.from_user.first_name}! 🌟\n\n" +
        f"Initializing Uploader bot... 🤖\n\n"
        f"Progress: [⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️] 0%\n\n"
        f"╭━━━━━━ INITIALIZING ━━━━━━➣\n"
        f"┣⪼ 🔄 System Status:\n"
        f"┃  ├─⪼ 📡 Connecting to servers...\n"
        f"┃  ╰─⪼ ⚙️ Loading modules...\n"
        f"┣⪼ 📊 Progress: ▰▱▱▱▱▱▱▱▱▱ 10.1%\n"
        f"╰━━━━━━━━━━━━━━━━━━━━➣\n"
    )

    await asyncio.sleep(1)
    await start_message.edit_text(
        f"🌟 Welcome {m.from_user.first_name}! 🌟\n\n" +
        f"Loading features... ⏳\n\n"
        f"Progress: [🟥🟥🟥⬜️⬜️⬜️⬜️⬜️⬜️⬜️] 25%\n\n"
        f"╭━━━━━━ LODING ━━━━━━➣\n"
        f"┣⪼ 🔄 System Status:\n"
        f"┃  ├─⪼ 📡 Connecting to servers...\n"
        f"┃  ╰─⪼ ⚙️ Loading modules...\n"
        f"┣⪼ 📊 Progress: ▰▰▰▱▱▱▱▱▱ 33.03%\n"
        f"╰━━━━━━━━━━━━━━━━━━━━➣\n"
    )
    
    await asyncio.sleep(1)
    await start_message.edit_text(
        f"🌟 Welcome {m.from_user.first_name}! 🌟\n\n" +
        f"This may take a moment, sit back and relax! 😊\n\n"
        f"Progress: [🟧🟧🟧🟧🟧⬜️⬜️⬜️⬜️⬜️] 50%\n\n"
        f"╭━━━━━━ PREPARING ━━━━━━➣\n"
        f"┣⪼ 🔄 System Status:\n"
        f"┃  ├─⪼ 📡 Connecting to servers...\n"
        f"┃  ╰─⪼ ⚙️ Loading modules...\n"
        f"┣⪼ 📊 Progress: ▰▰▰▰▰▰▱▱▱▱ 65.33%\n"
        f"╰━━━━━━━━━━━━━━━━━━━━➣\n"
    )

    await asyncio.sleep(1)
    await start_message.edit_text(
        f"🌟 Welcome {m.from_user.first_name}! 🌟\n\n" +
        f"Checking subscription status... 🔍\n\n"
        f"Progress: [🟨🟨🟨🟨🟨🟨🟨🟨⬜️⬜️] 75%\n\n"
        f"╭━━━━━━ FINALIZING ━━━━━━➣\n"
       f"┣⪼ 🔄 System Status:\n"
       f"┃  ├─⪼ ✅ Security verified\n"
       f"┃  ├─⪼ ✅ Data synced\n"
       f"┃  ╰─⪼ 🔍 Checking access...\n"
       f"┣⪼ 📊 Progress: ▰▰▰▰▰▰▰▰▰▱ 75.9%\n"
       f"╰━━━━━━━━━━━━━━━━━━━━➣\n"
        
    )

    await asyncio.sleep(1)
    if m.chat.id in AUTH_USERS:
        await start_message.edit_text(
            f"🌟 Welcome {m.from_user.first_name}! 🌟\n\n" +
            f"Great! You are a premium member!\n"
            f"Use Command : /help to get started 🌟\n\n"
            f"╭━━━ 𝐌𝐫𝐒𝐭𝐫𝐚𝐧𝐠𝐞𝐫™❤️ ━━━━➣\n"
            f"┣⪼ 🔄 System Status:\n"
            f"┃  ├─⪼ ✅ Security verified\n"
            f"┃  ├─⪼ ✅ Data synced\n"
            f"┃  ╰─⪼ 🔍 Checking access...\n"
            f"┣⪼ 📊 Progress: ▰▰▰▰▰▰▰▰▰▱ 99.9%\n"
            f"├─⪼ 😶‍🌫️ Gems मिटाए 🤯\n"
            f"╰━━━━━━━━━━━━━━━━━━━━➣\n"
            f"If you face any problem contact -  𝐌𝐫𝐒𝐭𝐫𝐚𝐧𝐠𝐞𝐫™❤️\n", disable_web_page_preview=True, reply_markup=BUTTONSCONTACT
        )
    else:
        await asyncio.sleep(2)
        await start_message.edit_text(
           f" 🎉 Welcome {m.from_user.first_name} to DRM Bot! 🎉\n\n"
            f"╭━━━𝐌𝐫𝐒𝐭𝐫𝐚𝐧𝐠𝐞𝐫™❤️━━━━➣\n"
            f"┣⪼ 🔄 System Status:\n"
            f"┃  ├─⪼ ✅ Security verified\n"
            f"┃  ├─⪼ ✅ Data synced\n"
            f"┃  ╰─⪼ 🔍 Checking access...\n"
            f"┣⪼ 📊 Progress: ▰▰▰▰▰▰▰▰▰▱ 99.9%\n"
            f"├─⪼ 😶‍🌫️ Gems मिटाए 🤯\n"
            f"┣⪼ 👨‍💻Login tg number ━➣ Get Aurth\n"
            f"╰━━━━━━━━━━━━━━━━━━━━➣\n"
           f"𝓨𝓸𝓾 𝓬𝓪𝓷 𝓱𝓪𝓿𝓮 𝓪𝓬𝓬𝓮𝓼𝓼 𝓽𝓸 𝓭𝓸𝔀𝓷𝓵𝓸𝓪𝓭 𝓪𝓵𝓵 𝓝𝓸𝓷-𝓓𝓡𝓜+𝓐𝓔𝓢 𝓔𝓷𝓬𝓻𝔂𝓹𝓽𝓮𝓭 𝓤𝓡𝓛𝓼 🔐 𝓲𝓷𝓬𝓵𝓾𝓭𝓲𝓷𝓰\n\n"
           f"Use Command : /help to get started 🌟\n\n"
           f"╭━━━━━━ FREE USER ━━━━━━➣\n"
           f"┣⪼ ⚠️ Access Restricted\n"
           f"┣⪼ 📝 Status: Free User\n"
           f"┣⪼ 👨‍💻Login tg number ━➣ Get Aurth\n"
           f"┣⪼ 📱Login tg number ━➣📱 number\n"
           f"┣⪼ ❌ Downloads: Not Available\n"
           f"┃\n"
           f"┣⪼ 💡 To Download Videos:\n"
           f"┃  ├─⪼ 🌟 Purchase Premium Plan\n"
           f"┃  ├─⪼ 📞 Contact Admin\n"
           f"┃  ╰─⪼ ?? B0T OWNER ━➣ 𝐌𝐫𝐒𝐭𝐫𝐚𝐧𝐠𝐞𝐫™❤️\n"
           f"┃\n"
           f"┣⪼ ✨ Benefits:\n"
           f"┃  ├─⪼ 🚀 Instant Downloads\n"
           f"┃  ├─⪼ 📺 HD Quality Videos\n"
           f"┃  ├─⪼ 🔒 Secure Access\n"
           f"┃  ╰─⪼ 🎯 24/7 Support\n"
           f"┃  ╰─⪼ 📋 /info - Upgrade Plan & More Details\n"
           f"╰━━━━━━━━━━━━━━━━➣\n"
           f"🚀 𝒴𝑜𝓊 𝒶𝓇𝑒 𝓃𝑜𝓉 𝓈𝓊𝒷𝓈𝒸𝓇𝒾𝒷𝑒𝒹 𝓉𝑜 𝒶𝓃𝓎 𝓅𝓁𝒶𝓃 𝓎𝑒𝓉! \n\n"
           f"<blockquote>💵 Monthly Plan: 🎉 ₹299🙋‍♂️💠</blockquote>\n\n"
           f"𝐼𝒻 𝓎𝑜𝓊 𝓌𝒶𝓃𝓉 𝓉𝑜 𝒷𝓊𝓎 𝓂𝑒𝓂𝒷𝑒𝓇𝓈𝒽𝒾𝓅 𝑜𝒻 𝓉𝒽𝑒 𝒷𝑜𝓉, 𝒻𝑒𝑒𝓁 𝒻𝓇𝑒𝑒 𝓉𝑜 𝒸𝑜𝓃𝓉𝒶𝒸𝓉 𝓉𝒽𝑒 𝐵𝑜𝓉 𝒜𝒹𝓂𝒾𝓃.\n", disable_web_page_preview=True, reply_markup=keyboard
    )

@bot.on_message(filters.command(["upgrade"]))
async def id_command(client, message: Message):
    chat_id = message.chat.id
    await message.reply_text(
        f" 🎉 Welcome {message.from_user.first_name} to DRM Bot! 🎉\n\n"
        f"╭━━━𝐌𝐫𝐒𝐭𝐫𝐚𝐧𝐠𝐞𝐫™❤️━━━━━➣\n"
        f"┣⪼ 🔄 System Status:\n"
        f"┃  ├─⪼ ✅ Security verified\n"
        f"┃  ├─⪼ ✅ Data synced\n"
        f"┃  ╰─⪼ 🔍 Checking access...\n"
        f"┣⪼ 📊 Progress: ▰▰▰▰▰▰▰▰▰▱ 99.9%\n"
        f"├─⪼ 😶‍🌫️ Gems मिटाए 🤯\n"
        f"┣⪼ 👨‍💻Login tg number ━➣ Get Aurth\n"
        f"╰━━━━━━━━━━━━━━━━━━━━➣\n"
           f"𝓨𝓸𝓾 𝓬𝓪𝓷 𝓱𝓪𝓿𝓮 𝓪𝓬𝓬𝓮𝓼𝓼 𝓽𝓸 𝓭𝓸𝔀𝓷𝓵𝓸𝓪𝓭 𝓪𝓵𝓵 𝓝𝓸𝓷-𝓓𝓡𝓜+𝓐𝓔𝓢 𝓔𝓷𝓬𝓻𝔂𝓹𝓽𝓮𝓭 𝓤𝓡𝓛𝓼 🔐 𝓲𝓷𝓬𝓵𝓾𝓭𝓲𝓷𝓰\n\n"
           f"Use Command : /help to get started 🌟\n\n"
           f"╭━━━━━━ FREE USER ━━━━━━➣\n"
           f"┣⪼ ⚠️ Access Restricted\n"
           f"┣⪼ 📝 Status: Free User\n"
           f"┣⪼ 👨‍💻Login tg number ━➣ Get Aurth\n"
           f"┣⪼ 📱Login tg number ━➣📱whatsapp number\n"
           f"┣⪼ ❌ Downloads: Not Available\n"
           f"┃\n"
           f"┣⪼ 💡 To Download Videos:\n"
           f"┃  ├─⪼ 🌟 Purchase Premium Plan\n"
           f"┃  ├─⪼ 📞 Contact Admin\n"
           f"┃  ╰─⪼ 🤖 B0T OWNER ━➣ 𝐌𝐫𝐒𝐭𝐫𝐚𝐧𝐠𝐞𝐫™❤️\n"
           f"┃\n"
           f"┣⪼ ✨ Benefits:\n"
           f"┃  ├─⪼ 🚀 Instant Downloads\n"
           f"┃  ├─⪼ 📺 HD Quality Videos\n"
           f"┃  ├─⪼ 🔒 Secure Access\n"
           f"┃  ╰─⪼ 🎯 24/7 Support\n"
           f"┃  ╰─⪼ 📋 /info - Upgrade Plan & More Details\n"
           f"╰━━━━━━━━━━━━━━━━➣\n"

           f"<blockquote>💵 Monthly Plan: 🎉 ₹299 🙋‍♂️💠</blockquote>\n\n"
           f"𝐼𝒻 𝓎𝑜𝓊 𝓌𝒶𝓃𝓉 𝓉𝑜 𝒷𝓊𝓎 𝓂𝑒𝓂𝒷𝑒𝓇𝓈𝒽𝒾𝓅 𝑜𝒻 𝓉𝒽𝑒 𝒷𝑜𝓉, 𝒻𝑒𝑒𝓁 𝒻𝓇𝑒𝑒 𝓉𝑜 𝒸𝑜𝓃𝓉𝒶𝒸𝓉 𝓉𝒽𝑒 𝐵𝑜𝓉 𝒜𝒹𝓂𝒾𝓃.\n", disable_web_page_preview=True, reply_markup=BUTTONSCONTACT
    )  

@bot.on_message(filters.command(["id"]))
async def id_command(client, message: Message):
    chat_id = message.chat.id
    await message.reply_text(f"<blockquote>The ID of this chat id is:</blockquote>\n`{chat_id}`")

@bot.on_message(filters.private & filters.command(["info"]))
async def info(bot: Client, update: Message):
    
    text
