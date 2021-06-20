import discord
import os
import asyncio
import schedule
import aiohttp

client = discord.Client()

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))

	while True:
		schedule.run_pending()
		await asyncio.sleep(10)
		

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content.startswith('$hello'):
		await message.channel.send('Hello!')

# https://discordpy.readthedocs.io/en/latest/faq.html#what-does-blocking-mean
async def send_current_velma_count(channel):
	# channel = discord.utils.get(guild.text_channels, name="Name of channel")
	async with aiohttp.ClientSession() as session:
		async with session.get('https://vial.calltheshots.us/dashboard/public-velma-remaining/') as r:
			if r.status == 200:
				text = await r.text()
				print(text)

				# await channel.send(js['file'])

async def job():
	print("I'm working...")
	
	send_current_velma_count(client.get_channel("532448188901228570")) # bot-spam area51


schedule.every(10).seconds.do(job)
client.run(os.getenv('TOKEN'))
