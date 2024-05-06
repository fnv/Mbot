# misc.py
import re

import discord
import pytz
from discord import HTTPException
from discord.ext import commands
import random
import os
import asyncio
import urllib.request
import datetime
import string

# A cog for nonessential commands and triggers


# temporary april fools joke: 
# https://gist.github.com/AXVin/2e7dc608b552d05d2b04cecaaa4457bc
flipped_lower_chars = "ɐqɔpǝɟƃɥıɾʞןɯuodbɹsʇnʌʍxʎz"
flipped_lower_chars = "ɐqɔpǝɟƃɥıɾʞlɯuodbɹsʇnʌʍxʎz"
flipped_upper_chars = "∀𐐒Ɔ◖ƎℲ⅁HIſ⋊˥WNOԀΌᴚS⊥∩ΛMX⅄Z"
mapping = {char: flipped_lower_chars[i] for i, char in enumerate(string.ascii_lowercase) }
mapping.update({char: flipped_upper_chars[i] for i, char in enumerate(string.ascii_uppercase) })
mapping.update({
"-": "-",
"_": "‾",
" ": " "
})
flipped_mapping = {v:k for k,v in mapping.items()}




class MiscCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def flipchannels(self, ctx):
        idxall = [555663169612283906,556694164234960938,797939344056778824,797576926197841940,833541557746925578,667749988222107653,870111032138412063]
        # print('start')
        for idx in idxall:
            channel = self.bot.get_channel(idx)
            # print(channel)
            emoji = channel.name[0:2]
            name = channel.name[2:]
            revname = "".join(mapping[char] for char in name[::-1])
            newname = emoji+revname
            # print(newname)
            await channel.edit(name=newname)

    @commands.command()
    @commands.is_owner()
    async def unflipchannels(self, ctx):
        idxall = [555663169612283906,556694164234960938,797939344056778824,797576926197841940,833541557746925578,667749988222107653,870111032138412063]
        for idx in idxall:
            channel = self.bot.get_channel(idx)
            # print(channel)
            emoji = channel.name[0:2]
            name = channel.name[2:]
            revname = "".join(flipped_mapping[char] for char in name[::-1])
            newname = emoji+revname
            # print(newname)
            await channel.edit(name=newname)


    @commands.command()
    async def flip(self, ctx):
        if random.uniform(0,1) <= 0.2:
            await ctx.send('Coin landed on the edge\n*wait what??*')
        else:
            flip = random.choice(['heads', 'tails'])
            await ctx.send(flip)

    @commands.command(aliases=['dice'])
    async def roll(self, ctx, number_of_dice: int, number_of_sides: int):
        if number_of_dice > 10:
            await ctx.send('Why do you need so many dice rolls...')
        elif number_of_dice == 0:
            await ctx.send('This is how I know you do not need me. Doomslug was ever the better companion.')
        elif number_of_dice < 0 and number_of_dice >= -20000:
            await ctx.send('*Mbot gives an exasperated sigh*')
        elif number_of_dice <-20000:
            await ctx.send('Do you think I was Made in Abyss? You do know that those who go there, rarely come back...')
        if number_of_sides > 20:
            await ctx.send('What kind of dice do you have??? My friend, those are called marbles. Did you lose them?')
        elif number_of_sides < 4 and number_of_sides > 0:
            await ctx.send('Do you live in Flatland?')
        elif number_of_sides == 2:
            await ctx.send('You could just flip a coin.')
        elif number_of_sides == 0:
            await ctx.send('I am not sure you actually need my help. Maybe I can fly you to the nearest therapist...')
        elif number_of_sides < 0 and number_of_sides >= -9:
            await ctx.send('What are we in, inverse space? I wonder, would that be the place with all the watching eyes...')
        elif number_of_sides < -10 and number_of_sides >= -25:
            await ctx.send('Heh, going deeper I see.')
        elif number_of_sides < -25 and number_of_sides >= -33:
            await ctx.send('I recommend stopping that now.')
        elif number_of_sides < -33 and number_of_sides >= -55:
            await ctx.send('<:szeth:667773296896507919>')
        elif number_of_sides < -55 and number_of_sides >= -74:
            await ctx.send('Why are you even testing this? Are you a quality analyst? (Please don\'t be too harsh on my code when you (maybe eventually) see it: https://xkcd.com/1513/ )')
        elif number_of_sides < -74 and number_of_sides >= -103:
            await ctx.send('You broke me. Happy now?')
        elif number_of_sides < -103:
            await ctx.send('Okay, I refuse to go farther... The eyes are watching.')
        if number_of_dice <= 10 and number_of_dice > 0 and number_of_sides <= 20 and number_of_sides >= 4:
            dice = [
                str(random.choice(range(1, number_of_sides + 1)))
                for _ in range(number_of_dice)
            ]
            await ctx.send(', '.join(dice))

    @commands.command(aliases=['sz'])
    async def szeth(self,ctx):
        filepath = './misc/emotes/szeth.png'
        await ctx.send(file=discord.File(filepath))
        #await ctx.send('<:szeth:667773296896507919>')

    def is_it_hunt_string(self):
        huntdate = datetime.datetime(2024,1,12,17,0,0,0) # start time in utc
        now = datetime.datetime.utcnow()
        delta = huntdate - now
        days = delta.days
        hours = delta.seconds // 3600
        minutes = (delta.seconds % 3600) // 60
        seconds = (delta.seconds % 3600) % 60
        if days < 0:
            return '**YES!!!** :tada: Mystery Hunt 2024 has started!'
        else:
            return '**NO.** \nHunt is in {} days, {} hours, {} minutes, {} seconds.'.format(days,hours,minutes,seconds)

    @commands.command(aliases=['iihy', 'iihy?', 'isithuntyet?'])
    async def isithuntyet(self,ctx):
        await ctx.send(self.is_it_hunt_string())

    @commands.command(aliases=['emoji'])
    async def emote(self,ctx,query):

        if query == 'list':
            all_emotes = os.listdir('./misc/emotes/')
            final = '`!emote namehere`\n'
            for item in all_emotes:
                final = final + item[:-4] + '\n'
            await ctx.send(final)
            return

        await ctx.message.delete()

        filepath = './misc/emotes/'+query+'.png'
        await ctx.send(file=discord.File(filepath))

    @commands.command(aliases=['time', 'timezone'])
    async def time_in(self, ctx, *, query=None):
        if not query:
            await ctx.send('Usage: `!time [region]`')
            return

        query = query.upper().replace(' ', '_')
        fmt = '**%I:%M %p** on **%d %b %Y**'
        valid_zones = []
        for timezone_str in pytz.common_timezones_set:
            if query == timezone_str.upper():
                valid_zones = [timezone_str]
                break
            elif query in timezone_str.upper():
                valid_zones.append(timezone_str)
        if len(valid_zones) == 1:
            await ctx.send('The current time in **' + valid_zones[0] + '** is ' +
                           datetime.datetime.now(tz=pytz.timezone(valid_zones[0])).strftime(fmt))
        elif len(valid_zones) > 1:
            try:
                await ctx.send('Requested timezone is ambiguous. Possible options are:\n\n' + '\n'.join(valid_zones))
            except HTTPException:
                await ctx.send('Requested timezone is ambiguous. Your request matches too many options to list.')
        else:
            await ctx.send('I don\'t recognize that timezone.')


async def setup(bot):
    await bot.add_cog(MiscCog(bot))
