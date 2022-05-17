import discord
from datetime import datetime

color = 0x04ceff  #color of the embeded message
days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
current_key_features = {
  'temp' : 'Temperature',
  'feels_like' : 'Feels Like',
  'temp_min' : 'Minimum Temperature',
  'temp_max' : 'Maximum Temperature'
}

# current_parse_data() function
#
# Input Parameters:  data
# Output Parameters: data
# Description:       Based on the data given, it removes all the unwanted information
#                       and leaves only the data for the current weather
def current_parse_data(data):
  data = data['main']
  del data['humidity']
  del data['pressure']
  return data

# daily_parse_data() function
#
# Input Parameters:  data
# Output Parameters: daily_data
# Description:       Based on the data given, it gather only the information for the 8-day
#                       forecast
def daily_parse_data(data):
  daily_data = []
  for dic in data['daily']:
    daily_data.append(dic['weather'][0]['description'])
    daily_data.append(round(dic['temp']['max']))
    daily_data.append(round(dic['temp']['min']))
  return daily_data

# get_coordinates() function
#
# Input Parameters:  data
# Output Parameters: data
# Description:       Based on the data given, it returns only the coordinates from the data
def get_cordinates(data):
  data = data['coord']
  return data

# current_weather_message() function
#
# Input Parameters:  data, weather_type, location
# Output Parameters: message
# Description:       An embedded message is created with the given data to display the current
#                       weather in a organized fashion.
def current_weather_message(data, weather_type, location):
  location = location.title()
  message = discord.Embed(
    title = f'{location} Weather',
    description = f'Here is the weather in {location}.',
    color = color)
  
  message.add_field(name='Description', value=weather_type.upper(), inline=False)
  
  for key in data:
    message.add_field(name=current_key_features[key],value=f'{str(round(data[key]))} °F', inline=False)
  
  return message

# daily_weather_message() function
#
# Input Parameters:  data, weather_type, location
# Output Parameters: message
# Description:       An embedded message is created with the given data to display the 8-day 
#                       weather in a organized fashion.
def daily_weather_message(daily_data, location):
  location = location.title()
  message = discord.Embed(
    title = f'{location} Weather',
    description = f'Here is the 8 day forecast for {location}.',
    color = color)
  
  stat_index = 0
  day_of_week = datetime.today().weekday()
  for i in range(8):
    message.add_field(name=f'{days[day_of_week]}',
      value=f'{daily_data[stat_index].upper()}\nMax : {daily_data[stat_index+1]} °F\nMin : {daily_data[stat_index+2]} °F\n\u200B------------------------------------',
      inline=False)
    
    stat_index += 3
    day_of_week += 1

    if day_of_week > 6:
      day_of_week = 0
  
  return message

# error_message() function
#
# Input Parameters:  location
# Output Parameters: None
# Description:       An embedded error message is created
def error_message(location):
  location = location.title()
  return discord.Embed(title='Error',description=f'There was an error retrieving weather data for {location}.', color = color)
