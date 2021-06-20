import discord
import os
import schedule

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


async def job():
	print("I'm working...")
	
	# send_current_velma_count(client.get_channel("532448188901228570")) # bot-spam area51


schedule.every(10).seconds.do(job)
client.run(os.getenv('TOKEN'))
