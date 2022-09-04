# (c) @EverythingSuckz | @AbirHasan2005

import urllib.parse
from WebStreamer.bot import StreamBot
from WebStreamer.vars import Var
from WebStreamer.utils.human_readable import humanbytes
from WebStreamer.utils.database import Database
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant

db = Database(Var.DATABASE_URL, Var.SESSION_NAME)

def get_media_file_size(m):
    media = m.video or m.audio or m.document
    if media and media.file_size:
        return media.file_size
    else:
        return None
def get_media_file_name(m):
    media = m.video or m.document or m.audio
    if media and media.file_name:
        return urllib.parse.quote_plus(media.file_name)
    else:
        return None

@StreamBot.on_message(filters.command('start') & filters.private & ~filters.edited)
async def start(b, m):
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await b.send_message(
            Var.BIN_CHANNEL,
            f"#NEW_USER: \n\nNew User [{m.from_user.first_name}](tg://user?id={m.from_user.id}) Started !!"
        )
    usr_cmd = m.text.split("_")[-1]
    if usr_cmd == "/start":
        if Var.UPDATES_CHANNEL != "None":
            try:
                user = await b.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
                if user.status == "kicked":
                    await b.send_message(
                        chat_id=m.chat.id,
                        text="Sorry Sir, You are Banned to use me. Contact my [Support Bot](https://t.me/FlixHelpBot).",
                        parse_mode="markdown",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="**Please Join My Updates Channel to use this Bot!**\n\nDue to Overload, Only Channel Subscribers can use the Bot!",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("🤖 Join Updates Channel", url=f"https://t.me/+ieAUoN0k7aFjYmE0")
                            ]
                        ]
                    ),
                    parse_mode="markdown"
                )
                return
            except Exception:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="Something went Wrong. Contact my [Support Bot](https://t.me/FlixHelpBot).",
                    parse_mode="markdown",
                    disable_web_page_preview=True)
                return
        await m.reply_text(
            text='🙋 Hey Welcome To 𝗧𝗘𝗟𝗘𝗚𝗥𝗔𝗠 𝗙𝗜𝗟𝗘 𝗧𝗢 𝗟𝗜𝗡𝗞 𝗚𝗘𝗡𝗘𝗥𝗔𝗧𝗢𝗥 𝗕𝗢𝗧!!\n\nI Am An Instant Telegram File to Link Generator Bot.\n\nSend Me Any Telegram File/Documents & I Will Generate An Instant Link Back To You!',
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton('🔊 𝗖𝗛𝗔𝗡𝗡𝗘𝗟', url='https://t.me/FlixBots')],
                    [InlineKeyboardButton('🙎 𝗗𝗘𝗩𝗘𝗟𝗢𝗣𝗘𝗥', url='https://t.me/FristyFlakes')]
                ]
            ),
            disable_web_page_preview=True
        )
    else:
        if Var.UPDATES_CHANNEL != "None":
            try:
                user = await b.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
                if user.status == "kicked":
                    await b.send_message(
                        chat_id=m.chat.id,
                        text="Sorry Sir, You are Banned to use me. Contact my [Support Bot](https://t.me/FlixHelpBot).",
                        parse_mode="markdown",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="**Please Join My Updates Channel to use this Bot!**\n\nDue to Overload, Only Channel Subscribers can use the Bot!",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("🤖 Join Updates Channel", url=f"https://t.me/+ieAUoN0k7aFjYmE0")
                            ],
                            [
                                InlineKeyboardButton("🔄 Refresh / Try Again",
                                                     url=f"https://t.me/{(await b.get_me()).username}?start=AbirHasan2005_{usr_cmd}")
                            ]
                        ]
                    ),
                    parse_mode="markdown"
                )
                return
            except Exception:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="Something went Wrong. Contact my [Support Bot](https://t.me/FlixHelpBot).",
                    parse_mode="markdown",
                    disable_web_page_preview=True)
                return

        get_msg = await b.get_messages(chat_id=Var.BIN_CHANNEL, message_ids=int(usr_cmd))

        file_name = get_media_file_name(get_msg)
        file_size = humanbytes(get_media_file_size(get_msg))

        stream_link = "https://{}/{}/{}".format(Var.FQDN, get_msg.message_id, file_name) if Var.ON_HEROKU or Var.NO_PORT else \
            "http://{}:{}/{}/{}".format(Var.FQDN,
                                     Var.PORT,
                                     get_msg.message_id,
                                     file_name)

        msg_text = "**LINK SUCCESSFULLY GENERATED!! 🤓**\n\n**Copy & Paste This Link In Your Browser & The File Download Will Start Immediately!!**\n\n**📁 File Name :** `{}`\n\n**🔓 File Size :** `{}`\n\n**⭕️ Download Link :** `{}`"
        await m.reply_text(
            text=msg_text.format(file_name, file_size, stream_link),
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("📩  DIRECT DOWNLOAD  📩", url=stream_link)],
                    [InlineKeyboardButton("⚠ FREE NETFLIX ACCOUNTS ⚠", url="https://t.me/+ieAUoN0k7aFjYmE0")],
                ]
            )
        )


@StreamBot.on_message(filters.command('help') & filters.private & ~filters.edited)
async def help_handler(bot, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)
        await bot.send_message(
            Var.BIN_CHANNEL,
            f"#NEW_USER: \n\nNew User [{message.from_user.first_name}](tg://user?id={message.from_user.id}) Started !!"
        )
    if Var.UPDATES_CHANNEL != "None":
        try:
            user = await bot.get_chat_member(Var.UPDATES_CHANNEL, message.chat.id)
            if user.status == "kicked":
                await bot.send_message(
                    chat_id=message.chat.id,
                    text="Sorry Sir, You are Banned to use me. Contact my [Support Bot](https://t.me/FlixHelpBot).",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await bot.send_message(
                chat_id=message.chat.id,
                text="**Please Join My Updates Channel to use this Bot!**\n\nDue to Overload, Only Channel Subscribers can use the Bot!",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🤖 Join Updates Channel", url=f"https://t.me/+ieAUoN0k7aFjYmE0")
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await bot.send_message(
                chat_id=message.chat.id,
                text="Something went Wrong. Contact my [Support Bot](https://t.me/FlixHelpBot).",
                parse_mode="markdown",
                disable_web_page_preview=True)
            return
    await message.reply_text(
        text="Add Me To Channel As Admin With The Appropriate Rights To Make Me Workable!!",
        parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("🔊 𝗖𝗛𝗔𝗡𝗡𝗘𝗟", url="https://t.me/FlixBots")],
                [InlineKeyboardButton("🙎 𝗗𝗘𝗩𝗘𝗟𝗢𝗣𝗘𝗥", url="https://t.me/FristyFlakes")]
            ]
        )
    )
