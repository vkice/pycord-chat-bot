# pycord-chat-bot
A simple chat bot for Discord, powered by OpenAI's ChatGPT and the Pycord Python library, a fork of Discord.py

This bot integrates the advanced conversational capabilities of ChatGPT4 into Discord, allowing users to interact with the bot in their servers for fun, information, or simply as a server assistant. Created as a fun personal project, but open to future suggestions and fine tuning!

Example using the Channel Monitoring Cog and a customized prompt to act like a Canadian human:
![Pycord Example Screenshot](https://kzp-public.s3.amazonaws.com/web/images/examples/pycord-chat-bot-example.png "Pycord Example Screenshot")

## Features

- **Conversational Interaction**: Engage in human-like conversations with ChatGPT4 by passing system messages describing how to respond
- **Information Retrieval**: Ask the bot to provide information on a wide range of topics
- **Custom Commands**: Create custom responses and commands tailored for your server
- **Message queueing**: Add context to your conversation by recalling a number of previous conversations without the use of an external database
- **Expandability**: Simply use my repo as a baseline to creating your own Discord bot using Python, even outside of ChatGPT

## Installation

To use this bot, you'll need to create a Discord Developer account, grab the bot token and invite the bot to your server. There's multiple ways to run the bot, but you could simply run it on your system's installed python as a test. You can also visit this article on my website for a [guide to setting this up](https://vkice.me/posts/discord-python-bot-docker-ecs-aws/#discord-developer-setup "Automatically Deploy Your Discord Python Bot into a Docker Container Hosted on ECS AWS") or read it in full on how to automate a CI/CD pipeline to deploy as a Docker container on AWS ECS.

You'll also need an API key from [OpenAI](https://platform.openai.com/api-keys), this will cost you money per request but for casual use it's not very significant. Be sure to set a usage limit so your friends don't drain your wallet!

Ensure your Discord and OpenAI tokens are kept secure!

1. **Clone the repository**
    ```bash
    git clone https://github.com/vkice/pycord-chat-bot.git
    cd pycord-chat-bot
    ```

2. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure your environment variables**
    - Rename `.env.example` to `.env`.
    - Fill in your Discord bot token and OpenAI API key

4. **Run the bot**
    ```bash
    python chat-bot.py
    ```

## Usage

Once the bot is running and invited to your server, you can start interacting with it using specific commands or by mentioning it.

Example commands:
- `/chat `: Get a ChatGPT response to your query, great for a one time use or one question rather than conversation because of how slash commands are treated in Discord
- `/image `: Generate an image with OpenAI's DALL-E based on your prompt which is sent as an image to the chat
- **Bonus! Channel Monitoring**: Right click a channel, grab the Channel ID, and place that in cogs/monitor.py L18 to automatically have conversations in a specific channel, with use of a slash command. This makes the interaction much more smoother!

## Acknowledgments

- OpenAI team for providing the GPT models and realistic AI behaviors
- Pycord team for maintaining an excellent Python library for creating Discord bots