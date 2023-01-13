import requests
import openai
from discord.ext import commands

# Setting the intents for the bot
intents = discord.Intents.all()

# Creating the bot with a command prefix of / and the intents defined above
bot = commands.Bot(command_prefix='/', intents=intents)

# Assigning the OpenAI API key to the openai module
openai.api_key = "OPENAI API KEY"

# The chat command that generates a text response using the OpenAI API
@bot.command()
async def chat(ctx, *, question):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=question,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    response = "```" + response["choices"][0]["text"] + "```"
    embed=discord.Embed(title="Response", description=response, color=0x87CEFA)
    await ctx.send(embed=embed)

# The clear command that clears the chat history in the current channel
@bot.command()
async def clear(ctx):
    await ctx.channel.purge()

# The image command that generates an image based on a user-inputted description
@bot.command()
async def image(ctx, *, description):
    message = await ctx.send("Processing your image...")
    response = requests.post(
        'https://api.openai.com/v1/images/generations',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {openai.api_key}'
        },
        json={
            'model': 'image-alpha-001',
            'prompt': f'{description}',
            'num_images':1,
            'size': '1024x1024',
            'response_format': 'url'
        }
    ).json()
    url = response['data'][0]['url']
    embed = discord.Embed(title="Response", color=0x87CEFA)
    embed.set_image(url=url)
    await message.edit(content='', embed=embed)

# Running the bot with the Discord bot token
bot.run('DISCORD BOT TOKEN')
