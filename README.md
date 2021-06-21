# Velma-Bot
![Velma from scooby doo](velma.png)

Velma bot is a discord bot to automatically post the number of sites that need to be matched in Velma to the discord channel twice a day to let people know.

The bot is currently set up only for operation in a single channel and requires the environment variables `DISCORD_TOKEN` (for the discord token) and `CHANNEL` (for the channel ID) in order to run.

## Building

To build the docker image:
`docker build -t velma-bot .`
## Hosting

The bot can be hosted with docker

```bash
docker run \ 
	-e DISCORD_TOKEN=YOUR_DISCORD_TOKEN \
	-e CHANNEL=CHANNEL_ID \
	--mount type=bind,source="$(pwd)",target=/data \
	velma-bot

```