import discord
import random
import datetime
from discord.ext import commands, tasks


intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True
intents.presences = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

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

def get_country():
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
    
continent = get_country()


@tasks.loop(seconds=60)
async def main():
    now = datetime.datetime.now()
    if now.hour == 6 and now.minute == 0:
        countries = random.sample(allcountries[continent], 3)
        countries.sort()

        for guild in bot.guilds:
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
    for guild in bot.guilds:
        print(guild.name, guild.id)
    print('bot is online!')
    main.start()


bot.run('MTM3NTY1NDYwMzAyMjAwODUwMQ.Gun621.NcW6JIAStzV_OEU2aA88tagRx1mNboEOy_oM_c')