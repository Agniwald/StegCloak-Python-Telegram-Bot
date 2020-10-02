import core as stegcloak
import bot_stats
import os

import telebot
import pymongo
import os
from datetime import date

from dotenv import load_dotenv
load_dotenv()

# MongoDB
cluster = pymongo.MongoClient(os.getenv('MONGO_DB_URL'))
statsData = cluster["stats"]["stats"]

bot = telebot.TeleBot(os.getenv('TOKEN'))
user_hide_dict = {}
user_reveal_dict = {}


@bot.message_handler(commands=['start', 'info'])
def start(message):
	start_text = "This bot can hide secrets inside text by encrypting the secret before cloaking it with special unicode invisible characters. It can be used to safely watermark strings, invisible scripts on webpages, texts on social media or for any other covert communication. Completely invisible!\n\n/hide to hide your secret\n/reveal to reveal secret"\
	"\n\n[Original idea](https://github.com/KuroLabs/stegcloak)\n" \
	"[Bot's source code](https://github.com/DSH01/StegCloak-Python-Telegram-Bot)"
	bot.send_message(message.chat.id, start_text, parse_mode="Markdown", disable_web_page_preview=True)


@bot.message_handler(commands=['hide'])
def hide(message):
	user_hide_dict[message.chat.id] = {}
	msg = bot.reply_to(message, "📔 Send *cover text*", parse_mode="Markdown")
	bot.register_next_step_handler(msg, process_cover_step)


def process_cover_step(message):
	user_hide_dict[message.chat.id]["cover"] = message.text
	msg = bot.reply_to(message, '🤫 Send *secret text*', parse_mode="Markdown")
	bot.register_next_step_handler(msg, process_secret_step)


def process_secret_step(message):
	user_hide_dict[message.chat.id]["secret"] = message.text
	msg = bot.reply_to(message, '🔑 Send *password that will encrypt your secret*', parse_mode="Markdown")
	bot.register_next_step_handler(msg, process_password_step)


def process_password_step(message):
	bot.reply_to(message, '⏳ Ok, now wait a bit...')

	secret = user_hide_dict[message.chat.id]["secret"]
	cover = user_hide_dict[message.chat.id]["cover"]
	password = message.text
	try:
		res = stegcloak.hide(secret, password=password, hide_text=cover)

		bot.send_message(message.chat.id, "✅ *Done! Here is the result:*", parse_mode="Markdown")
		bot.send_message(message.chat.id, res)

		del user_hide_dict[message.chat.id]
		bot_stats.send_stats(message, statsData, "hide_success", date.isoformat(date.today()), bot)
	except Exception as e:
		print(e)
		bot.send_message(message.chat.id, "❌ *Oops... something went wrong.*", parse_mode="Markdown")
		bot_stats.send_stats(message, statsData, "hide_error", date.isoformat(date.today()), bot)


@bot.message_handler(commands=['reveal'])
def reveal(message):
	user_reveal_dict[message.chat.id] = {}
	msg = bot.reply_to(message, "💬 Send *text*", parse_mode="Markdown")
	bot.register_next_step_handler(msg, process_text_step)


def process_text_step(message):
	user_reveal_dict[message.chat.id]["text"] = message.text
	msg = bot.reply_to(message, '🔑 Send *password that will decrypt secret*', parse_mode="Markdown")
	bot.register_next_step_handler(msg, process_reveal_password_step)


def process_reveal_password_step(message):
	bot.reply_to(message, '⏳ Ok, now wait a bit...')

	txt = user_reveal_dict[message.chat.id]["text"]
	password = message.text
	try:
		res = stegcloak.reveal(txt, password)

		bot.send_message(message.chat.id, "✅ *Done! Here is the result:*", parse_mode="Markdown")
		bot.send_message(message.chat.id, res)

		del user_reveal_dict[message.chat.id]
		bot_stats.send_stats(message, statsData, "reveal_success", date.isoformat(date.today()), bot)
	except Exception as e:
		print(e)
		bot.send_message(message.chat.id, "❌ *Oops... something went wrong.*", parse_mode="Markdown")
		bot_stats.send_stats(message, statsData, "reveal_error", date.isoformat(date.today()), bot)


if __name__ == '__main__':
	bot.infinity_polling()
