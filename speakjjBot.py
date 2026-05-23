import os
import json
import asyncio
import requests
from flask import Flask, request

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties

# ======================
# CONFIG
# ======================

TOKEN = os.getenv("BOT_TOKEN")
RENDER_URL = os.getenv("RENDER_EXTERNAL_URL")

if not TOKEN:
    raise Exception("BOT_TOKEN is missing")

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode="HTML")
)

dp = Dispatcher()
app = Flask(__name__)

USERS_FILE = "users.json"


# ======================
# USERS STORAGE
# ======================

def load_users():
    try:
        with open(USERS_FILE, "r") as f:
            return set(json.load(f))
    except:
        return set()


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(list(users), f)


users = load_users()


# ======================
# MAIN LOGIC
# ======================

@dp.message()
async def handle_message(message: types.Message):
    users.add(message.from_user.id)
    save_users(users)

    for uid in list(users):
        if uid == message.from_user.id:
            continue

        try:
            await bot.copy_message(
                chat_id=uid,
                from_chat_id=message.chat.id,
                message_id=message.message_id
            )
        except:
            pass


# ======================
# WEBHOOK ENDPOINT
# ======================

@app.post(f"/{TOKEN}")
def telegram_webhook():
    data = request.get_json()

    update = types.Update.model_validate(data)

    # безопасный запуск async внутри sync Flask
    asyncio.run(dp.feed_update(bot, update))

    return "OK"


# ======================
# SET WEBHOOK ON START
# ======================

async def setup_webhook():
    url = f"{RENDER_URL}/{TOKEN}"

    requests.get(
        f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={url}"
    )

    print("Webhook set to:", url)


# ======================
# RUN SERVER (FIXED)
# ======================

async def runner():
    await setup_webhook()
    print("Bot is running...")

    port = int(os.environ.get("PORT", 10000))

    from threading import Thread

    def run_flask():
        app.run(host="0.0.0.0", port=port)

    Thread(target=run_flask, daemon=True).start()

    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(runner())
