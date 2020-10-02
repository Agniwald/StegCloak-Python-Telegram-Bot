def send_stats(message, database, command, date, bot):
	database.insert_one(
		{"bot_id": bot.get_me().id, "bot_name": bot.get_me().first_name, "chat": message.chat.id, "command": command, "date": date})


def get_all_chats(database, bot_id):
	chat_data = database.distinct("chat", {"bot_id": bot_id})
	chat_list = ["group" if chat < 0 else "direct" for chat in chat_data]
	return {"group": chat_list.count("group"), "direct": chat_list.count("direct")}

	
def get_stats(database, date):
	res_dict = {}
	all_bots_id = database.distinct("bot_id")
	for bot_id in all_bots_id:
		bot_data = database.find({"bot_id": bot_id})
		bot_data_list = [d for d in bot_data]
		bot_data_today = database.find({"bot_id": bot_id, "date": date})
		bot_data_today_list = [d for d in bot_data_today]
		bot_name = database.find_one({"bot_id": bot_id})["bot_name"]
		res_dict[bot_name] = []
		today = {}
		all_time = {}
		
		# For today
		for command in database.distinct("command", {"bot_id": bot_id, "date": date}):
			today[command] = sum(v == command for el in bot_data_today_list for v in el.values())

		# For all time
		for command in database.distinct("command", {"bot_id": bot_id}):
			all_time[command] = sum(v == command for el in bot_data_list for v in el.values())
		
		# res_dict[bot_name][0] - today; res_dict[bot_name][1] - all_time; res_dict[bot_name][2] - chats data
		res_dict[bot_name].append(today)
		res_dict[bot_name].append(all_time)
		res_dict[bot_name].append(get_all_chats(database, bot_id))
	
	res_text = "_From 12.06.2020_"
	for bot_in_dict in res_dict:
		res_text += "\n\n%s *(group -  %s direct - %s)*:\n\n" % (bot_in_dict,
														res_dict[bot_in_dict][2]["group"],
														res_dict[bot_in_dict][2]["direct"])
		for command in res_dict[bot_in_dict][1]:
			if res_dict[bot_in_dict][0] is not None:
				if command in res_dict[bot_in_dict][0].keys():
					res_text += "Today *%s - %s*\n" % (command, res_dict[bot_in_dict][0][command])
			res_text += "All time *%s - %s*\n\n" % (command, res_dict[bot_in_dict][1][command])
	
	return res_text
