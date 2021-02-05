"""
NoFuture.py: A future-less Discord bot (Python version)
-------------------------------------------------------------------------------
Look, I'll give it to you straight: This is a general-purpose,
do-whatever-you-want kind of bot, it has no specific goal and is mostly there
so I can practive programming and not get bored out of my mind with
infrastructure at work.

This bot's name, possibly its avatar picture too (in the original instance that
I maintain, that is) and a lot of other things make references towards Free
from Soul Eater (credits to Ōkubo-sensei for that awesome manga). If you
haven't given the show a read or a watch, you likely won't understand much.

The idea for the bot's name is that a bot with no purpose has no future.
Simple as that.
-------------------------------------------------------------------------------
This file in particular has the core stuff and the bot's setup/main event loop.
Cogs in particular go into their respective categories under ./cogs/category.
"""

# Import essentials/builtins
from discord.ext import commands
from discord.ext.commands.core import is_owner
from discord.flags import Intents
from os import getenv
from sqlalchemy.orm import close_all_sessions

# Import cogs
# ...

# Bot configuration
nf_token = getenv("NF_TOKEN")
bot = commands.Bot(
    command_prefix="nf ",
    owner_id=int(getenv("NF_OWNERID")),
    intents=Intents(messages=True, guilds=True, members=True, presences=True)
)

# Cogs
# ...

# Bot events

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    else:
        raise error

@bot.event
async def on_ready():
    print("NoFuture bot running now. I want to watch some quality comedy.")


# Core commands, mostly debugging stuff

@bot.command('hi')
async def nf_greet(ctx: commands.Context):
    if ctx.author.display_name != ctx.author.name:
        suffix = f"{ctx.author.display_name} (AKA {ctx.author.name})"
    else:
        suffix = ctx.author.name
    await ctx.send(f"Hey there, {suffix}.")

@bot.command('die')
async def nf_shutdown(ctx: commands.Context):
    if not await bot.is_owner(ctx.author):
        await ctx.send("I can't die. I am, after all, immortal.")
    else:
        await ctx.send("Fine, fine. I will die for a while, but I'll be back anyway. I am, after all, immortal.")
        await bot.logout()

# After 200 years...
bot.run(nf_token)
#close_all_sessions()  # for SQLAlchemy
print("THAT'S IT! REHABILITATION! FIRST COMES REHABILITATION!")
