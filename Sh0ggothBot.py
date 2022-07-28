from twitchio.ext import commands, pubsub
from dotenv import dotenv_values
from random import choice
import twitch_auth as twitch_auth
import twitchio
import inflect
import pickle
import base64
import os
from sys import argv

try:
    data = argv[1]
    config = pickle.loads(base64.b64decode(data.encode()))
except:
    try:
        with open("configFile", 'r') as f:
            data = f.read()
        os.remove("configFile")
        config = pickle.loads(base64.b64decode(data.encode()))
    except:
        config = dotenv_values()

class Bot(commands.Bot):
    def __init__(self):
#        config = dotenv_values()
        super().__init__(
            token = config['SH_ACCESS_TOKEN'], 
            prefix = config['BOT_PREFIX'], 
            initial_channels = [config['CHANNEL']],
            SH_CLIENT_ID = config['SH_CLIENT_ID'],
            nick = config['BOT_NICK']
        )

    async def event_ready(self):
        'Called at startup'
#        config = dotenv_values()
        print(f"{config['BOT_NICK']} is online!")

    async def event_channel_joined(self, channel: twitchio.Channel):
        print(f"[+] Joined channel: {channel.name}")

    async def event_token_expired(self):
#        config = dotenv_values()
        return twitch_auth.refresh_auth(config["SH_REFRESH_TOKEN"], config["SH_CLIENT_ID"], config["SH_CLIENT_SECRET"])

    async def event_pubsub_bits(self, event: pubsub.PubSubBitsMessage):
        bits = event.bits_used
        user = event.user.name
        chan = self.get_channel('alh4zr3d')
        if bits == 69:
            choices = [
                f"@{user} Nice."
            ]
        elif bits >= 1000:
            choices = [
                    f"@{user} You really should have someone take over your finances.",
                    f"@{user} That is a lot of bitties to give a cult leader on the internet.",
                    f"@{user} You have been lost to the abysms of shrieking, immemorial lunacy!"
                ]
        else:
            choices = [
                    f"@{user} Cthulhu fhtagn! Thanks for those tig ol' bitties."
                ]
        await chan.send(choice(choices))

    async def event_pubsub_channel_points(self, event: pubsub.PubSubChannelPointsMessage):
        redemption = event.reward.title
        user = event.user.name
        chan = self.get_channel('alh4zr3d')
        match redemption:
            case "ZAP Gang Takeover":
                choices = [
                    f"@{user} alh4zMald I sense malding in our future... alh4zMald",
                    f"@{user} Even the Elder Things didn't treat my kind as poorly as you treat Al.",
                    f"@{user} FUCK ZAP AND FUCK YOU."
                ]
            case "Draw a Card from the Fit Deck":
                choices = [
                    f"@{user} gachiBASS Hoping for those squats or fire hydrants... gachiBASS",
                    f"@{user} He probably didn't notice this so get on his ass. Dance, streamer monkey. DANCE.",
                    f"@{user} Make sure he makes eye contact, or I can't finish."
                ]
            case "Summon Fighter Pilot Alh4zr3d":
                choices = [
                    f"@{user} alh4zTopgay You are still degenerate, but you can be Al's wingman anytime. alh4zTopgay",
                    f"@{user} 🍆 I FEEL A NEED. THE NEED FOR RILEY REID. 🍆",
                    f"@{user} alh4zPog Sorry, chat, it's time to buzz the tower. alh4zPog"
                ]
            case "Summon Alh4z-Ross":
                choices = [
                    f"@{user} Shoggoths were not mistakes; we were happy accidents. Kappa",
                    f"@{user} alh4zN3cro Let's have some happy malding, and find freedom in the command prompt. alh4zNecro",
                    f"@{user} You can do anything you want to do. This is your world. Until Cthulhu awakens. Then it's his."
                ]
            case "Play a single game of Hearthstone":
                choices = [
                    f"@{user} Why is this even enabled?"
                ]
            case "STOP MALDING AND TRY HARDER":
                choices = [
                    f"@{user} alh4zMald MALDING DETECTED. TURN DOWN YOUR VOLUME, CHAT. alh4zMald",
                    f"@{user} Al might wake Cthulhu with his malding, but that's nothing compared to the even larger Old One: your mom.",
                    f"@{user} Hey remember when hacking didn't piss Al off? Neither do I. Kappa"
                ]
            case "Sound Alert: Hey! Listen!":
                choices = [
                    f"@{user} Remember when Al remembered to change the scene after Stream Raiders? Me either. Kappa",
                    f"@{user} I literally ripped Elder Things limb from limb with my bare tentacles, and if you're telling Al to use netstat in a pod I'll do worse to you.",
                    f"@{user} Yeah, he doesn't listen to me either.",
                    f"@{user} Whether Al likes it or not, he needs chat's help. FlexLeft monkeyLUL FlexRight APES TOGETHER STRONG FlexLeft monkeyLUL FlexRight"
                ]
            case "Sound Alert: What are you DOING, step bro?":
                choices = [
                    f"@{user} Was Al testing Twitch chat again? Kappa",
                    f"@{user} alh4zTopgay You know, he's only pretending to be stuck in the washing machine, chat. alh4zTopgay",
                    f"@{user} This guy created an entire eldritch creature purely to roast him in his chat. Even he doesn't know what he's doing."
                ]
            case "Sound Alert: FBI Open Up!":
                choices = [
                    f"@{user} LETSGO MIKE PARSON IS AFTER US AGAIN LETSGO",
                    f"@{user} Missouri is doing just fine, chat. They decided not to prosecute the F12 key and women there almost have all the same rights as fetuses. It's fine. This is fine.",
                    f"@{user} monkaShoot They've finally come for him... monkaShoot"
                ]
            case "5-Minute Timeout":
                choices = [
                    f"@{user} Your wish is my command.",
                    f"@{user} Don't tell me how to do my job. I don't just come down to the bus station and slap the dick out of your mouth, do I?",
                    f"@{user} Good. I was tired of pretending to like you."
                ]
                await chan.send("/timeout {user} 300")
            # case _:
            #     choices = [
            #         f"@{user} Fill this in with a default option?",
            #     ]

        await chan.send(choice(choices))

    async def event_error(error: Exception, data=None):
        print("[-] Error: " + str(type(error)))
        print(str(error))
