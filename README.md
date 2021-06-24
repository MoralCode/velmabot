# Velma-Bot
![Velma from scooby doo](velma.png)

Velma bot is a discord bot to automatically post the number of sites that need to be matched in Velma to the discord channel twice a day to let people know.

The bot is currently set up only for operation in a single channel and requires the environment variables in the docker command below in order to run.

## Commands

`$velma status` - prints the status of velma sites to be scraped as of the last check

`$velma help` - display a help message with a link to this lost of commands

## Building

To build the docker image:
`docker build -t velma-bot .`
## Hosting

The bot can be hosted with docker

```bash
docker run \ 
	-e DISCORD_TOKEN=YOUR_DISCORD_TOKEN \
	-e CHANNEL=CHANNEL_ID \
	-e API_KEY=YOUR_VIAL_API_KEY \
	-e TZ=America/Los_Angeles \
	--mount type=bind,source=/etc/localtime,target=/etc/localtime,readonly  \
	--mount type=bind,source="$(pwd)",target=/data \
	velma-bot

```


## Troubleshooting

### Timezones
for the time to be correct, you need to mount `/etc/localtime` from the host into the docker container as read only AND set the `TZ` environment variable. both of these are done in the docker command above