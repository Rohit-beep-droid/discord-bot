"""
My first ever Discord bot and first time working with an API

The bot is not complete since there are features I wanted to add
I could not due to external factors and life in general

I have decided to delete some features (kick, ban, unban), since
I believe they are unnecessary.

NOTE: I HAVE USED A SEPARATE JSON FILES FOR ASAMI'S RESPONSES
AND YOU MAY USE YOUR OWN JSON FILE

"""
import discord, random, typing, asyncio, requests, json
from discord.ext import commands
from asami_weather import attributes_parse, weather_msg, invalid_msg, visibility_parse
from discord.utils import get

intents = discord.Intents(members=True)
bot = discord.Client(intents=intents)
bot = commands.Bot(command_prefix = 'a!')

token = ''
weather_api_key = ''
bot.remove_command('help')

# EVENTS

@bot.event
async def on_ready():
    activity = discord.Game(name="Valorant | a!help")
    await bot.change_presence(status=discord.Status.online,activity=activity)
    print('{0.user} is online! Meow! Meow!'.format(bot))

@bot.event
async def on_member_join(ctx, member):
    print(f'Someone named {member.name} joined')
    embed = discord.Embed(title=f'Welcome {member.name}!', description="We are definetly so glad you are here.", color=discord.Color.green())
    await bot.channel.ctx.send(embed = embed)

@bot.event
async def on_member_leave(ctx, member):
    print(f'{member.name} has left.')
    embed = discord.Ember(title=f'Rip {member.user}', description="Meow! Down goes one more!",color=discord.Color.red())
    await bot.channel.ctx.send(embed = embed)

 # COMMANDS

@bot.command()
async def bite(ctx, member: discord.Member, *, reason='for being a hoe'):
    await ctx.send(f'{member.mention} just got bit {reason}!')

@bot.command()
async def swat(ctx, member: discord.Member, *, reason='for being a hoe'):
    await ctx.send(f'{member.mention} just got swatted {reason}!')

@bot.command()
async def meow(ctx, *, member: discord.Member):
    await ctx.send(f'{member.mention} Meow!')

@bot.command()
async def hello(ctx):
    await ctx.reply(random.choice(greetings))

@bot.command()
async def pat(ctx):
    await ctx.reply(random.choice(pats))

bot.counter = 0
@bot.command()
async def kiss(ctx):
    user = ctx.author.mention
    bot.counter+=1
    if bot.counter == 1:
        await ctx.reply(f'{user} Meow!')
    if bot.counter == 2:
        await ctx.reply(f"{user} I won't warn you again!")
    if bot.counter >= 3:
        await ctx.reply(f'{user} {random.choice(angry)}')

@bot.command()
async def feed(ctx):
    await ctx.reply(random.choice(hungry))

@bot.event
async def on_message(message):
    msg = message.content.lower()
    for word in response:
        if word in msg:
            await message.channel.send(random.choice(greetings))
            break
    await bot.process_commands(message)

# NEW FEATURE

@bot.command()
async def weather(ctx, message):
    location = message
    if len(location) >= 1:
        url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&units=imperial&appid={weather_api_key}'
        try:
            data = json.loads(requests.get(url).content)
            visibility = visibility_parse(data)
            data = attributes_parse(data)
            await ctx.send(embed=weather_msg(data, visibility, location))
        except KeyError:
            await ctx.send(embed=invalid_msg(location))

@bot.event
async def on_message(message):
    msg = message.content.lower()
    for word in response:
        if word in msg:
            await message.channel.send(random.choice(greetings))
            break
    await bot.process_commands(message)
    
# HELP COMMANDS

@bot.group(invoke_without_command=True)
async def help(ctx):
    print (f'{ctx.author.mention} has used help')
    embed = discord.Embed(title="Help", description="Use a!help <command> to see more information.",color=ctx.author.color)
    embed.add_field(name="Moderation",value="kick, ban, unban", inline=False)
    embed.add_field(name="Miscellaneous",value="bite, hello, feed, meow, pat, swat, smooch", inline=False)
    embed.add_field(name="New Feature(s)",value="weather")
    embed.add_field(name="Features",value="Weather Teller (Asami can sense the weather!)\n(Coming soon!)\n(Coming soon!)", inline=False)
    await ctx.send(embed = embed)

@help.command()
async def hello(ctx):
    embed = discord.Embed(title="Hello",description="Asami greets you back",color=ctx.author.color)
    embed.add_field(name="Syntax",value="a!hello")
    await ctx.send(embed=embed)

@help.command()
async def meow(ctx):
    embed = discord.Embed(title="Meow",description="Asami will meow at a member",color=ctx.author.color)
    embed.add_field(name="Syntax",value="a!meow <member>")
    await ctx.send(embed=embed)

@help.command()
async def pat(ctx):
    embed = discord.Embed(title="Pat",description="Pat Asami",color=ctx.author.color)
    embed.add_field(name="Syntax",value="a!pat")
    await ctx.send(embed=embed)

@help.command()
async def swat(ctx):
    embed = discord.Embed(title="Swat",description="Asami swats a member from the server",color=ctx.author.color)
    embed.add_field(name="Syntax",value="a!swat <member> [reason]")
    await ctx.send(embed=embed)

@help.command()
async def bite(ctx):
    embed = discord.Embed(title="Bite",description="Asami bites a member from the server",color=ctx.author.color)
    embed.add_field(name="Syntax",value="a!bite <member> [reason]")
    await ctx.send(embed=embed)

@help.command()
async def feed(ctx):
    embed = discord.Embed(title="Feed",description="Give our ever starving king food",color=ctx.author.color)
    embed.add_field(name="Syntax",value="a!feed")
    await ctx.send(embed=embed)

@help.command()
async def kiss(ctx):
    embed = discord.Embed(title="Kiss",description="Give Asami a kiss but be careful",color=ctx.author.color)
    embed.add_field(name="Syntax",value="a!kiss")
    await ctx.send(embed=embed)

@help.command()
async def weather(ctx):
    embed = discord.Embed(title="Weather",description="Asami can sense the current weather of a city",color=ctx.author.color)
    embed.add_field(name="Syntax",value="a!weather <city name>")
    await ctx.send(embed=embed)

bot.run(token)