#        print(str(error.__traceback__))
        if data:
            print("[-] From Twitch API: " + str(data))

    async def event_command_error(context: commands.Context, error: Exception):
        print("[-] Error: " + type(error))
        print(str(error))
#        print(str(error.__traceback__))

    async def event_message(self, message):
#        print(message) # Debugging
        if message.echo:
            return
# Perhaps add some functionality later to respond to private messages
        if not message.channel and "WHISPER" in message.raw_data:
#            print(f"[*] Private message received: {message.content}")
            return
        await self.handle_commands(message)

    # Debugging
#    async def event_raw_data(self, data: str):
#        print(data)
    
    async def event_raw_usernotice(self, channel: twitchio.Channel, tags: dict):
        msgType = tags['msg-id']
        if msgType == 'raid':
            await channel.send(f"Iä @{tags['msg-param-displayName']}! Welcome to your {tags['msg-param-viewerCount']} viewers! Iä R'lyeh! Cthulhu fhtagn!")
        elif msgType == 'sub':
            tier = "Initiate"
            if tags['msg-param-sub-plan'] == "Prime":
                tier = "Bezos Initiate"
            elif tags['msg-param-sub-plan'] == "2000":
                tier = "Disciple"
            elif tags['msg-param-sub-plan'] == "3000":
                tier = "Ascendant"
            await channel.send(f"alh4zNecro Welcome to the Esoteric Cult of Domain Admin, {tier} @{tags['login']}! alh4zNecro")
        elif msgType == 'resub':
            o = inflect.engine()
            tier = "Initiate"
            if tags['msg-param-sub-plan'] == "Prime":
                tier = "Bezos Initiate"
            elif tags['msg-param-sub-plan'] == "2000":
                tier = "Disciple"
            elif tags['msg-param-sub-plan'] == "3000":
                tier = "Ascendant"
            await channel.send(f"alh4zNecro Welcome back to the Alh4z-Red Team for your {o.ordinal(tags['msg-param-cumulative-months'])} month, {tier} @{tags['login']}! alh4zNecro")

    @commands.command()
    async def help(self, ctx: commands.Context):
        await ctx.reply(f"Al is constantly working to improve my functionality. Currently available commands are \"hello\", \"socials\", \"whisper\", \"penis\", and \"sigma\".")

    @commands.command()
    async def hello(self, ctx: commands.Context):
        await ctx.reply(f'Cthulhu fhtagn, {ctx.author.name}!')

    @commands.command()
    async def socials(self, ctx: commands.Context):
        await ctx.reply(f"Alh4zr3d's socials -- Twitter: https://twittter.com/alh4zr3d, Youtube: https://www.youtube.com/channel/UCz-Z-d2VPQXHGkch0-_KovA, Patreon: https://patreon.com/alh4zr3d, OnlyFans: https://shorturl.at/afnY4, Github: https://github.com/alh4zr3d, Email: alh4zr3d@gmail.com")

    @commands.command()
    async def whisper(self, ctx: commands.Context):
        lovecraft_quotes = [
            '“The world is indeed comic, but the joke is on mankind.” ― H.P. Lovecraft',
            '“The oldest and strongest emotion of mankind is fear, and the oldest and strongest kind of fear is fear of the unknown.” ― H.P. Lovecraft, Supernatural Horror in Literature',
            '“Pleasure to me is wonder—the unexplored, the unexpected, the thing that is hidden and the changeless thing that lurks behind superficial mutability.” ― H.P. Lovecraft',
            '“Almost nobody dances sober, unless they happen to be insane.” ― H.P. Lovecraft',
            '“The most merciful thing in the world, I think, is the inability of the human mind to correlate all its contents. We live on a placid island of ignorance in the midst of black seas of the infinity, and it was not meant that we should voyage far.” ― H.P. Lovecraft, The Call of Cthulhu',
            '“I have seen the dark universe yawning; where the black planets roll without aim; where they roll in their horror unheeded; without knowledge, or lustre, or name.” ― H. P. Lovecraft, Nemesis',
            '“The sciences, each straining in its own direction, have hitherto harmed us little; but some day the piecing together of dissociated knowledge will open up such terrifying vistas of reality, and of our frightful position therein, that we shall either go mad from the revelation or flee from the deadly light into the peace and safety of a new dark age.” ― H. P. Lovecraft',
            '“Ride face, put that water on your moustache.” ― Riley Reid',
            '“Who knows the end? What has risen may sink, and what has sunk may rise. Loathsomeness waits and dreams in the deep, and decay spreads over the tottering cities of men.” ― H.P. Lovecraft, The Call of Cthulhu',
            '“That is not dead which can eternal lie, and with strange aeons even death may die.” ― Elsa Jean',
            '“Where does madness leave off and reality begin?” ― H.P. Lovecraft, The Shadow Over Innsmouth',
            '“The mere telling helps me to restore confidence in my own faculties; to reassure myself that I was not simply the first to succumb to a contagious nightmare hallucination.” ― H.P. Lovecraft, The Shadow Over Innsmouth',
            '“Outside the ordered universe is that amorphous blight of nethermost confusion which blasphemes and bubbles at the center of all infinity―the boundless daemon sultan Azathoth, whose name no lips dare speak aloud, and who gnaws hungrily in inconceivable, unlighted chambers beyond time and space amidst the muffled, maddening beating of vile drums and the thin monotonous whine of accursed flutes.” ― H.P. Lovecraft, The Dream-Quest of Unknown Kadath'
        ]
        await ctx.send(choice(lovecraft_quotes))

    @commands.command()
    async def penis(self, ctx: commands.Context):
        response = f"@{ctx.author.name} 🍆 P.E.N.I.S. = Pentesting Efficiency and Necessary Investigation Score. Always work on making yours larger. 🍆 Kappa"
        await ctx.reply(response)

    @commands.command()
    async def sigma(self, ctx: commands.Context):
        choices = [
            "H.U.S.T.L.E. = Hackers Under Sigma Thinking Learn Entrepreneur",
            "Having trouble making ends meet? Just make more money.",
            "JUST WORK MORE.",
            "Being successful is easy. It's as simple as being born a white male in middle class America and having your parents send you to expensive private schools so that you get an appointment to the U.S. Air Force Academy so that you don't need to pay for college and have a decent job the instant you graduate that eventually leads to a lucrative career in cybersecurity. Anyone can do it.",
            "You should be saving 40-50% of your earnings. And if you can't, just make more money, idiot.",
            "Keep expenses low - cancel streams, don't buy/play video games, don't eat out. NO DOPAMINE EVER.",
            "This Saudi prince asked me once \"Would you rather have $6400 right now or $20 every third month for a year?\". Every time, I took the $20 every third month for a year because I'm smart and you're not.",
            "You'll hear people say you should have passive income. What you should really have is passive-aggressive income.",
            "This parrot trainer asked me once \"Would you rather have $4200 right now or a half-eaten empenada?\" And every time, I take the half-eaten empenada because within one quarter I can double that and then it's just all profit from there.",
            "When Al started this Twitch channel all he had was 40 hours of NetZero, an Uncrustable, and a DVD copy of \"The Babadook\". And with nothing but hard work and ingenuity, he was able to double that in just 15 years.",
            "One of my favorite Twitch chat students once asked me \"How do I live my passion?\" I said to him, \"You have to start with your WHY\". And he said to me \"I have no idea what that means\". And so I said \"Look, there's no refunds, bro.\"",
            "My first job was actually cleaning toilets at a toilet store and I told my boss \"Look sir, you don't need to pay me. I'm just here to learn.\" And what I learned is that you cannot pay rent if your boss doesn't pay you. And that knowledge is everything.",
            "My parents grew up in the Great Depression in the 1960s and they always had the mentality of \"No you can't.\" No you can't. No you can't drive down this street; it's a one-way street and you shouldn't even be driving in your condition. Both of them did pass away, and I think it's because they didn't believe in themselves.",
            "Here's a real question for you: how do you turn $100 into $1000? If anyone knows how to do that please contact Al. Because he would like to know.",
            "Every mistake brings you closer to success. For example the other day I left my son in a hot car with the windows rolled up while I had a few drinks. He passed away, however, I realized I didn't even want a son. He was holding me back."
        ]
        await ctx.reply(choice(choices))

    @commands.command()
    async def exec(self, ctx: commands.Context):
        choices = [
            "Error: param 'cmd' expected, but not found.",
            "Error: param 'twitch_chat_brain' expected, but not found.",
            'Traceback (most recent call last): File "/home/alh4zr3d/Sh0ggothBot.py", line 3, in <module>: cmd = params[1], IndexError: list index out of range',
            'Traceback (most recent call last): File "/home/alh4zr3d/Sh0ggothBot.py", line 3, in <module>: tryingharder = params[2], IndexError: list index out of range'
        ]
        await ctx.reply(choice(choices))

async def pubsub_connect(bot, oauth_token, channel_id):
    topics = [
         pubsub.channel_points(oauth_token)[channel_id],
         pubsub.bits(oauth_token)[channel_id]
     ]
    await bot.pubsub.subscribe_topics(topics)
        
def main():
#    config = dotenv_values()
#    _ = twitch_auth.refresh_auth(config["SH_REFRESH_TOKEN"], config["SH_CLIENT_ID"], config["SH_CLIENT_SECRET"])
    bot = Bot()
    bot.pubsub = pubsub.PubSubPool(bot)
    bot.loop.create_task(pubsub_connect(bot, config['AL_ACCESS_TOKEN'], int(config["AL_CHANNEL_ID"])))
    bot.run()

if __name__ == "__main__":
    main()
