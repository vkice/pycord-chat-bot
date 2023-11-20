from core_ai import Chat_Bot
from discord.ext import commands

chat_bot = Chat_Bot(environment="my_server")
class OpenAIMon(commands.Cog):

    def __init__(self, bot_: commands.bot):
        self.bot = bot_

    
    @commands.Cog.listener()
    async def on_message(self, message):
        if len(message.content) == 0:
            return
        if message.author == self.bot.user or message.content[0] == "!" or message.content[0] == "/":
            # These are our escape characters, use ! in the beginning of your message to ignore the bot but say something about it as example, change as needed.
            return
        
        channel = self.bot.get_channel(1234567890) # Enter your channel ID to monitor here
        if message.channel == channel:
        # if message.channel == channel and message.content[0] == "!":
        ### Alternative behavior, comment L19 uncomment L20, only monitor the channel only IF the specified prefix is mentioned! Remove L15 mentions as well if opting for this ###
            await chat_bot.message_respond(prompt=message.content, discord_message=message, msg_ctx=None)
            
        else:
            return
        
        
    async def error_handling(self, ctx, error):
        if isinstance(error):
            await ctx.send("Sorry, I've had an issue understanding you. What did you say?", reference=ctx.message)
            
        else:
            raise error

def setup(bot):
    bot.add_cog(OpenAIMon(bot))
    