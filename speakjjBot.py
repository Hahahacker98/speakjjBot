import os
import json
import asyncio
import requests

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiohttp import web

TOKEN = os.getenv("BOT_TOKEN")
RENDER_URL = os.getenv("RENDER_EXTERNAL_URL")

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode="HTML")
)

dp = Dispatcher()

users = set()
USERS_FILE = "users.json"


def load_users():
    try:
        return set(json.load(open(USERS_FILE)))
    except:
        return set()


def save_users():
    json.dump(list(users), open(USERS_FILE, "w"))


users = load_users()


@dp.message()
async def handle(message: types.Message):
    users.add(message.from_user.id)
    save_users()

    for uid in list(users):
        if uid == message.from_user.id:
            continue

        try:
            await bot.copy_message(uid, message.chat.id, message.message_id)
        except:
            pass


# ======================
# AIOHTTP SERVER (IMPORTANT)
# ======================

async def handle_webhook(request):
    data = await request.json()
    update = types.Update.model_validate(data)
    await dp.feed_update(bot, update)
    return web.Response(text="OK")


async def on_startup(app):
    url = f"{RENDER_URL}/{TOKEN}"

    requests.get(
        f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={url}"
    )

    print("Webhook set:", url)


app = web.Application()
app.router.add_post(f"/{TOKEN}", handle_webhook)
app.on_startup.append(on_startup)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    web.run_app(app, host="0.0.0.0", port=port)
