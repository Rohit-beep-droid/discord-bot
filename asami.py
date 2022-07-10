"""
My first ever Discord bot and first time working with an API

The bot is not complete since there are features I wanted to add
I could not due to external factors and life in general

"""
import discord, random, typing, asyncio, requests, json
from discord.ext import commands
from asami_weather import data_parse, weather_message, invalid_location
from discord.utils import get

intents = discord.Intents(members=True)
bot = discord.Client(intents=intents)
bot = commands.Bot(command_prefix = 'a!')

with open("secret.json", 'r') as secrets_file:
    secret = json.load(secrets_file)

token = secret['token']
api_key = secret['api']
pats = secret['pats']
greetings = secret['greetings']
angry = secret['angry']
hungry = secret['hungry']
response = secret['response']
bot.remove_command('help')

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

@bot.command()
async def bite(ctx, member: discord.Member, *, reason='for being a hoe'):
    await ctx.send(f'{member.mention} just got bit {reason}!')

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member,*,reason=None):
    if reason == None:
        reason = 'no reason provided!'
    await ctx.guild.kick(member)
    await ctx.send(f'{member.mention} has been scared away by Asami {reason}')

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *,reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} just got swatted {reason}!')

@bot.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")
    for ban_entry in banned_users:
        user = ban_entry.user
        if(user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

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
async def smooch(ctx):
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

@bot.command()
async def weather(ctx, message):
    location = message
    if len(location) >= 1:
        url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&units=imperial&appid={api_key}'
        try:
            data = json.loads(requests.get(url).content)
            data = data_parse(data)
            await ctx.send(embed=weather_message(data, location))
        except KeyError:
            await ctx.send(embed=invalid_location(location))

@bot.group(invoke_without_command=True)
async def help(ctx):
    print (f'{ctx.author.mention} has used help')
    embed = discord.Embed(title="Help", description="Use a!help <command> to see more information.",color=ctx.author.color)
    embed.add_field(name="Moderation",value="kick, ban, unban", inline=False)
    embed.add_field(name="Miscellaneous",value="bite, hello, feed, meow, pat, swat, smooch", inline=False)
    embed.add_field(name="New Feature(s)",value="weather")
    embed.add_field(name="Features",value="Weather Teller (Asami can sense the weather!)\nTimer (Coming soon!)\n(Coming soon!)", inline=False)
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
async def kick(ctx):
    embed = discord.Embed(title="Kick",description="Asami kicks a member from the server",color=ctx.author.color)
    embed.add_field(name="Syntax",value="a!kick <member> [reason]")
    await ctx.send(embed=embed)

@help.command()
async def ban(ctx):
    embed = discord.Embed(title="Ban",description="Asami bans a member from the server",color=ctx.author.color)
    embed.add_field(name="Syntax",value="a!ban <member> [reason]")
    await ctx.send(embed=embed)

@help.command()
async def unban(ctx):
    embed = discord.Embed(title="Unban",description="Asami unbans a member from the server",color=ctx.author.color)
    embed.add_field(name="Syntax",value="a!unban <member>")
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
async def smooch(ctx):
    embed = discord.Embed(title="Smooch",description="Give Asami a fat smooch but be careful",color=ctx.author.color)
    embed.add_field(name="Syntax",value="a!smooch")
    await ctx.send(embed=embed)

@help.command()
async def weather(ctx):
    embed = discord.Embed(title="Weather",description="Asami can sense the current weather of a city",color=ctx.author.color)
    embed.add_field(name="Syntax",value="a!weather <city name>")
    await ctx.send(embed=embed)

bot.run(token)
