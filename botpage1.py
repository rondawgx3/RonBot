"""Ronald Bot"""

import discord
from discord.ext import commands
from discord.utils import get

import youtube_dl
import os

import random
import asyncio
import aiohttp
import json

from discord import Game, utils
from discord.ext.commands import Bot

client: Bot = commands.Bot(command_prefix='~')


"""READY + STATUS MESSAGE"""


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="the command {~} | "
                                                           "***in 3 servers*** | "
                                                           "-made in PyCharm.py-"
                                                           " [~ronaldhelp]"
                                                           "(by:@rawndawg#5543)"))
    print('\n Bot is ready.')


"""HELP/COMMAND LIST"""


@client.command(name='rhelp',
                description='A hub for all-things Ronald Bot',
                brief='in-depth HELP',
                aliases=['ronbothelp', 'ronhelp'],
                pass_context=True)
async def ronaldhelp(ctx):
    response = ("""
----------------------------------------------------------------------------
    **[ ~ ] = Ronald Bot command prefix**      
    *clear* -  clears messages (+ # of messages you want deleted)                                                                           
    *ping* -  gives latency time of the bot                                                                                                               
    *8ball* -  ask a yes or no question, see what RonaldBot thinks 
    *fortune* -  RobBot's prediction of your tidings                                                                                                                                                         
    *funfact* -  learn an interesting piece of trivia                                                                                                                                                      
    *yomama* -  ask for a yo mama joke                                                                                                                                                
    *emoji* -  gives you an emoji
    *userinfo* -  information about another server member     
    *die* -  please don't :(                                                                           
    *discquestion* -  A discussion question from a wide range of subjects 
    *riddle* -  test your brain!  
    *dm* -  text a user through the bot, <~dm> <user> <message> 
    *adm* -  anonymous version of dm command   
    *join* -  ask the bot to join the voice chat! 
    *play* -  play any youtube video's audio with youtube link. 
----------------------------------------------------------------------------
""")
    information = ("TO LEARN HOW TO USE A COMMAND ~help <command name>")
    embed = discord.Embed(title="⬇Ronald Bot Help Center⬇",
                          description=f"{response}\n{information}",
                          color=discord.Color.from_rgb(r=5, g=6, b=7))
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/779025578015719513/785018357543206922/unknown.png")
    embed.set_footer(text="For information about the Bot ~info")
    embed.add_field(name="\n🔹Other🔹", value="***New command ~WindowsShortcuts***", inline=False)
    embed.add_field(name="\nDiscord Help", value="[⚙ Help Center](https://support.discord.com/hc/en-us)\n"
                    "[👤 Account Settings](https://support.discord.com/hc/en-us/categories/200404358)\n"
                    "[💬 Text Chat](https://support.discord.com/hc/en-us/sections/11500045867)\n"
                    "[🗣 Voice Chat](https://support.discord.com/hc/en-us/sections/201110537-Voice-Chat)\n"
                    "[👋 User Interface](https://support.discord.com/hc/en-us/categories/200404398)\n")
    await ctx.send(embed=embed)


@client.command(name='bitcoin',
                description='delete messages',
                brief='current price of Bitcoin in USD',
                aliases=['bitcoinprice'],
                pass_context=True)
async def bitcoin(ctx):
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    async with aiohttp.ClientSession() as session:  # Async HTTP request
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)
        await ctx.send("Bitcoin price is: $" + response['bpi']['USD']['rate'])


"""Administrative Tools"""


@client.command(name='clear',
                description='delete messages',
                brief='delete messages',
                aliases=['purge'],
                pass_context=True)
async def _clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)


@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    if member.top_role > ctx.author.top_role:
        return await ctx.send("Member's role is higher, cannot kick")
    await member.kick(reason=reason)


@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    if member.top_role > ctx.author.top_role:
        return await ctx.send("Member's role is higher, cannot ban")
    else:
        await member.kick(reason=reason)
        await ctx.send(f'Banned {member.mention}')


@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return


@client.command()
async def mute(ctx, member: discord.Member, *, reason="No reason given"):
    if member.top_role > ctx.author.top_role:
        return await ctx.send("Member's role is higher, cannot mute!")
    guild = ctx.guild
    muted_role = utils.get(guild.roles, name="Muted")
    if muted_role in member.roles:
        await ctx.send(f"**{member.display_name}** is already muted.")
        return
    if muted_role is None:
        muted_role = await guild.create_role(name="Muted")
        await member.add_roles(muted_role, reason=reason)
        await ctx.send(f"**{member.display_name}** was muted for **{reason}**")
        for channel in guild.channels:
            if channel.type == channel.type.text:
                await channel.set_permissions(muted_role, send_messages=False)
                if channel.type == channel.type.voice:
                    await channel.set_permissions(muted_role, speak=False)


"""PING/LATENCY"""


@client.command(name='ping',
                description='Latency of Bot Client Connection',
                brief='latency of Bot',
                aliases=['latency'],
                pass_context=True)
async def _ping(ctx):
    lping = round(client.latency * 1000)
    embed = discord.Embed(title="Pong!", description=f"{lping}ms", color=discord.Color.blue())
    await ctx.send(embed=embed)


"""8-BALL"""


@client.command(name='8ball',
                description="Answers a yes/no question.",
                brief="Answers from the beyond.",
                aliases=['eight_ball', 'eightball', '8-ball'],
                pass_context=True)
async def _8ball(ctx, *, question):
    responses = ['💥It is certain💥',
                 'it is decidedly so',
                 'Without a doubt',
                 'Yes - definitely',
                 'You may rely on it.',
                 'As I see it, yes.',
                 'Most likely🤔',
                 'reply hazy, try again',
                 'I am told no',
                 'Not looking so good',
                 'That would be a big no',
                 'NO!',
                 'Maybe I should not say this but... YEAH',
                 'Hmmmmmmmmmm... maybe I am going out on a limb but I think no',
                 "HAHA YOU THOUGHT!",
                 '😔😕Ummmmm... sorry but that is a no']
    await ctx.send(f'🎱\nQuestion: {question}\nAnswer: {random.choice(responses)}, {ctx.message.author.mention}')


"""RANDOM"""


@client.command(brief="Information about a user you ask about",
                aliases=["ui", "UI", "userI", "infouser", 'infou'])
async def userinfo(ctx, member: discord.Member):

    embed = discord.Embed(color=member.color, timestamp=ctx.message.created_at)

    embed.add_field(name=f"- User Info - {member}", value="---")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Demanded by {ctx.author}", icon_url=ctx.author.avatar_url)

    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="Name:", value=member.display_name)

    embed.add_field(name="Created account:", value=member.created_at.strftime("%a, %d %B %Y, %I:%M %p UTC"))
    embed.add_field(name="Joined the discord on:", value=member.joined_at.strftime("%a, %d %B %Y, %I:%M %p UTC"))

    embed.add_field(name="Bot?", value=member.bot)

    await ctx.send(embed=embed)


@client.command(name='time',
                description="Date/Time in UTC",
                brief="Exact Time",
                aliases=['date'])
async def datetime(ctx):
    embed = discord.Embed(color=discord.Color.from_rgb(5, 37, 80), timestamp=ctx.message.created_at)
    embed.add_field(name="⌛Time⏳:", value=f'{ctx.message.created_at}\n')
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/779025578015719513/784659638184050738/unknown.png")
    await ctx.send(embed=embed)


@client.command(brief="combine two things")
async def add(ctx, number1, number2):
    await ctx.send(number1 + number2)


@client.command(brief="No!")
async def die(ctx):
    await ctx.send("Hey that's really mean you aren't a nice person!! :zzz: X(")


@client.command(aliases=['spotify', 'link'])
async def links(ctx):
    responses = ["https://open.spotify.com/playlist/1YZgm6gBEgaVH0rWS5nwwd?si=9Fel6zsHQ0mGl1hWuVxnNA"
                 '   |   https://open.spotify.com/playlist/2YItfYjbp8GVSErdg20KtP?si=zHAhzeruS4mNgeaZjg2kxw'
                 '   |   https://open.spotify.com/playlist/71EeIWhpNdYqP8E7iSjdPA?si=cvIAgwyJQ36jqauOf7IR7Q'
                 '   |   https://open.spotify.com/playlist/1nBTLrhX6BTB5uMWuVe61q?si=_DrGKLVdT0WZfP15vvYhcA'
                 '   |   https://open.spotify.com/playlist/4GtQVhGjAwcHFz82UKy3Ca?si=kxJVRqpwRd2Tkt1GOB54Hw'
                 '   |   https://open.spotify.com/playlist/37i9dQZF1DX0yEZaMOXna3?si=kZCdmMKXRGKAh2MEqXxikQ'
                 '   |   https://open.spotify.com/playlist/2Rb0mojma5Yg3VYyt8SPz2?si=uH4qXkgATG-1G-Dnhm3n6w'
                 '   |   https://open.spotify.com/playlist/336lJ5JhqaNxwBwPC31PDI?si=7bkT7CmIThWCR1Ws2K_Rlg']
    await ctx.send(f"| LINKS: {responses}")


