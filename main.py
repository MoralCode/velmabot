import discord
import os
import asyncio
import aiohttp
import aiocron
import csv
from datetime import datetime
import time
import logging
import timeago

client = discord.Client()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

lastvalue = (None, None)

headers = {
    'User-Agent': 'velma-bot https://github.com/MoralCode/velmabot',
	"Authorization": "Bearer " + os.getenv("API_KEY")
	}
DATAFILE = "./data/data.csv"


@client.event
async def on_ready():
	logger.info('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	#TODO: history command that shows the last few data points
	if message.content.startswith('$velma status'):
		if lastvalue[1]:
			last_updated = get_lastupdate_string(lastvalue[0])
			await message.channel.send(generate_count_message(lastvalue[1], datestr=last_updated))
		else: 
			count = await get_current_velma_count()
			await message.channel.send(generate_count_message(count, get_lastupdate_string(time.time())))

	elif message.content.startswith('$velma help'):
		await message.channel.send("a full list of commands can be found at https://github.com/MoralCode/velmabot/")

def get_lastupdate_string(lastupdate):
	# return datetime.fromtimestamp(lastupdate).strftime('%m/%d %H:%M')
	return timeago.format(datetime.fromtimestamp(lastupdate), datetime.now())

def generate_count_message(count, datestr = "recently"):
	return "The current velma count as of " + datestr + " is: " + str(count)

# https://discordpy.readthedocs.io/en/latest/faq.html#what-does-blocking-mean
async def get_current_velma_count():
	async with aiohttp.ClientSession() as session:
		async with session.get('https://vial.calltheshots.us/api/searchSourceLocations?unmatched=1&size=0', headers=headers) as r:
			if r.status == 200:
				res = await r.json()
			
				return res.get("total")

# log and post the count at 7:30 am and 9:30 pm
@aiocron.crontab('0 4,16 * * *')
async def post_velma_count():
	logger.info("I'm posting...")
	channel = client.get_channel(int(os.getenv("CHANNEL")))
	count = await get_current_velma_count()

	await channel.send(generate_count_message(count, get_lastupdate_string(time.time())))

# log the count every minute
@aiocron.crontab('* * * * *')
async def log_velma_count():
	logger.info("I'm logging...")

	count = await get_current_velma_count()

	#write to csv
	await write_datapoint(count)


async def write_datapoint(datapoint):
	global lastvalue
	with open(DATAFILE, "a") as csvfile:
		writer = csv.writer(csvfile)
		lastvalue = (time.time(), datapoint)
		writer.writerow(lastvalue)


client.run(os.getenv('DISCORD_TOKEN'))
