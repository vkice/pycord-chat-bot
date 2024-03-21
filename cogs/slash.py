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
            image_url = image_resp.data[0].url
            
            response = requests.get(image_url) # Storing the URL into a new var as it will eventually time out and the image will be lost
            response.raise_for_status()  # Raises stored HTTPError, if one occurred.
            image_bytes = BytesIO(response.content) # BytesIO Object
            
            file = discord.File(fp=image_bytes, filename="prompt.png")
            await ctx.respond(file=file)
            
        except Exception as e:
            print("Error: {e}")
            await ctx.respond("Sorry, there was an issue either with the server or your prompt!")


def setup(bot):
    bot.add_cog(OpenAISlash(bot))