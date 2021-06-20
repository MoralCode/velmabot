import discord
import os
import asyncio
import aiohttp
import aiocron
from bs4 import BeautifulSoup

client = discord.Client()

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
async def get_current_velma_count(channel):
	# channel = discord.utils.get(guild.text_channels, name="Name of channel")
	async with aiohttp.ClientSession() as session:
		async with session.get('https://vial.calltheshots.us/dashboard/public-velma-remaining/') as r:
			if r.status == 200:
				text = await r.text()
				soup = BeautifulSoup(text, 'html.parser')
				results = soup.find(class_="query-results")
				number = results.find(class_="big-number")
				value = number.find("h1").text
				return value


@aiocron.crontab('* * * * *') #('30 7,21 * * *')
async def job():
	print("I'm working...")

	await send_current_velma_count(client.get_channel(839741667560259604))

client.run(os.getenv('TOKEN'))
