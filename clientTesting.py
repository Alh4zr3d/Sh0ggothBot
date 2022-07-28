import asyncio
import twitchio
from dotenv import dotenv_values

config = dotenv_values()

client = twitchio.Client(token=config["SH_ACCESS_TOKEN"], initial_channels=[config["CHANNEL"]])

@client.event()
async def event_ready():
    print("Connected.")

@client.event()
async def event_join(channel: twitchio.Channel, user: twitchio.User):
    print("Connected to channel.")

async def main():
    await client.connect()
    await client.wait_for("join")
    await asyncio.sleep(0.1)
    print(client.connected_channels)
    await client.connected_channels[0].send("This is a test message.")
    await client.close()

client.loop.run_until_complete(main())