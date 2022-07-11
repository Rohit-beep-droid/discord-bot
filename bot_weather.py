import discord

# the desired attributes to be displayed
attributes = {
    'temp': 'Temperature',
    'feels_like': 'Feels Like',
    'temp_min': 'Low',
    'temp_max': 'High'
}

# parsing the attributes
def attributes_parse(data):
    data = data['main']
    del data['pressure']
    del data['humidity']
    return data

# description of the weather
visibility = {
    'main': 'Visibility',
    'description': 'Description'
}

# parsing information collected from description
def visibility_parse(data):
    weather = []
    data = data['weather']
    for i in data:
        weather.append(i)
    data = weather[0]
    del data['id']
    del data['icon']
    return data

# function responsible for displaying weather information
def weather_msg(data, description, location):
    location = location.title()
    embed = discord.Embed(
        title=f'{location} Weather',description=f'Weather for {location}', color=0x0065FF
    )
    for i in description:
        embed.add_field(name= visibility[i], value=str(description[i]).capitalize(), inline=False)
    for key in data:
        embed.add_field(name=attributes[key], value=str(data[key]), inline=False)
    return embed

# error handling
def invalid_msg(location):
    location = location.title()
    return discord.Embed(
        title='Error',description=f'Could not retrieve data for {location}', color=0x0065FF
    )
