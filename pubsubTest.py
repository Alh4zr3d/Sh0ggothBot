import twitchio
import asyncio
from twitchio.ext import pubsub
from dotenv import dotenv_values

config = dotenv_values()
my_token = config['SH_ACCESS_TOKEN']
users_oauth_token = config['AL_ACCESS_TOKEN']
users_channel_id = int(config["AL_CHANNEL_ID"])
client = twitchio.Client(token=my_token)
client.pubsub = pubsub.PubSubPool(client)

@client.event()
async def event_pubsub_bits(event: pubsub.PubSubBitsMessage):
    print(event) # do stuff on bit redemptions

@client.event()
async def event_pubsub_channel_points(event: pubsub.PubSubChannelPointsMessage):
    print(event) # do stuff on channel point redemptions

async def main():
    topics = [
        pubsub.channel_points(users_oauth_token)[users_channel_id],
        pubsub.bits(users_oauth_token)[users_channel_id]
    ]
    await client.pubsub.subscribe_topics(topics)
    await client.start()

client.loop.run_until_complete(main())