import discord, os, openai
from core_ai import Chat_Bot
from discord.ext import commands

chat_bot = Chat_Bot(environment="my_server")
img_client = openai.OpenAI(api_key=os.environ['OPENAI_KEY'])

class OpenAISlash(commands.Cog):
        
    def __init__(self, bot_: commands.bot):
        self.bot = bot_

    # ChatGPT Slash
    @discord.slash_command(description="Send an input to ChatGPT")
    async def chat(self, ctx, prompt):
        
        await ctx.response.defer()
        await chat_bot.message_respond(prompt=prompt, discord_message=prompt, msg_ctx=ctx)

    # DALL-E Slash
    @discord.slash_command(description="Send an image generation")
    async def image(self, ctx, input):
        
        try:
            await ctx.defer()
            image_resp = img_client.images.generate( # Very basic, see https://platform.openai.com/docs/guides/images?context=node for additional parameters
                model="dall-e-3",
                prompt=input,
                n=1,
                size="1024x1024",
                quality="standard"
                )
            response = image_resp.data[0].url
            await ctx.respond(response)
            
        except Exception as e:
            print("Error: {e}")
            await ctx.respond("Sorry, there was an issue either with the server or your prompt!")


def setup(bot):
    bot.add_cog(OpenAISlash(bot))