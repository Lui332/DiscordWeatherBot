import discord
import requests
import json
from weather import *
from keep_alive import keep_alive

token = 'ODc1MDQ2NDE4MTQwNzg2NzY5.YRP0ew.ra88iobQKes0cgzFyxJlpgyQNVw'
api_key = '44494cd29593cb0ee92c2d22ec08c32a'
current_prefix = 'c.'
daily_prefix = 'd.'
client = discord.Client()

# on_ready() function
#
# Input Parameters:  None
# Output Parameters: None
# Description:       Sets the activity of the discord bot to help user 
@client.event
async def on_ready():
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f'{current_prefix}[location]'))

# on_message(message) function
#
# Input Parameter:  message (user message)
# Output Parameter: None
# Description:      If the message was given by a user with a proper command prefix, the function performs
#                       appropriate actions and function calls to display a embeded message to the channel
@client.event
async def on_message(message):

  # Command prefix = c.
  # If a message was sent in the channel from a user other than the bot, and the message starts with 'c.'
  if message.author != client.user and message.content.startswith(current_prefix):
    location = message.content.replace(current_prefix, '').lower()

    # if the user did not enter anything after command prefix
    if len(location) >= 1:
      url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=imperial'
      try:

        # gather and format data, then display embeded message
        data = json.loads(requests.get(url).content)
        weather_type = data['weather'][0]['description']
        data = current_parse_data(data)
        await message.channel.send(embed=current_weather_message(data, weather_type, location))
      
      except KeyError:
        await message.channel.send(embed=error_message(location))
  
  # Command prefix = d.
  # If a message was sent in the channel from a user other than the bot, and the message starts with 'd.'
  elif message.author != client.user and message.content.startswith(daily_prefix):
    location = message.content.replace(daily_prefix, '').lower()

    #if the user did not enter anything after command prefix
    if len(location) >= 1:
      url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=imperial'
      try:

        # get the coordinates given from the first url
        coordinates = json.loads(requests.get(url).content)
        coordinates = get_cordinates(coordinates)
        latitude = coordinates['lat']
        longitude = coordinates['lon']

        # get the 8 day forecast based in the coordinates from other url, format data, and display embeded message
        url = f'https://api.openweathermap.org/data/2.5/onecall?lat={latitude}&lon={longitude}&exclude=current,minutely,hourly,alerts&appid={api_key}&units=imperial'
        data = json.loads(requests.get(url).content)
        daily_data = daily_parse_data(data)
        await message.channel.send(embed=daily_weather_message(daily_data, location))
      
      except KeyError:
        await message.channel.send(embed=error_message(location))

keep_alive()        # keeps the bot running continuously
client.run(token)   # run the bot
