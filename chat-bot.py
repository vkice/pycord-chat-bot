import discord,os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

bot = commands.Bot(command_prefix=">>",
                   intents=discord.Intents.all(),
                   status=discord.Status.online,
                   activity=discord.Activity(type=discord.ActivityType.watching, name=" for chats")
                   )

@bot.event
async def on_ready():
    print(f"{bot.user} is online.")

cogs_list = [ # Not sure how to work with cogs? https://docs.pycord.dev/en/stable/ext/commands/cogs.html
    'slash',
    # 'monitor', # Uncomment and add a Channel ID to L18 of cogs/monitor.py to monitor a Discord channel
]

for cog in cogs_list:
    bot.load_extension(f'cogs.{cog}')
    print(f'Loaded {cog}')

bot.run(os.getenv('BOT_TOKEN'))