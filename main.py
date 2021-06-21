import discord
import os
import asyncio
import aiohttp
import aiocron
import csv
import time
from bs4 import BeautifulSoup

client = discord.Client()

headers = {
    'User-Agent': 'velma-bot https://github.com/MoralCode/velmabot'}


@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content.startswith('$hello'):
		await message.channel.send('Hello!')

# https://discordpy.readthedocs.io/en/latest/faq.html#what-does-blocking-mean
async def get_current_velma_count():
	async with aiohttp.ClientSession() as session:
		async with session.get('https://vial.calltheshots.us/dashboard/public-velma-remaining/', headers=headers) as r:
			if r.status == 200:
				text = await r.text()
				soup = BeautifulSoup(text, 'html.parser')
				results = soup.find(class_="query-results")
				number = results.find(class_="big-number")
				value = number.find("h1").text
				return value

# log and post the count at 7:30 am and 9:30 pm
@aiocron.crontab('30 7,21 * * *')
async def post_velma_count():
	print("I'm posting...")
	channel = client.get_channel(os.getenv("CHANNEL"))
	count = await get_current_velma_count()

	await channel.send("The Current velma count is: " + str(count))

# log the count every 30 minutes
@aiocron.crontab('30 * * * *')
async def post_velma_count():
	print("I'm logging...")

	count = await get_current_velma_count(client.get_channel(os.getenv("CHANNEL")))

	#write to csv
	await write_datapoint(count)


async def write_datapoint(datapoint):
	with open("./data/data.csv", "a") as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow([time.time(), datapoint])


client.run(os.getenv('DISCORD_TOKEN'))
