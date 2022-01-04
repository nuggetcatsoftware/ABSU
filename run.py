import os
import discord
from chatterbot import ChatBot
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatdata.pretrain import *
from discord.ext import commands
import time
import psutil
from chatdata.token import discord_token
chatbot = ChatBot(
    'Alpha',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand.',
            'maximum_similarity_threshold': 0.90
        },
        {
            'import_path': 'chatterbot.logic.MathematicalEvaluation',
            'default_response': 'I am sorry, but I do not understand (time).',
            'maximum_similarity_threshold': 0.40
        }
    ]
)

trainer=ChatterBotCorpusTrainer(chatbot)
trainer.train(
    "chatterbot.corpus.english.greetings",
    "chatterbot.corpus.english.conversations",
    "chatterbot.corpus.english.ai"
)
trainer=ListTrainer(chatbot)
trainer.train(conversation)
TOKEN=discord_token

bot = commands.Bot(command_prefix="^") #only for dev debuggers
start_time = time.time()
@bot.event
async def on_ready():
    for guild in bot.guilds:
        for channel in guild.text_channels :
            if str(channel) == "general" :
                await guild.me.edit(nick="Alpaca")
                await channel.send("Alpaca online!")
        print('Active in {}\n Member Count : {}'.format(guild.name,guild.member_count))
    print(f'{bot.user.name} has connected to discord and is now online')
    print("Connection time: \n")
    print("--- %s seconds ---" % (time.time() - start_time))
    print("STARTED!!")
    await bot.change_presence(activity=discord.Game("English"))


bot.remove_command('help')
async def on_member_join(member):
    await member.create_dm()
    embedVar = discord.Embed(title="Hello", description="What's up nerd! Don't forget to check out this bot by starting a new sentence with //! ", color=0xff0000)
    embedVar.add_field(name="Let's get started!", value="Type: (^help) to get started!!", inline=False)
    await member.dm_channel.send(f'Hi {member.name}')
    await member.dn_channel.send(embed=embedVar)

@bot.command(name="ping")
async def ping(ctx: commands.Context):
    await ctx.send(f"Pwaaaaa! {round(bot.latency * 1000)}ms")

@bot.command(name="help")
async def help(ctx:commands.Context):
    await ctx.send("start any sentence with // then speak your sentence and wait for the bot to generate a response")

@bot.command(name="debug")
async def debug(ctx:commands.Context):
        print("Debug command")
        await ctx.send("IF you are reading this: The bot has: \n 0: Exceptions raised \n Unknown number of warnings \n Bot is online")
        time.sleep(1)
        await ctx.send("Host clinet ram usage: ")
        await ctx.send(psutil.virtual_memory())
        before = time.monotonic()
        message = await ctx.send("Ping: ")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"Ping:  `{int(ping)}ms`")
@bot.listen()
async def on_message(message):
    if message.author == bot.user:
        return
    input = message.content.lower()
    input = str(input)
    if input.startswith("//"):
        input =input.replace("//",'')
        input= str(input)
        response = chatbot.get_response(input)
        conf=int(response.confidence)
        if response.confidence>=0.80:
            response=str(response)
            await message.channel.send(response)
            await message.channel.send("This message was sent with: " +conf + "confidence.")
        else:
            await message.channel.send("sorry, I am not confident saying this")
        await bot.process_commands(message)
bot.run(TOKEN)