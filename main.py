import discord
import random
import datetime
import os
import json
from dotenv import load_dotenv
from discord.ext import commands, tasks


intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True
intents.presences = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

config_file = "data.json"

allcountries = {
    "Africa": [
        "South Africa", "Angola", "Algeria", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cape Verde",
        "Cameroon", "Chad", "Comoros", "Congo", "Ivory Coast", "Djibouti", "Egypt", "Eritrea", "Eswatini",
        "Ethiopia", "Gabon", "Gambia", "Ghana", "Guinea", "Guinea-Bissau", "Equatorial Guinea", "Lesotho",
        "Liberia", "Libya", "Madagascar", "Malawi", "Mali", "Morocco", "Mauritius", "Mauritania", "Mozambique",
        "Namibia", "Niger", "Nigeria", "Kenya", "Central African Republic", "Democratic Republic of the Congo",
        "Rwanda", "São Tomé and Príncipe", "Senegal", "Sierra Leone", "Seychelles", "Somalia", "Sudan",
        "South Sudan", "Tanzania", "Togo", "Tunisia", "Uganda", "Zambia", "Zimbabwe"
    ],
    "Asia": [
        "Afghanistan", "Saudi Arabia", "Armenia", "Azerbaijan", "Bahrain", "Bangladesh", "Bhutan", "Brunei",
        "Cambodia", "Qatar", "Kazakhstan", "China", "Cyprus", "North Korea", "South Korea", "United Arab Emirates",
        "Philippines", "Georgia", "India", "Indonesia", "Iran", "Iraq", "Israel", "Japan", "Jordan", "Kuwait",
        "Laos", "Lebanon", "Malaysia", "Maldives", "Mongolia", "Myanmar", "Nepal", "Oman", "Pakistan", "Palestine",
        "Kyrgyzstan", "Russia", "Singapore", "Syria", "Sri Lanka", "Tajikistan", "Thailand", "East Timor",
        "Turkmenistan", "Turkey", "Uzbekistan", "Vietnam", "Yemen"
    ],
    "Europe": [
        "Albania", "Germany", "Andorra", "Armenia", "Austria", "Azerbaijan", "Belgium", "Belarus",
        "Bosnia and Herzegovina", "Bulgaria", "Cyprus", "Croatia", "Denmark", "Slovakia", "Slovenia", "Spain",
        "Estonia", "Finland", "France", "Georgia", "Greece", "Hungary", "Ireland", "Iceland", "Italy", "Kazakhstan",
        "Kosovo", "Latvia", "Liechtenstein", "Lithuania", "Luxembourg", "North Macedonia", "Malta", "Moldova",
        "Monaco", "Montenegro", "Norway", "Netherlands", "Poland", "Portugal", "United Kingdom", "Czech Republic",
        "Romania", "Russia", "San Marino", "Serbia", "Sweden", "Switzerland", "Turkey", "Ukraine", "Vatican City"
    ],
    "South America": [
        "Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Ecuador", "Guyana", "Paraguay",
        "Peru", "Suriname", "Uruguay", "Venezuela"
    ],
    "North America": [
        "Antigua and Barbuda", "Bahamas", "Barbados", "Belize", "Canada", "Costa Rica", "Cuba",
        "Dominica", "El Salvador", "United States", "Grenada", "Guatemala", "Haiti", "Honduras",
        "Jamaica", "Mexico", "Nicaragua", "Panama", "Dominican Republic", "Saint Kitts and Nevis",
        "Saint Lucia", "Saint Vincent and the Grenadines", "Trinidad and Tobago"
    ],
    "Oceania": [
        "Australia", "Fiji", "Marshall Islands", "Solomon Islands", "Kiribati", "Micronesia", "Nauru", "New Zealand",
        "Palau", "Papua New Guinea", "Samoa", "Tonga", "Tuvalu", "Vanuatu"
    ],
    "Antarctica": [
        "Australian Antarctic Territory", "British Antarctic Territory", "Chilean Antarctic Territory",
        "French Southern and Antarctic Lands", "New Zealand Antarctic Territory", "Norwegian Antarctic Territory",
        "Argentine Antarctic Territory"
    ]
}

def get_cont():
    day = datetime.datetime.today().weekday()
    if day == 0:
        return "Africa"
    if day == 1:
        return "Asia"
    if day == 2:
        return "Europe"
    if day == 3:
        return "South America"
    if day == 4:
        return "North America"
    if day == 5:
        return "Oceania"
    if day == 6:
        return "Antarctica"
    
continent = get_cont()

def load_config():
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            return json.load(f)
    else:
        return {}

def save_config(config):
    with open(config_file, "w") as f:
        json.dump(config, f, indent=4)


@tasks.loop(seconds=60)
async def main():
    now = datetime.datetime.now()
    config = load_config()

    for guild in bot.guilds:
        guild_id = str(guild.id)

        if guild_id in config:
            hour = config[guild_id]["hour"]
            minute = config[guild_id]["minute"]

            if now.hour == hour and now.minute == minute:
                countries = random.sample(allcountries[continent], 3)
                countries.sort()

                for ctg in guild.categories:
                    if ctg.name == 'Countries':
                        for vc in guild.voice_channels:
                            if vc.category == ctg:
                                await vc.delete()
                        await ctg.delete()

                category = await guild.create_category('Countries')
                for c in countries:
                    await guild.create_voice_channel(name= c, category=category, bitrate=64000)

                if guild.system_channel:
                    await guild.system_channel.send('3 random channels were created today')

@bot.event
async def on_ready():
    config = load_config()

    for guild in bot.guilds:
        guild_id = str(guild.id)
        if guild_id not in config:
            config[guild_id] = {
                "hour": 6,
                "minute": 0
            }

    save_config(config)
    print('bot is online!')
    print('settings updated with server')
    print(config)

    main.start()

@bot.command()
@commands.has_permissions(administrator=True)
async def settime(ctx, hour:int, minute: int):
    if not (0 <= hour <= 23) or not (0 <= minute <= 59):
        await ctx.send(f'Please set the time right! Hour must be between 0-23 and minute 0-59')
        return
    config = load_config()
    guild_id = str(ctx.guild.id)

    if guild_id not in config:
        config[guild_id] = {}

    config[guild_id]["hour"] = hour
    config[guild_id]["minute"] = minute

    save_config(config)

    await ctx.send(f'⏰ Your server reset time was updated to {hour:02d}:{minute:02d} in this server!')
        

@bot.command()
async def showtime(ctx):
    config = load_config()
    guild_id = str(ctx.guild.id)

    if guild_id in config:
        hour = config[guild_id]["hour"]
        minute = config[guild_id]["minute"]

        await ctx.send(f"The time set in this server is {hour:02d}:{minute:02d}!")
    
    else:
        await ctx.send("Your doesn't have a time set yet!")


load_dotenv()

token=os.getenv("DCTOKEN")
bot.run(token)