# Disclaimer

# This project is created for educational and communication purposes only.

# The author is not responsible for any illegal, abusive, or malicious use of this software. Users are fully responsible for complying with the laws and regulations of their country while using this project.

# By using this software, you agree to use it at your own risk.

Telegram bot for anonymous communication
__________________________________________
# How to activate
* Create a bot via Bot Father
* Copy the key
* Go to Render, New + Web Service + Connect GitHub
* Fill in
* Build Command -> pip install -r requirements.txt
* Start Command -> python speakjjBot.py
* Environment Variables -> BOT_TOKEN = your token (from Bot Father), RENDER_EXTERNAL_URL = (click the generate button)
* deploy
___________________________________________

# How it works

* User sends a message to the Telegram bot
* Telegram sends the update to the webhook URL
* Render receives the request
* Telegram processes the update
* User ID is saved to `users.json`
* Bot copies the message to all other users
* Supports text, photos, videos, stickers, GIFs, etc.

# Stack

* Python
* aiogram
* aiohttp
* Render Web Service
* Telegram Bot API

# Features

* Global message broadcast
* Webhook support
* Automatic user saving
