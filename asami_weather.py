import discord

color = 0xFF6500

features = {
    'temp': 'Temperature',
    'feels_like': 'Feels Like',
    'temp_min': 'Minimum Temperature',
    'temp_max': 'Maximum Temperature'
}

def data_parse(data):
    data = data['main']
    del data['humidity']
    del data['pressure']
    return data

def weather_message(data, location):
    location = location.title()
    embed = discord.Embed(
        title=f'{location} Weather',description=f'Weather for {location}', color = color
    )
    for key in data:
        embed.add_field(name=features[key], value=str(data[key]), inline=False)
    return embed

def invalid_location(location):
    location = location.title()
    return discord.Embed(
        title='Error',description=f'Could not retrieve data for {location}',color= color
    )
