from aiogram import Bot, Dispatcher, types
import asyncio
import json
import os

TOKEN = "8445773512:AAG6D7dw4Iv4kISueElolcO9O-iPeFDqwzs"

bot = Bot(token=TOKEN)
dp = Dispatcher()

USERS_FILE = "users.json"


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


@dp.message()
async def broadcast(message: types.Message):
    user_id = message.from_user.id

    if user_id not in users:
        users.add(user_id)
        save_users(users)

    for uid in users:
        if uid == user_id:
            continue

        try:
            await bot.copy_message(
                chat_id=uid,
                from_chat_id=message.chat.id,
                message_id=message.message_id
            )
        except:
            pass


async def main():
    print("Bot started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())