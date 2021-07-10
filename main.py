import discord
import os
import asyncio
import aiohttp
import aiocron
import csv
from datetime import datetime, timedelta
import time
import logging
import timeago
import matplotlib.pyplot as plt
import random



client = discord.Client()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

lastvalue = (None, None)

headers = {
    'User-Agent': 'velma-bot https://github.com/MoralCode/velmabot',
	"Authorization": "Bearer " + os.getenv("API_KEY")
	}
DATAFILE = "./data/data.csv"
IMAGE_CACHE = 'data/graph-tmp.png'
VOICELINES_FILE = 'lines.txt'

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
	elif message.content.startswith('$velma graph'):
		generate_graph()
		await send_image(message.channel)
	elif message.content.startswith('$velma help'):
		await message.channel.send("a full list of commands can be found at https://github.com/MoralCode/velmabot/")

def get_lastupdate_string(lastupdate):
	# return datetime.fromtimestamp(lastupdate).strftime('%m/%d %H:%M')
	return timeago.format(datetime.fromtimestamp(lastupdate), datetime.now())

def generate_graph():
	x = []
	y = []
	date_24h_ago = datetime.now() - timedelta(hours = 24)
	data = get_data_since(datetime.timestamp(date_24h_ago))
	for entry in data:
		row = entry.split(",")
		if row[1].strip():
			x.append(row[0].strip())
			y.append(row[1].strip())

	# convert data to the respective format
	x = [datetime.fromtimestamp(float(d)) for d in x ]
	y = [int(v) if v else 0 for v in y ]

	fig1, ax1 = plt.subplots()
	ax1.set_title("Number of unmatched velma sites in the last 24 hours")
	plt.plot(x, y)
	ax1.set_ylim(bottom=0)
	plt.xticks(rotation = 20) # Rotates X-Axis Ticks by 45-degrees
	plt.savefig(IMAGE_CACHE)
	plt.cla()

async def send_image(channel):
	await channel.send(file=discord.File(IMAGE_CACHE))

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


def get_data_since(timestamp):
	data = []
	with open(DATAFILE, 'r') as f:
		for line in f:
			date = line.split(",")[0] 
			date = date.strip() if date else None
			date = float(date) if date else 0
			if date >= timestamp:
				data.append(line)
	return data

#https://stackoverflow.com/a/3540315/
def random_line(filename):
	with open(filename, "r") as afile:
		line = next(afile)
		for num, aline in enumerate(afile, 2):
			if random.randrange(num):
				continue
			line = aline
		return line



client.run(os.getenv('DISCORD_TOKEN'))