@client.command(aliases=['yomamajoke', 'yo-mama', 'yo_mama'])
async def yomama(ctx):
    responses = ["Yo mama's so fat, when she fell I didn't laugh, but the sidewalk cracked up.",
                 "Yo mama's so fat, when she skips a meal, the stock market drops.",
                 "Yo mama's so fat, it took me two buses and a train to get to her good side.",
                 "Yo mama's so fat, when she goes camping, the bears hide their food.",
                 "Yo mama's so fat, if she buys a fur coat, a whole species will become extinct.",
                 "Yo mama's so fat, she stepped on a scale and it said: 'To be continued.'",
                 "Yo mama's so fat, I swerved to miss her in my car and ran out of gas.",
                 "Yo mama's so fat, when she wears high heels, she strikes oil.",
                 "Yo mama's so fat, when she sits around the house, she SITS AROUND the house.",
                 "Yo mama's so fat, her car has stretch marks.",
                 "Yo mama's so fat, she can't even jump to a conclusion.",
                 "Yo mama's so fat, her blood type is Ragu.",
                 "Yo mama's so fat, if she was a Star Wars character, her name would be Admiral Snackbar.",
                 "Yo mama's so stupid, she stared at a cup of orange juice for 12 hours because it said 'concentrate.'",
                 "Yo mama's so fat, she brought a spoon to the Super Bowl.",
                 "Yo mama's so stupid, when they said, 'Order in the court,' she asked for fries and a shake.",
                 "Yo mama's so stupid, she thought a quarterback was a refund.",
                 "Yo mama's so stupid, when I told her that she lost her mind, she went looking for it",
                 "Yo mama's so stupid, she went to the dentist to get a Bluetooth.",
                 "Yo mama's so stupid, she took a ruler to bed to see how long she slept.",
                 "Yo mama's so stupid, she got locked in the grocery store and starved to death.",
                 "Yo mama's so stupid, she put airbags on her computer in case it crashed.",
                 "Yo mama's so ugly, she threw a boomerang and it refused to come back.",
                 "Yo mama's so ugly, her portraits hang themselves.",
                 "Yo mama's so lazy, she stuck her nose out the window and let the wind blow it.",
                 "Yo mama so short, she went to see Santa and he told her to get back to work."]
    await ctx.send(f"Here's a yo mama joke: {random.choice(responses)}")


@client.command(aliases=['riddles', 'ariddle', 'giveriddle'])
async def riddle(ctx):
    responses = ["What has to be broken before you can use it?\n||Answer: An egg||"
                 "I’m tall when I’m young, and I’m short when I’m old. What am I?""\n||Answer: A candle||",
                 "What month of the year has 28 days?""\n||Answer: All of them||",
                 "What is full of holes but still holds water?""\n||Answer: A sponge||",
                 "What question can you never answer yes to?""\n||Answer: Are you asleep yet?||",
                 "What is always in front of you but can’t be seen?""\n||Answer: The future||",
                 "There is a one-story house where everything is yellow. Yellow walls, yellow doors, yellow furniture."
                 "What color are the stairs?""\n||Answer: There aren’t any—it’s a one-story house.||",
                 "What can you break, even if you never pick it up or touch it? \n||Answer: A promise||",
                 "What goes up but never comes down? \n||Answer: Your age||",
                 "A man who was outside in the rain without umbrella, didn’t get a single hair on his head wet. Why?"
                 "\n||Answer: He was bald.||",
                 "What gets wet while drying? \n||Answer: A towel||",
                 "What can you keep after giving to someone? \n||Answer: Your word||",
                 "I shave every day, but my beard stays the same. What am I? \n||Answer: A barber||",
                 "You see a boat filled with people, yet there isn’t a single person on board. How is that possible?\n"
                 "||Answer: All the people on the boat are married.||",
                 "Man dies of old age on his 25 birthday. How is this possible? \n||Answer: He was born on Feb 29.||",
                 "I have branches, but no fruit, trunk or leaves. What am I? \n||Answer: A bank||",
                 "What can’t talk but will reply when spoken to? \n||Answer: An echo||",
                 "The more of this there is, the less you see. What is it? \n||Answer: Darkness||",
                 "David’s parents have three sons: Snap, Crackle, what’s the name of the third son?\n||Answer: David||",
                 "I follow you all the time+copy every move,you can’t touch or catch me. What am I?\n||Your shadow||",
                 "What has many keys but can’t open a single lock? \n||A piano||",
                 "What can you hold in your left hand but not in your right? \n||Answer: Your right elbow||",
                 "What is black when it’s clean and white when it’s dirty? \n||Answer: A chalkboard||",
                 "What gets bigger when more is taken away? \n||Answer: A hole||",
                 "I’m light as feather, the strongest person can’t hold me for five minutes.?\n||Answer: Your breath||",
                 "I’m found in socks, scarves and mittens; and often in the paws of playful kittens.\n||Answer: Yarn||",
                 "Where does today come before yesterday? \n||Answer: The dictionary||",
                 "What invention lets you look right through a wall? \n||Answer: A window||",
                 "If you’ve got me, you want to share me; if you share me, you haven’t kept me? \n||Answer: A secret||",
                 "What can’t be put in a saucepan? \n||Answer: It’s lid||",
                 "What goes up and down but doesn’t move? \n||Answer: A staircase||",
                 "you’re running in a race and you pass person in 2nd place, what place you in?\n||Answer: 2nd place||",
                 "It belongs to you, but other people use it more than you do. What is it? \n||Answer: Your name||",
                 "What has lots of eyes, but can’t see? \n||Answer: A potato||",
                 "What has one eye, but can’t see? \n||Answer: A needle||",
                 "What has many needles, but doesn’t sew?\n||Answer: A Christmas tree||",
                 "What has hands, but can’t clap?\n||Answer: A clock||",
                 "What has legs, but doesn’t walk?\n||Answer: A table||",
                 "What has one head, one foot and four legs?\n||Answer: A bed||",
                 "What can you catch, but not throw?\n||Answer: A cold||",
                 "What kind of band never plays music?\n||Answer: A rubber band||",
                 "What has many teeth, but can’t bite?\n||Answer: A comb||",
                 "What is cut on a table, but is never eaten?\n||Answer: A deck of cards||",
                 "What has words, but never speaks?\n||Answer: A book||",
                 "What runs all around a backyard, yet never moves?\n||Answer: A fence||",
                 "What has a thumb and four fingers, but is not a hand?\n||Answer: A glove||",
                 "What has a head and a tail but no body?\n||Answer: A coin||",
                 "Where does one wall meet the other wall?\n||Answer: On the corner||",
                 "What building has the most stories?\n||Answer: The library||"
                 ]
    await ctx.send(f"Riddle: {random.choice(responses)}")


"""DM"""


@client.command(brief="DM another user with Bot",
                aliases=['directmessage'])
async def dm(ctx, user4: discord.Member, *, dmmessage: str):
    channel = ctx.message.channel
    messages = []
    async for message in channel.history(limit=2):
        messages.append(message)
    await channel.delete_messages(messages)
    await user4.send("You have one new message from:")
    await user4.send(ctx.author)
    await user4.send("with message:")
    await user4.send("**" + dmmessage + "**")
    await ctx.author.send("DM has been sent to:")
    await ctx.author.send(user4)
    await ctx.author.send("with message:")
    await ctx.author.send("**" + dmmessage + "**")


@client.command(brief="Anonymous DM to another user with Bot",
                aliases=['anonymous', 'dmanonymous'])
async def adm(ctx, user8: discord.Member, *, dmmessage2: str):
    channel = ctx.message.channel
    messages = []
    async for message in channel.history(limit=2):
        messages.append(message)
    await channel.delete_messages(messages)
    await user8.send("You have one new message:")
    await user8.send("**" + dmmessage2 + "**")
    await ctx.author.send("Anonymous DM to:")
    await ctx.author.send(user8)
    await ctx.author.send("with message:")
    await ctx.author.send("**" + dmmessage2 + "**")
    await ctx.author.send("has been sent")


"""Voice_Channel"""


@client.command(pass_context=True, aliases=['j', 'joi'])
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await voice.disconnect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"The bot has connected to {channel}\n")

    await ctx.send(f"Joined {channel}")


@client.command(pass_context=True, aliases=['l', 'lea'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"The bot has left {channel}")
        await ctx.send(f"Left {channel}")
    else:
        print("Bot was told to leave voice channel, but was not in one")
        await ctx.send("Don't think I am in a voice channel")


@client.command(pass_context=True, aliases=['p', 'pla'])
async def play(ctx, url: str):

    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("ERROR: Music playing")
        return

    await ctx.send("Getting everything ready now")

    voice = get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print("Song finished!"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nname = name.rsplit("-", 2)
    await ctx.send(f"Playing: {nname[0]}")
    print("playing now\n")


@client.command(aliases=['songs', 'playlist', "Ronald's_collection", "compiled_music"])
async def music(ctx):
    responses = [
                 "https://www.youtube.com/watch?v=eHvgQDRpA-s",
                 "https://www.youtube.com/watch?v=SgL1tkWKj-I",
                 "https://www.youtube.com/watch?v=u8pVZ5hTGJQ",
                 "https://www.youtube.com/watch?v=8O9P5Us_eVo",
                 "https://www.youtube.com/watch?v=wYwkVyDl4Oo",
                 "https://www.youtube.com/watch?v=t0pocjTJQ5I",
                 "https://www.youtube.com/watch?v=B06qqB7bp-w",
                 "https://www.youtube.com/watch?v=O8g_iLP_9go",
                 "https://www.youtube.com/watch?v=f_K_0SNaRk0",
                 "https://www.youtube.com/watch?v=lV8fBH6S_xw",
                 "https://www.youtube.com/watch?v=UyEHgnqlHtY",
                 "https://www.youtube.com/watch?v=MMPqgqCprKY",
                 "https://www.youtube.com/watch?v=DmNfT-B7nlA",
                 "https://www.youtube.com/watch?v=YGsFs_BxKUA",
                 "https://www.youtube.com/watch?v=GftZ601-pXs",
                 "https://www.youtube.com/watch?v=4nbYqWVXp7Q",
                 "https://www.youtube.com/watch?v=V1mzLYKb35I",
                 "https://www.youtube.com/watch?v=veJlefvVkPI",
                 "https://www.youtube.com/watch?v=L22VmoQZqT4",
                 "https://www.youtube.com/watch?v=RYr96YYEaZY",
                 "https://www.youtube.com/watch?v=TA1W-pHNKl8",
                 "https://www.youtube.com/watch?v=GhdGWTZs1rc",
                 "https://www.youtube.com/watch?v=RRl_C73vFtQ",
                 "https://www.youtube.com/watch?v=ztkXQCr8lrQ",
                 "https://www.youtube.com/watch?v=bx1Bh8ZvH84",
                 "https://www.youtube.com/watch?v=tI-5uv4wryI",
                 "https://www.youtube.com/watch?v=xFrGuyw1V8s",
                 "https://www.youtube.com/watch?v=unfzfe8f9NI",
                 "https://www.youtube.com/watch?v=papuvlVeZg8",
                 "https://www.youtube.com/watch?v=WXBHCQYxwr0",
                 "https://www.youtube.com/watch?v=ZLZCGWCUtgY",
                 "https://www.youtube.com/watch?v=RjlvdcBAKdg",
                 "https://www.youtube.com/watch?v=vXHyFN9_2so",
                 "https://www.youtube.com/watch?v=9_y6nFjoVp4",
                 "https://www.youtube.com/watch?v=Y3G7gzg_FhU",
                 "https://www.youtube.com/watch?v=-59rmRj4QnA",
                 "https://www.youtube.com/watch?v=s0KXV0gB0dw",
                 "https://www.youtube.com/watch?v=eocoBdbCC0I",
                 "https://www.youtube.com/watch?v=-nhcwtS9xUM",
                 "https://www.youtube.com/watch?v=La4Dcd1aUcE",
                 "https://www.youtube.com/watch?v=YArQ641o8V8",
                 "https://www.youtube.com/watch?v=CCyiVRJ96ok",
                 "https://www.youtube.com/watch?v=KYHIugsKC88",
                 "https://www.youtube.com/watch?v=Z4mbxaa3XL8",
                 "https://www.youtube.com/watch?v=uJ_1HMAGb4k",
                 "https://www.youtube.com/watch?v=SDTZ7iX4vTQ",
                 "https://www.youtube.com/watch?v=34Na4j8AVgA",
                 "https://www.youtube.com/watch?v=aBKEt3MhNMM",
                 "https://www.youtube.com/watch?v=RPUAldgS7Sg",
                 "https://www.youtube.com/watch?v=nGBLlFMn9Xc",
                 "https://www.youtube.com/watch?v=CY3D_14-AC8",
                 "https://www.youtube.com/watch?v=_xQKBMCTIpQ",
                 "https://www.youtube.com/watch?v=q5uMOOQ6MV0",
                 "https://www.youtube.com/watch?v=vGJTaP6anOU",
                 "https://www.youtube.com/watch?v=77R1Wp6Y_5Y",
                 "https://www.youtube.com/watch?v=7Zb35-ZRMUE",
                 "https://www.youtube.com/watch?v=X6-sU7pVJ3k",
                 "https://www.youtube.com/watch?v=v89rw32hb9Y",
                 "https://www.youtube.com/watch?v=XecDz-o-KnY",
                 "https://www.youtube.com/watch?v=0xGPi-Al3zQ",
                 "https://www.youtube.com/watch?v=k4M53xndqiU",
                 "https://www.youtube.com/watch?v=dQRJc9I-Iw4",
                 "https://www.youtube.com/watch?v=CFhFyvk0yS8",
                 "https://www.youtube.com/watch?v=txDMiD8ia50",
                 "https://www.youtube.com/watch?v=dZQsKkvLsNA",
                 "https://www.youtube.com/watch?v=3KFvoDDs0XM",
                 "https://www.youtube.com/watch?v=lXh19yDFO84",
                 "https://www.youtube.com/watch?v=hOUTme34ZKA",
                 "https://www.youtube.com/watch?v=gxEPV4kolz0",
                 "https://www.youtube.com/watch?v=x194HbAI-og",
                 "https://www.youtube.com/watch?v=oVhNPHF0Sb0",
                 "https://www.youtube.com/watch?v=b9rhaGxlr6M",
                 "https://www.youtube.com/watch?v=KMeQ3LxA30k",
                 "https://www.youtube.com/watch?v=mI1sxQi7USA",
                 "https://www.youtube.com/watch?v=yZ-VUnIehi8",
                 "https://www.youtube.com/watch?v=BdEe5SpdIuo",
                 "https://www.youtube.com/watch?v=27k0iaN2uOs",
                 "https://www.youtube.com/watch?v=fbHbTBP_u7U",
                 "https://www.youtube.com/watch?v=NVtIgfqI6yo",
                 "https://www.youtube.com/watch?v=50VNCymT-Cs",
                 "https://www.youtube.com/watch?v=NU9JoFKlaZ0",
                 "https://www.youtube.com/watch?v=U0XcqF7rqHk",
                 "https://www.youtube.com/watch?v=p7x8rx1GVcs",
                 "https://www.youtube.com/watch?v=Efa6BAWPm9o",
                 "https://www.youtube.com/watch?v=bJ9r8LMU9bQ",
                 "https://www.youtube.com/watch?v=eJn_RwQ0WTo",
                 "https://www.youtube.com/watch?v=VdQY7BusJNU",
                 "https://www.youtube.com/watch?v=RmwvRC4KApM",
                 "https://www.youtube.com/watch?v=ZVeAFoT97g4",
                 "https://www.youtube.com/watch?v=PIkl371ufG4",
                 "https://www.youtube.com/watch?v=5rOiW_xY-kc",
                 "https://www.youtube.com/watch?v=0uLI6BnVh6w",
                 "https://www.youtube.com/watch?v=l3LFML_pxlY",
                 "https://www.youtube.com/watch?v=coR_6sAOugY",
                 "https://www.youtube.com/watch?v=cWFc1yUy1lM",
                 "https://www.youtube.com/watch?v=fpRKWA0pAXI",
                 "https://www.youtube.com/watch?v=ic9KOmxNrDc",
                 "https://www.youtube.com/watch?v=4aifzMWfNmg",
                 "https://www.youtube.com/watch?v=gLLE3B75UJw",
                 "https://www.youtube.com/watch?v=ic8j13piAhQ",
                 "https://www.youtube.com/watch?v=pHoHDNxay3A",
                 "https://www.youtube.com/watch?v=2B9fBFtBXhU",
                 "https://www.youtube.com/watch?v=bqJ9I-3MG1g",
                 "https://www.youtube.com/watch?v=0o0WbQV6OZQ",
                 "https://www.youtube.com/watch?v=oNiyHQhYqTc",
                 "https://www.youtube.com/watch?v=pVpO3zc4Shs",
                 "https://www.youtube.com/watch?v=5cs77TyQ95o",
                 "https://www.youtube.com/watch?v=hFzEA7ZAfZQ",
                 "https://www.youtube.com/watch?v=sAbdbwXziMY",
                 "https://www.youtube.com/watch?v=ufO1G9x7Qxk",
                 "https://www.youtube.com/watch?v=rT-5NY83OYI",
                 "https://www.youtube.com/watch?v=ssVvkfcL9HI",
                 "https://www.youtube.com/watch?v=TaWLLFQHeEg",
                 "https://www.youtube.com/watch?v=2Tuyw9WBFkQ",
                 "https://www.youtube.com/watch?v=AIoaiTwLk6I",
                 "https://www.youtube.com/watch?v=PKoBTEcq8Ck",
                 "https://www.youtube.com/watch?v=YmQlBfxh4Us",
                 "https://www.youtube.com/watch?v=1_qQQIzLCbY",
                 "https://www.youtube.com/watch?v=FzufCN5tYWA",
                 "https://www.youtube.com/watch?v=1PPdYEDRDX0",
                 "https://www.youtube.com/watch?v=F7n0nJfc2xg",
                 "https://www.youtube.com/watch?v=WagHxoEaxKM",
                 "https://www.youtube.com/watch?v=c0BnniO5xYo",
                 "https://www.youtube.com/watch?v=77Jgt77ENqs",
                 "https://www.youtube.com/watch?v=JeVIek_krKQ",
                 "https://www.youtube.com/watch?v=MYnwtPZCooI",
                 "https://www.youtube.com/watch?v=U6DH8ZnyJLU",
                 "https://www.youtube.com/watch?v=Ps-8MaPQ9LY",
                 "https://www.youtube.com/watch?v=Hxgq7gvJJK4",
                 "https://www.youtube.com/watch?v=lXVzx1XonNY",
                 "https://www.youtube.com/watch?v=Rslqwh_o7Ps",
                 "https://www.youtube.com/watch?v=vqAEdsnNboY",
                 "https://www.youtube.com/watch?v=sVz-5ZNCueM",
                 "https://www.youtube.com/watch?v=FJManH2Nv8k",
                 "https://www.youtube.com/watch?v=WVLUk5tOfXc",
                 "https://www.youtube.com/watch?v=eMRRdk8xHr4",
                 "https://www.youtube.com/watch?v=fiUxO1chYDY",
                 "https://www.youtube.com/watch?v=mUCvQtYKHns"
                 ]
    await ctx.send(f'{random.choice(responses)}')


"""Embeds"""


@client.command(brief="Bot source credits and other info")
async def info(ctx):  # embed is the name of the command: >embed

    embed = discord.Embed(title="INFORMATION", description="discord contact: rawndawg#5543", color=discord.Color.gold())

    embed.add_field(name="Tools🛠⚙", value="ヾ[Pycharm IDE](https://www.jetbrains.com/pycharm/),\n"
                    "ヾ[YouTube video (1)](https://www.youtube.com/watch?v=ZNA7Eij3UmY&feature=youtu.be)\n"
                    "ヾ[YouTube Video (2)](https://www.youtube.com/watch?v=xdg39s4HSJQ)\n"
                    "ヾ[Ffmpeg](https://ffmpeg.org)\n"
                    "ヾ[youtube.dll](https://youtube-dl.org)\n "
                    "ヾ[Documentation](https://discordpy.readthedocs.io/en/latest/) @ "
                    "https://discordpy.readthedocs.io/en/latest/", inline=True)

    await ctx.send(embed=embed)


@client.command(brief="work-in-progress")
async def musicdoc(ctx):
    embed = discord.Embed(title="Your Title", description="A description", color=discord.Color.blurple())

    embed.add_field(name="Some field", value="Some value", inline=True)
    embed.add_field(name="Another field", value="Another value", inline=False)

    await ctx.send(embed=embed)


@client.command(brief="your profile picture enlarged")
async def wat(ctx):
    idk = "👤"
    embed = discord.Embed(Title="idk", description=f"{idk}", color=discord.Color.dark_theme())
    embed.set_thumbnail(url=ctx.author.avatar_url)
    await ctx.send(embed=embed)


@client.command(name='funfact',
                brief='Learn something new!',
                description="Ronald's hand-picked fun facts!",
                aliases=['ronfact', 'intfact', 'dailyfact', 'interestingfact'],
                pass_context=True)
async def fact(ctx):
    responses = ["Christian Bale reportedly studied Tom Cruise’s mannerisms to prepare for his role",
                 "Gene Autry is the only person to be awarded stars in all five categories on the Walk of Fame",
                 "The word “PEZ” comes from the German word for peppermint – PfeffErminZ.",
                 "The hashtag symbol is technically called an octothorpe.",
                 "There are 11 U.S. states have land farther south than the most northern point of Mexico",
                 "There is a Boring, Oregon and a Dull, Scotland. They have been sister cities since 2012.",
                 "The Sahara is the largest non-polar desert in the world.",
                 "It’s been said that nearly 3% of the ice in Antarctic glaciers is penguin urine.",
                 "The first tiger shark to hatch inside of its mother’s womb eats all the other embryos",
                 "The the Kola Superdeep Borehole in Russia is the world’s deepest hole.",
                 "King Henry VIII had a “Groom of the Stool”",
                 "High heeled shoes were originally created for men.",
                 "Up to 12 million Dum Dums are made every single day.",
                 "Baby porcupines are called “porcupettes”.",
                 "Bubble Wrap was originally intended to be used as 3D wallpaper.",
                 "Americans consume around 150 million hot dogs on 4th of July each year.",
                 "President Richard Nixon was at Disney World when he infamously proclaimed, 'I am not a crook.'",
                 "Reno, Nevada is west of Los Angeles, California.",
                 "Since 1945, all British tanks have come equipped with tea making facilities.",
                 "India and China are the only countries in the world with populations above 1 billion people.",
                 "The U.S. Supreme Court has its own private basketball court.",
                 "Roughly 30% of the Earth’s remaining mineral resources can be found in Africa.",
                 "A snail can sleep for three years.",
                 "Earth’s highest point on land (Mt. Everest), and lowest (Dead Sea), are both found in Asia.",
                 "Indonesia is made up of over 17,000 islands.",
                 "When spliced together, there are 26 minutes of quiet staring in the Twilight film series.",
                 "There is no spot in Central America more than 125 miles from the ocean.",
                 "There’s a village in Norway called Hell, and it freezes over every winter.",
                 "Pluto’s average distance from the Sun is 3,670,050,000 miles.",
                 "With 94% identical DNA, Chimpanzees are the closest living relatives to humans.",
                 "Tootsie Rolls were used as part of the rations for World War II soldiers.",
                 "A pluot is a hybrid between a plum and a apricot.",
                 "Aulophobia is an exaggerated or irrational fear of flutes",
                 "Monaco is the most densely populated nation in the world.",
                 "Elephants can’t jump.",
                 "The Atacama Desert is the driest non-polar region on Earth.",
                 "The U.S. Supreme Court has previously ruled that tomatoes are vegetables.",
                 "Snakes can help predict earthquakes.",
                 "Crows can hold grudges against specific individual people.",
                 "The oldest “your mom” joke was discovered on a 3,500 year old Babylonian tablet.",
                 "So far, two diseases have successfully been eradicated: smallpox and rinderpest.",
                 "7% of American adults believe that chocolate milk comes from brown cows.",
                 "If you lift a kangaroo’s tail off the ground it can’t hop.",
                 "Most Korean people don’t have armpit odor.",
                 "The original London Bridge is now in Arizona.",
                 "During your lifetime, you will produce enough saliva to fill two swimming pools.",
                 "Movie trailers were originally shown after the movie, which is why they were called 'trailers'.",
                 "The smallest bone in your body is in your ear.",
                 "Tennis players are not allowed to swear when they are playing in Wimbledon.",
                 "Only 5% of the ocean has been explored.",
                 "The top six foods that make your fart are beans, corn, bell peppers, cauliflower, cabbage and milk.",
                 "The United States Navy has started using Xbox controllers for their periscopes.",
                 "A sheep, a duck and a rooster were the first passengers in a hot air balloon.",
                 "The average male gets bored of a shopping trip after 26 minutes.",
                 "95% of people text things they could never say in person.",
                 "A crocodile can’t poke its tongue out.",
                 "Sea otters hold hands when they sleep so they don’t drift away from each other.",
                 "Hewlett-Packard’s (also known as HP) name was decided in a coin toss in 1939.",
                 "There is a total of 1,710 steps in the Eiffel Tower.",
                 "The Pokémon Hitmonlee and Hitmonchan are based off of Bruce Lee and Jackie Chan.",
                 "Pigs are very smart animals.",
                 "Los Angeles’s full name is 'El Pueblo de Nuestra Senora la Reina de los Angeles de Porciuncula.'",
                 "There is official Wizard of New Zealand.",
                 "The average person walks the equivalent of five times around the world in their lifetime.",
                 "The world record for stuffing drinking straws into your mouth at once is 459.",
                 "The feeling of getting lost inside a mall is known as the Gruen transfer.",
                 "The hottest spot on the planet is in Libya.",
                 "The elevation in an airplane can have a detrimental effect on our ability to taste things.",
                 "Only two mammals like spicy food: humans and the tree shrew.",
                 "The M's in M&Ms stand for 'Mars' and 'Murrie.'",
                 "Marie Curie is the only person to earn a Nobel prize in two different sciences.",
                 "The English word with the most definitions is 'set.'",
                 "Pigeons can tell the difference between a painting by Monet and Picasso.",
                 "The dot over the lower case 'i' or 'j' is known as a 'tittle.'",
                 "Chewing gum boosts concentration.",
                 "The first computer was invented in the 1940s.",
                 "Alan Turing and his code-breaking team broke the Enigma Code during WWII at Bletchley park, UK",
                 "The unicorn is the national animal of Scotland.",
                 "'E' is the most common letter and appears in 11 percent of all english words.",
                 "The healthiest place in the world is in Panama.",
                 "Pringles aren't technically chips.",
                 "Showers really do spark creativity.",
                 "Abraham Lincoln's bodyguard left his post at Ford's Theatre to go for a drink.",
                 "Water makes different pouring sounds depending on its temperature.",
                 "Less than 20 percent of laughter comes after jokes",
                 "One man has saved more than 200 people from suicide on the Golden Gate Bridge.",
                 "Koalas have fingerprints.",
                 "Humans are just one of the estimated 8.7 million species on Earth.",
                 "Riding a roller coaster could help you pass a kidney stone.",
                 "Bee hummingbirds are so small they get mistaken for insects.",
                 "Sea lions can dance to a beat.",
                 "Nutmeg can be fatally poisonous.",
                 "The first mobile device to be called an 'iPhone' was made by Cisco, not Apple",
                 "The Comic Sans font came from an actual comic book.",
                 "The man who wrote Dracula never visited Transylvania.",
                 "The Australian government banned the word 'mate' for a day.",
                 "Tornadoes can cause 'fish rain.'",
                 "Star Trek's Scotty stormed the beach at Normandy.",
                 "Apple Pie isn't actually American.",
                 "Pigs are constitutionally protected in Florida.",
                 "The fire hydrant patent was lost in a fire.",
                 "Saudi Arabia imports camels from Australia.",
                 "One man, Tsutomu Yamaguchi, Tsutomu Yamaguchi, survived two atomic bombs.",
                 "The cast of Friends still earns around $20 million each year.",
                 "In 2011, more than 1 in 3 divorce filings in the U.S. contained the word 'Facebook.'"]
    embed = discord.Embed(title="Your Fact", description=f"{random.choice(responses)}", color=discord.Color.dark_red())
    await ctx.send(embed=embed)


@client.command(name='discquestion',
                brief='A random question asked by the bot',
                description='A topic to spark conversation',
                aliases=['deepq', 'disc', 'deepquestion', 'dquestion', 'discussion', 'dq'])
async def discq(ctx):
    responses = ["Have you ever farted in an elevator?",
                 "True or false? You have a crush on [fill in the blank].",
                 "Of the people in this room, who do you want to trade lives with?",
                 "What are some things you think about when sitting on the toilet?",
                 "Did you have an imaginary friend growing up?",
                 "Do you cover your eyes during a scary part in a movie?",
                 "Have you ever practiced kissing in a mirror?",
                 "Did your parents ever give you the “birds and the bees” talk?",
                 "What is your guilty pleasure?",
                 "What is your worst habit?",
                 "Has anyone ever walked in on you when going #2 in the bathroom?",
                 "Have you ever had a wardrobe malfunction?",
                 "Have you ever walked into a wall?",
                 "Do you pick your nose?",
                 "Do you sing in the shower?",
                 "Have you ever peed yourself?",
                 "What was your most embarrassing moment in public?",
                 "Have you ever farted loudly in class?",
                 "Do you ever talk to yourself in the mirror?",
                 "What would be in your web history that you’d be embarrassed if someone saw?",
                 "Have you ever tried to take a sexy picture of yourself?",
                 "Do you sleep with a stuffed animal?",
                 "Do you drool in your sleep?",
                 "Do you talk in your sleep?",
                 "Who is your secret crush?",
                 "Do you think [fill in the name] is cute?",
                 "Who do you like the least in this room, and why?",
                 "What does your dream boy or girl look like?",
                 "What is your go-to song for the shower?",
                 "Who is the sexiest person in this room?",
                 "How would you rate your looks on a scale of 1 to 10?",
                 "Rather have sex with [name] in secret or not have sex with that person, but everyone thinks you did?",
                 "What don't you like about me?",
                 "What color underwear are you wearing right now?",
                 "What was the last thing you texted?",
                 "Do you think you'll marry your current girlfriend/boyfriend?",
                 "How often do you wash your undergarments?",
                 "Have you ever tasted ear wax?",
                 "You rescuing people from a burning building and you had to leave one person behind from this room.",
                 "Have you ever farted and then blamed someone else?",
                 "Have you ever tasted your sweat?",
                 "What is the most illegal thing you have ever done?",
                 "Who is your favorite? Mom or Dad?",
                 "Would you trade your sibling in for a million dollars?",
                 "Would you trade in your dog for a million dollars?",
                 "What is your biggest pet peeve?",
                 "If you were allowed to marry more than one person, would you? Who would you choose to marry?",
                 "Would you rather lose your sex organs forever or gain 200 pounds?",
                 "Choose to save 100 people without anyone knowing about it or not save them but everyone praise you?",
                 "If you could only hear one song for the rest of your life, what would it be?",
                 "If you lost one day of your life every time you said a swear word, would you try not to do it?",
                 "Who in this room would be the worst person to date? Why?",
                 "Would you rather live with no internet or no A/C or heating?",
                 "If someone offered you $1 million to break up with your girlfriend/boyfriend, would you do it?",
                 "If you were reborn, what decade would you want to be born in?",
                 "If you could go back in time in erase one thing you said or did, what would it be?",
                 "Has your boyfriend or girlfriend ever embarrassed you?",
                 "Have you ever thought about cheating on your partner?",
                 "If you could suddenly become invisible, what would you do?",
                 "Have you ever been caught checking someone out?",
                 "Have you ever waved at someone thinking they saw you when really they didn't?",
                 "What's the longest time you've stayed in the bathroom, and why did you stay for that long?",
                 "What's the most unflattering school picture of you?",
                 "Have you ever cried because you missed your parents so much?",
                 "Would you rather be caught picking your nose or picking a wedgie?",
                 "Describe the strangest dream you've ever had. Did you like it?",
                 "Have you ever posted something on social media that you regret?",
                 "What is your biggest fear?",
                 "Do you pee in the shower?",
                 "Have you ever ding dong ditched someone?",
                 "The world ends next week, and you can do anything you want (even if it's illegal).What would you do?",
                 "Would you wear your shirt inside out for a whole day if someone paid you $100?",
                 "What is the most childish thing that you still do?",
                 "How far would you go to land the guy or girl of your dreams?",
                 "Tell us about a time you embarrassed yourself in front of a crush.",
                 "Have you ever kept a library book?",
                 "Who is one person you pretend to like, but actually don’t?",
                 "What children’s movie could you watch over and over again?",
                 "Do you have bad foot odor?",
                 "Do you have any silly nicknames?",
                 "When was the last time you wet the bed?",
                 "How many pancakes have you eaten in a single sitting?",
                 "Have you ever accidentally hit something with your car?",
                 "If you had to make out with any Disney character, who would it be?",
                 "Have you ever watched a movie you knew you shouldn’t?",
                 "Have you ever wanted to try LARP (Live Action Role-Play)?",
                 "What app on your phone do you waste the most time on?",
                 "Have you ever pretended to be sick to get out of something? If so, what was it?",
                 "What is the most food you’ve eaten in a single sitting?",
                 "Do you dance when you’re by yourself?",
                 "Would you have voted for or against Trump?",
                 "What song on the radio do you sing with every time it comes on?",
                 "Do you sleep with a stuffed animal?",
                 "Do you own a pair of footie pajamas?",
                 "Are you scared of the dark?",
                 "What ‘As seen on TV’ product do you secretly want to buy?",
                 "Do you still take bubble baths?",
                 "If you were home by yourself all day, what would you do?",
                 "How many selfies do you take a day?",
                 "What is something you’ve done to try to be ‘cooler’?",
                 "When was the last time you brushed your teeth?",
                 "Have you ever used self-tanner?",
                 "What do your favorite pajamas look like?",
                 "Do you have a security blanket?",
                 "Have you ever eaten something off the floor?",
                 "Have you ever butt-dialed someone?",
                 "Do you like hanging out with your parents?",
                 "Have you ever got caught doing something you shouldn’t?",
                 "What part of your body do you love, and which part do you hate?",
                 "Have you ever had lice?",
                 "Have you ever pooped your pants?",
                 "What was the last R-rated movie you watched?",
                 "Do you lick your plate?",
                 "What is something that no one else knows about you?",
                 "Do you write in a diary?",
                 "What is the worst date you’ve ever been on?",
                 "Have you ever had a crush on a friend’s boyfriend/girlfriend?",
                 "If you had to make out with a boy at school, who would it be?",
                 "Would you rather go for a month without washing your hair or go for a day without wearing a bra?",
                 "Have you ever asked someone out?",
                 "Have you ever had a crush on a person at least 10 years older than you?",
                 "Who is the worst kisser you’ve kissed?",
                 "What size is your bra?",
                 "Do you wear tighty whities or granny panties?",
                 "Do you ever admire yourself in the mirror?",
                 "Has a crush ever found out you liked them and turned you down?",
                 "Have you ever been stood up on a date?",
                 "What’s the most embarrassing thing you’ve done regarding your crush?",
                 "Do you secretly love Twilight?",
                 "Have you ever wanted to be a cheerleader?",
                 "Who is the hottest? Hagrid, Dumbledore, or Dobby?",
                 "If you could marry any celebrity, who would it be?",
                 "What do you do to get yourself 'sexy'?",
                 "Who is your current crush?",
                 "What hairstyle have you always wanted, but never been willing to try?",
                 "What’s the most embarrassing thing you’ve said or done in front of someone you like?",
                 "What part of your body do you love, and which part do you hate?",
                 "Who is your celebrity crush?",
                 "If you could change one thing about your body, what would it be?",
                 "Who was your first kiss? Did you like it?",
                 "Who are you jealous of?",
                 "If you could be another girl at our school, who would you be?",
                 "Would you kiss a guy on the first date? Would you do more than that?",
                 "Who are the top five cutest guys in our class? Rank them.",
                 "How many kids do you want to have in the future?",
                 "Who do you hate the most?",
                 "If you could go out on a date with a celebrity, who would it be?",
                 "If you were stranded on a deserted island, who would you want to be stranded with from our school?",
                 "Have you ever flirted with your best friend’s siblings?",
                 "Have you ever been dumped? What was the reason for it?",
                 "Jock, nerd, or bad guy?",
                 "Have you ever had a crush on friend's boyfriend?",
                 "Who is your first pick for prom?",
                 "What's the sexiest thing about a guy?",
                 "What's the sexiest thing about a girl?",
                 "What's one physical feature that you would change on yourself if you could?",
                 "Would you rather be a guy than a girl? Why?",
                 "Describe your dream career.",
                 "If you could eat anything you wanted without getting fat, what would that food be?",
                 "If you had to do a game show with someone in this room, who would you pick?",
                 "Would you go a year without your phone if it meant you could marry the person of your dreams?",
                 "You are going to be stuck on a desert island, and you can only bring five things. List them.",
                 "If you could only wear one hairstyle for the rest of your life, choose curly hair or straight hair?",
                 "You have to give up one makeup item for the rest of your life. What is it?",
                 "Would you date someone shorter than you?",
                 "If someone paid you $1000 to wear your bra outside your shirt, would you do it?",
                 "Who would you hate to see naked?",
                 "How long have you gone without a shower?",
                 "If you could only text one person for the rest of your life, but never see them, Who?",
                 "How long have you gone without brushing your teeth?",
                 "What's one thing you would never eat on a first date?",
                 "What have you seen that you wish you could unsee?",
                 "If you could be reincarnated into anyone's body, who would you want to become?",
                 "If you switched genders for the day, what would you do?",
                 "What's one food that you will never order at a restaurant?",
                 "What's the worst weather to be stuck outside in if all you could wear was a bathing suit?",
                 "If your car broke down in the middle of the road, who here would be last person you would call? Why?",
                 "What's the most useless piece of knowledge you know?",
                 "What did you learn in school that you wish you could forget?",
                 "Is it better to use shampoo as soap or soap as shampoo?",
                 "If you ran out of toilet paper, would you consider wiping with the empty roll?",
                 "What would be the worst part about getting pantsed in front of your crush?",
                 "If you could only use one swear word for the rest of your life, which one would you choose?",
                 "What's the best thing to say to your friend that would be the worst thing to say to your crush?",
                 "Who do you think is the Beyonce of the group?",
                 "Would you rather eat dog food or cat food?",
                 "If you had nine lives, what would you do that you wouldn't do now?",
                 "If you could play a prank on anyone without getting caught, who would you play it on?",
                 "What would the prank be?",
                 "Have you ever pretended to like a gift? How did you pretend?",
                 "Would you rather not shower for a month, or eat the same meal every day for a month?",
                 "What animal most closely resembles your eating style?",
                 "Choose to never sweat for the rest of your life or never have to use the bathroom again.",
                 "If you could spend every waking moment with your gf or bf, would you?",
                 "If you had to date someone else's boyfriend, who would it be?",
                 "Who's hotter? You or your friend?",
                 "Have you ever shared your friend's secret with someone else?",
                 "Rate everyone in the room from 1 to 10, with 10 being the hottest.",
                 "Would you share a toothbrush with your best friend?",
                 "Rate everyone in the room from 1 to 10, with 10 being the best personality.",
                 "Have you ever ignored a friend's text? Why did you do it?",
                 "Have you ever lied to your best friend?",
                 "Would you let a friend cheat on a test?",
                 "If your friend asked you to lie for her and you knew you would get in trouble, would you do it?",
                 "If one of your friends were cheating with your other friend's boyfriend, what would you do?",
                 "Would you ditch your friends if you could become the most popular girl in school?",
                 "If you had to choose, who would you stop being friends with?",
                 "Name one thing you would change about each person in this room.",
                 "If you had to trade your friend in for the celebrity crush of your dreams, which friend you choose?",
                 "You win a trip and are allowed to bring two people. Who do you pick?",
                 "On an overnight trip, would you rather share a bed with your best friend or someone of opposite sex",
                 "If you could swap one physical feature with your best friend, what would that be?",
                 "If your best friend had B.O., would you tell her?",
                 "What is the most annoying thing about your best friend?",
                 "Do you currently have a crush on anyone?",
                 "Describe what your crush looks like.",
                 "What is your crush's personality like?",
                 "Is there anything about your life you would change?",
                 "Who do you hate, and why?",
                 "What's your biggest pet peeve?",
                 "How many people have you kissed?",
                 "What's your biggest turn-on?",
                 "If you could date anyone in the world, who would you date?",
                 "Would you rather be skinny and hairy or fat and smooth?",
                 "Who would you ask to prom if you could choose anyone?",
                 "Describe your perfect date.",
                 "Would you ever date two people at once if you could get away with it?",
                 "You have to delete every app on your except for five. Name the five you would keep.",
                 "Have you ever sent out a nude Snapchat?",
                 "Have you ever received a nude selfie? Who was it from?",
                 "Have you ever gotten mad at a friend for posting an unflattering picture of you?",
                 "Have you ever had a crush on a teacher?",
                 "Who do you think would make the best kisser? (List a few people for them to choose.)",
                 "Have you ever sent someone the wrong text?",
                 "Have you ever cursed at your parents? Why?",
                 "Who do you think is the cutest person in our class?",
                 "What is the most attractive feature on a person?",
                 "What the biggest deal-breaker for you?",
                 "How far would you go on a first date?",
                 "Have you ever regretted something you did to get a crush's attention?",
                 "Would you ever be mean to someone if it meant you could save your close friend from embarrassment?",
                 "Of the people at our school, who do you think would make the best president?",
                 "If we didn't have a dress code, what would you wear to school that you can't wear now?",
                 "Describe what makes someone husband or wife material.",
                 "If you could make $1 million, would you drop out of school?",
                 "What is your worst habit?",
                 "What's one thing you do that you don't want anyone to know about?",
                 "Do you frequently stalk anyone on social media? Who?",
                 "If you had to choose between dating someone ugly, good in bed or dating someone hot + bad in bed",
                 "If you could be invisible, who would you spy on?",
                 "Who are the top 5 hottest girls at our school? In our class?",
                 "Who in this room would you make out with?",
                 "If you could date one of your bro's girlfriends, who would it be?",
                 "What your favorite body part?",
                 "When was the last time you flexed in the mirror?",
                 "Describe your perfect partner.",
                 "Have you ever been in love?",
                 "Blonde or brunette?",
                 "What turns you on the most?",
                 "If your parents hated your girlfriend, would you dump her?",
                 "If your girlfriend hated your best friend, what would you do?",
                 "Who is your biggest celebrity crush?",
                 "Would you take steroids?",
                 "Have you ever had a crush on a friend's girlfriend?",
                 "Who are you jealous of?",
                 "Who do you think is the hottest in our group?",
                 "What is your biggest turn-off?",
                 "Have you ever been rejected by someone?",
                 "If you had to choose between being poor and smart or being rich and dumb, what would you choose?",
                 "What have you lied to your partner about?",
                 "Have you ever cheated on your partner?",
                 "Would you go out with an older woman?",
                 "Do you have a crush on someone from another school?",
                 "Boxers or briefs?",
                 "When was the last time you cried?",
                 "Have you ever had a crush on a friend's girlfriend?",
                 "If you could make out with someone else's girl, who would it be?",
                 "If every time you checked out a girl's body, you would gain 5 pounds, how often would you do it?",
                 "Have you ever lied about your age?",
                 "Have you ever fallen in love at first sight?",
                 "If a girl you didn't like had a crush on you, how would you act around her?",
                 "What if she was your friend?",
                 "What would you do if you found out your girlfriend liked someone else?",
                 "If we formed a boy band, who here would make the best lead singer?",
                 "Who do you want to make out with the most?",
                 "If you had to flash just one person in this room, who would it be?",
                 "If you haven't had your first kiss yet, who in this room do you want to have your first kiss with?",
                 "Of the people in this room, who would you go out with?",
                 "Describe the most attractive thing about each person in this room.",
                 "Who here do you think is the best flirt?",
                 "Who has the best smile?",
                 "Who has the cutest nose?",
                 "How about prettiest eyes?",
                 "Who's the funniest in this room?",
                 "What's one thing you would never do in front of someone you had a crush on?",
                 "How often do you check yourself out in the mirror when you're on a date?",
                 "Who here do you think would be the best kisser?",
                 "Who has the best dance moves?",
                 "If you could have one physical feature of someone in this room, what would that be?",
                 "What is your wildest fantasy?",
                 "How far would you go with someone you just met and will never see again?",
                 "Rate me on a scale of 1 to 10, with 10 being the hottest.",
                 "If I was a food, what would I be, and how would you eat me?",
                 "Would you choose a wild, hot relationship or a calm and stable one?",
                 "If you had one week to live and you had to marry someone in this room, who would it be?",
                 "If you only had 24 hours to live and you could do anything with anyone in this room, who + what?",
                 "What's your biggest turn-on?",
                 "And your biggest turn-off?",
                 "Would you go out with me if I was the last person on earth?",
                 "What's the most flirtatious thing you've ever done?",
                 "What's the sexiest thing about [fill in the name of a person in the room]?",
                 "If you could go on a romantic date with anyone in this room, who would you pick?",
                 "If you had to delete one app from your phone, which one would it be?",
                 "What is your greatest fear in a relationship?",
                 "Go around the room and say one positive and one negative thing about each person.",
                 "What is one disturbing fact I should know about you?",
                 "Have you ever smoked?",
                 "Have you ever tried drugs?",
                 "What about alcohol?",
                 "What's the craziest thing you've done while under the influence?",
                 "If trapped for three days on an island, who are 3 people in this room you would bring with + why?",
                 "Would you go to a nude beach?",
                 "Who's the most annoying person in this room?",
                 "Are you still a virgin?",
                 "If you had to marry someone in this room, who would it be?",
                 "Do you have hidden piercings or tattoos?",
                 "How long was your longest relationship?",
                 "If you could have one celebrity follow you on Instagram, who would that be?",
                 "Do you want to get married one day?",
                 "Do you want to have kids? How many?",
                 "Would you ever get into a long-distance relationship?",
                 "Describe the person of your dreams.",
                 "What would you do if you found out you flunked school?",
                 "If you're girlfriend or boyfriend broke up with you at school, what would you do?",
                 "If you had the power to fire one teacher, who would it be?",
                 "Basketball, baseball, or football?",
                 "What was your first job?",
                 "If you don't have one yet, where would you want to work?",
                 "How many hours would you spend online if you didn't have school or homework?",
                 "How tall do you want to be?",
                 "What's your biggest fear about college?",
                 "What are you most excited about?",
                 "Would you want your best friend to go to the same college as you?",
                 "Would you want your current boyfriend or girlfriend to go to the same college as you?",
                 "Who do you think is the hottest celebrity?",
                 "What's your dream job?",
                 "What was a rumor that went around about you?",
                 "Have you ever failed a class?",
                 "If you had the power to fire one teacher, who would that be?",
                 "If you could plan a class prank knowing you'll never get caught, what would the prank be?",
                 "Have you ever cheated on a test?",
                 "Have you ever had a crush on a teacher? Who?",
                 "Who would you take to prom?",
                 "Have you ever made out at school?",
                 "Who would you never ever want to sit next to in class?",
                 "Have you ever been late to class?",
                 "What's the most embarrassing thing you've ever done in front of a teacher?",
                 "Have you ever stuck gum under a desk?",
                 "What do you think is better: tests or essays?",
                 "Have you ever eaten lunch by yourself? Why?",
                 "If you had to take one class for the rest of your life, what class, and who would the teacher be?",
                 "If you wanted to make out on campus, where would you do it?",
                 "Have you ever gotten into a fight on school grounds?",
                 "What was the worst score you’ve ever gotten on a test?",
                 "Have you ever fallen asleep in class?",
                 "Have you ever gotten detention or been suspended?",
                 "If you were invisible, would you sneak a peek in the other locker room?",
                 "If so, who would you be hoping to see?",
                 "Who's the hottest teacher at our school?",
                 "What's the worst class to have first period?",
                 "If you had to take a person from another grade to prom, who would that be?",
                 "Have you ever flashed someone?",
                 "Have you ever sexted anyone?",
                 "Have you ever been to a nudist beach? Would you consider going?",
                 "Would you ever consider posing for Playboy?",
                 "Who has seen you without clothes on?",
                 "Have you ever seen a naughty magazine?",
                 "Have you ever sent a nude selfie? Who would you send it to?",
                 "Have you ever searched for something dirty on the internet?",
                 "Who do you most want to sleep with, out of everyone here?",
                 "What's your favorite body part on your partner?",
                 "How many people have you kissed?",
                 "Have you ever been attracted to the same sex?",
                 "When and where was your first kiss? Who was it with?",
                 "When did you lose your virginity, and to whom did you lose it?",
                 "What's your ultimate sexual fantasy?",
                 "Would you go out with an older guy/girl? How old is too old?",
                 "Do you sleep in the nude?",
                 "How much money would we have to pay you for you to agree to flash your boobs?",
                 "Have you ever been in a 'friends with benefits' situation?",
                 "If you had to go skinny dipping with someone, who in this room would you choose?",
                 "If I paid you $100, would you wear your sexiest clothes to class?"]
    embed = discord.Embed(title="Discussion Q:", description=f"{random.choice(responses)}", color=discord.Color.blue())
    await ctx.send(embed=embed)


@client.command(aliases=['myfortune'])
async def fortune(ctx):
    responses = [
        "A beautiful, smart, and loving person will be coming into your life.",
        "A dubious friend may be an enemy in camouflage.",
        "A feather in the hand is better than a bird in the air.",
        "A fresh start will put you on your way.",
        "A friend asks only for your time not your money.",
        "A friend is a present you give yourself.",
        "A gambler not only will lose what he has, but also will lose what he doesn’t have.",
        "A golden egg of opportunity falls into your lap this month.",
        "A good friendship is often more important than a passionate romance.",
        "A good time to finish up old tasks.",
        "A hunch is creativity trying to tell you something.",
        "A lifetime friend shall soon be made.",
        "A lifetime of happiness lies ahead of you.",
        "A light heart carries you through all the hard times.",
        "A new perspective will come with the new year.",
        "A person is never to old to learn.",
        "A person of words and not deeds is like a garden full of weeds.",
        "A pleasant surprise is waiting for you.",
        "A short pencil is usually better than a long memory any day.",
        "A small donation is call for. It’s the right thing to do.",
        "A smile is your personal welcome mat.",
        "A smooth long journey! Great expectations.",
        "A soft voice may be awfully persuasive.",
        "A truly rich life contains love and art in abundance.",
        "Accept something that you cannot change, and you will feel better.",
        "Adventure can be real happiness.",
        "Advice is like kissing. It costs nothing and is a pleasant thing to do.",
        "Advice, when most needed, is least heeded.",
        "All the effort you are making will ultimately pay off.",
        "All the troubles you have will pass away very quickly.",
        "All will go well with your new project.",
        "All your hard work will soon pay off.",
        "Allow compassion to guide your decisions.",
        "An acquaintance of the past will affect you in the near future.",
        "An agreeable romance might begin to take on the appearance.",
        "An important person will offer you support.",
        "An inch of time is an inch of gold.",
        "Any decision you have to make tomorrow is a good decision.",
        "At the touch of love, everyone becomes a poet.",
        "Be careful or you could fall for some tricks today.",
        "Beauty in its various forms appeals to you.",
        "Because you demand more from yourself, others respect you deeply.",
        "Believe in yourself and others will too.",
        "Believe it can be done.",
        "Better ask twice than lose yourself once.",
        "Bide your time, for success is near.",
        "Carve your name on your heart and not on marble.",
        "Change is happening in your life, so go with the flow!",
        "Competence like yours is underrated.",
        "Congratulations! You are on your way.",
        "Could I get some directions to your heart?",
        "Courtesy begins in the home.",
        "Courtesy is contagious.",
        "Curiosity kills boredom. Nothing can kill curiosity.",
        "Dedicate yourself with a calm mind to the task at hand.",
        "Depart not from the path which fate has you assigned.",
        "Determination is what you need now.",
        "Diligence and modesty can raise your social status.",
        "Disbelief destroys the magic.",
        "Distance yourself from the vain.",
        "Do not be intimidated by the eloquence of others.",
        "Do not demand for someone’s soul if you already got his heart.",
        "Do not let ambitions overshadow small success.",
        "Do not make extra work for yourself.",
        "Do not underestimate yourself. Human beings have unlimited potentials.",
        "Do you know that the busiest person has the largest amount of time?",
        "Don’t be discouraged, because every wrong attempt discarded is another step forward.",
        "Don’t confuse recklessness with confidence.",
        "Don’t just spend time. Invest it.",
        "Don’t just think, act!",
        "Don’t let friends impose on you, work calmly and silently.",
        "Don’t let the past and useless detail choke your existence.",
        "Don’t let your limitations overshadow your talents.",
        "Don’t worry; prosperity will knock on your door soon.",
        "Each day, compel yourself to do something you would rather not do.",
        "Education is the ability to meet life’s situations.",
        "Embrace this love relationship you have!",
        "Emulate what you admire in your parents.",
        "Emulate what you respect in your friends.",
        "Every flower blooms in its own sweet time.",
        "Everyday in your life is a special occasion",
        "Everywhere you choose to go, friendly faces will greet you.",
        "Expect much of yourself and little of others.",
        "Failure is the chance to do better next time.",
        "Failure is the path of lease persistence.",
        "Fear and desire – two sides of the same coin.",
        "Fearless courage is the foundation of victory.",
        "Feeding a cow with roses does not get extra appreciation.",
        "First think of what you want to do; then do what you have to do.",
        "Follow the middle path. Neither extreme will make you happy.",
        "For hate is never conquered by hate. Hate is conquered by love.",
        "For the things we have to learn before we can do them, we learn by doing them.",
        "Fortune Not Found: Abort, Retry, Ignore?",
        "From listening comes wisdom and from speaking repentance.",
        "From now on your kindness will lead you to success.",
        "Get your mind set – confidence will lead you on.",
        "Get your mind set…confidence will lead you on.",
        "Go for the gold today! You’ll be the champion of whatever.",
        "Go take a rest; you deserve it.",
        "Good news will be brought to you by mail.",
        "Good news will come to you by mail.",
        "Good to begin well, better to end well.",
        "Happiness begins with facing life with a smile and a wink.",
        "Happiness will bring you good luck.",
        "Happy life is just in front of you.",
        "Hard words break no bones, fine words butter no parsnips.",
        "Have a beautiful day.",
        "He who expects no gratitude shall never be disappointed.",
        "He who knows he has enough is rich.",
        "He who knows others is wise. He who knows himself is enlightened.",
        "How you look depends on where you go.",
        "If certainty were truth, we would never be wrong.",
        "If you continually give, you will continually have.",
        "If you look in the right places, you can find some good offerings.",
        "Imagination rules the world.",
        "In order to take, one must first give.",
        "In the end all things will be known.",
        "It takes courage to admit fault.",
        "It is worth reviewing some old lessons.",
        "Like the river flow into the sea. Something are just meant to be.",
        "Long life is in store for you.",
        "Love lights up the world.",
        "Love truth, but pardon error.",
        "Man is born to live and not prepared to live.",
        "New ideas could be profitable.",
        "Now is the time to try something new.",
        "Place special emphasis on old friendship.",
        "Practice makes perfect.",
        "Savor your freedom – it is precious.",
        "Say hello to others. You will have a happier day.",
        "Self-knowledge is a life long process.",
        "Small confidences mark the onset of a friendship.",
        "Soon life will become more interesting.",
        "Stand tall. Don’t look down upon yourself.",
        "Success is a journey, not a destination.",
        "Swimming is easy. Stay floating is hard.",
        "Take the high road.",
        "The best prediction of future is the past.",
        "The harder you work, the luckier you get.",
        "There is no mistake so great as that of being always right.",
        "Use your eloquence where it will do the most good.",
        "Your mind is your greatest asset.",
        "Your moods signal a period of change.",
        "Your talents will be recognized and suitably rewarded.",
        "Your work interests can capture the highest status or prestige.",
        "Your loyalty is a virtue, but not when it’s wedded with blind stubbornness.",
        "Your love life will be happy and harmonious."]
    embed = discord.Embed(title="⚖ Fortune:", description=f"{random.choice(responses)}", color=discord.Color.dark_blue())
    await ctx.send(embed=embed)


@client.command(name='windowsshortcuts',
                brief='List of Built-in Windows Shortcuts',
                description='shortcuts to help you get around your Windows\ncomputer faster and increase productivity',
                aliases=['winshort', 'windows_shortcut', 'WindowsShortcuts', 'WS', 'ws', 'shortcuts'],
                pass_context=True)
async def win_shortcuts(ctx):
    embed = discord.Embed(title="Windows Shortcuts:", description=
                                "--Essentials:\n"
                                "[Windows key] = Start Menu\n"
                                "[Windows key] + [E] = File Explorer\n"
                                "[Ctr] + [Shift] + [Esc] = Task Manager\n"
                                "[Ctr] + [A]     = Select All\n"
                                "[Ctr] + [V]     = Paste\n"
                                "[Ctr] + [C]     = Copy\n"
                                "[Ctr] + [X]     = Cut\n"
                                "[Ctr] + [R]     = Refresh active window\n"
                                "[Ctr] + [F]     = Search Page (in any application)\n"
                                "[Alt] + [Left/Right Arrow] = Go Back/Forward\n"
                                "[Alt] + [F4] = Close active App\n"
                                "[Alt] + [Tab] = Switch btwn open apps (press Tab multiple times)\n"
                                "--Windows Key Shortcuts:\n"
                                "[Windows key] + [.] = Emoji Panel\n"
                                "[Windows key] + [Shift] + [S] = Clip/Snip\n"
                                "[Windows key] + [D] = Minimizes ALL applications\n"
                                "[Windows key] + [I] = Settings\n"
                                "[Windows key] + [G] = Xbox games bar\n"
                                "[Windows key] + [Alt] + [R] = Record active App\n"
                                "[Windows key] + [Alt] + [Prt Scn] = Screenshot\n"
                                "[Windows key] + [L] = Locks Device\n"
                                "[Windows key] + [R] = Run command\n"
                                "[Windows key] + [K] = Connected devices\n"
                                "[Windows key] + [V] = Clipboard Bin/History\n"
                                "[Windows key] + [+/-] = Magnifier\n"
                                "[Windows key] + [,] = Peek at desktop\n"
                                "[Windows key] + (Shift) + [0-9] = Open app position in taskbar\n(another instance)\n"
                                "[Windows key] + [Space] = Change keyboard layout/input language.\n"
                                "[Windows key] + [Tab] = Task View\n"
                          , colour=discord.Colour.dark_magenta())
    embed.add_field(name="More shortcuts here:",
                    value="https://www.windowscentral.com/best-windows-10-keyboard-shortcuts",
                    inline=True)
    embed.add_field(name="Help Forums:", value="[❔- link 1](https://www.windowscentral.com/windows-10-help)\n-or-\n"
                                               "[❓- link 2](https://answers.microsoft.com/en-us?auth=1)", inline=False)
    await ctx.send(embed=embed)


@client.command(aliases=['giveemoji', 'emoticon', 'emojirandom', 'randomemoji'])
async def emoji(ctx):
    responses = [":poop:",
                   ":smile:",
                   ":wink:",
                   ":laughing:",
                   ":blush:",
                   ":smiley:",
                   ":relaxed:",
                   ":smirk:",
                   ":heart_eyes:",
                   ":kissing_heart:",
                   ":kissing_closed_eyes:",
                   ":flushed:",
                   ":relieved:",
                   ":satisfied:",
                   ":grin:",
                   ":stuck_out_tongue_winking_eye:",
                   ":stuck_out_tongue_closed_eyes:",
                   ":grinning:",
                   ":kissing:",
                   ":kissing_smiling_eyes:",
                   ":stuck_out_tongue:",
                   ":sleeping:",
                   ":worried:",
                   ":frowning:",
                   ":anguished:",
                   ":open_mouth:",
                   ":grimacing:",
                   ":confused:",
                   ":hushed:",
                   ":expressionless:",
                   ":unamused:",
                   ":sweat_smile:",
                   ":sweat:",
                   ":disappointed_relieved:",
                   ":weary:",
                   ":pensive:",
                   ":disappointed:",
                   ":confounded:",
                   ":fearful:",
                   ":cold_sweat:",
                   ":persevere:",
                   ":cry:",
                   ":sob:",
                   ":joy:",
                   ":astonished:",
                   ":scream:",
                   ":angry:",
                   ":tired_face:",
                   ":rage:",
                   ":sleepy:",
                   ":yum:",
                   ":mask:",
                   ":sunglasses:",
                   ":dizzy_face:",
                   ":imp:",
                   ":smiling_imp:",
                   ":neutral_face:",
                   ":no_mouth:",
                   ":innocent:",
                   ":alien:",
                   ":yellow_heart:",
                   ":blue_heart:",
                   ":purple_heart:",
                   ":heart:",
                   ":green_heart:",
                   ":broken_heart:",
                   ":heartbeat:",
                   ":two_hearts:",
                   ":revolving_hearts:",
                   ":cupid:",
                   ":sparkling_heart:",
                   ":sparkles:",
                   ":star:",
                   ":star2:",
                   ":dizzy:",
                   ":boom:",
                   ":collision:",
                   ":anger:",
                   ":exclamation:",
                   ":question:",
                   ":grey_exclamation:",
                   ":grey_question:",
                   ":zzz:",
                   ":dash:",
                   ":sweat_drops:",
                   ":notes:",
                   ":musical_note:",
                   ":fire:",
                   ":hankey:",
                   ":poop:",
                   ":shit:",
                   ":+1:",
                   ":-1:",
                   ":ok_hand:",
                   ":punch:",
                   ":fist:",
                   ":v:",
                   ":wave:",
                   ":hand:"]
    embed = discord.Embed(title="emoji!", description=f"{random.choice(responses)}", color=discord.Color.orange())
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/779025578015719513/784906636597788682/unknown.png")
    embed.add_field(name="Information on Emojis - ", value="[wikipedia page](https://en.wikipedia.org/wiki/Emoji)")
    embed.add_field(name="Emoticons - ", value="[wikipedia page](https://en.wikipedia.org/wiki/Emoticon)")
    await ctx.send(embed=embed)


"""Server"""


@client.command(name='server',
                brief='Server Info')
async def fetchServerInfo(context):
    guild = context.guild
    await context.send(f'Server Name: {guild.name}')
    await context.send(f'Total Server Count: {len(client.guilds)}')
    await context.send(f'Server Owner: {guild.owner_id}{discord.WidgetMember.display_name}')
    for server in client.guilds:
        await context.send("Ronald Bot is Online on: ")
        await context.send(f"{server.name}")


@client.event
async def badwords(self, message):
    word_list = ['cheat', 'cheats', 'hack', 'hacks', 'internal', 'external', 'ddos', 'denial of service']

    # don't respond to ourselves
    if message.author == self.user:
        return

    message_content = message.content
    if len(message_content) > 0:
        for words in word_list:
            if words in message_content:
                await message.delete()
                await message.channel.send('Do not say that!')

    message.attachments = message.attachments
    if len(message.attachments) > 0:
        for attachment in message.attachments:
            if attachment.filename.endswith(".dll"):
                await message.delete()
                await message.channel.send("No DLL's allowed!")
            elif attachment.filename.endswith('.exe'):
                await message.delete()
                await message.channel.send("No EXE's allowed!")
            else:
                break


async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed():
        print("Current servers:")
        for server in client.guilds:
            print(server.name)
        await asyncio.sleep(5000)
    return


client.loop.create_task(list_servers())
client.run('Nzc3NjIxNDg0MTQ3MzEwNjYy.X7GGcQ.STnlDMC7u2-FCJ95Lk50jW7I5dE')
