"""
NoFuture.py: A future-less Discord bot (Python version)
-------------------------------------------------------------------------------
Look, I'll give it to you straight: This is a general-purpose,
do-whatever-you-want kind of bot, it has no specific goal and is mostly there
so I can practice programming and not get bored out of my mind with
infrastructure at work.

This bot's name, possibly its avatar picture too (in the original instance that
I maintain, that is) and a lot of other things make references towards Free
from Soul Eater (credits to Ōkubo-sensei for that awesome manga). If you
haven't given the show a read or a watch, you likely won't understand much.

The idea for the bot's name is that a bot with no purpose has no future.
Simple as that.

And yes, the text above is the original one that I moved to README.md.
-------------------------------------------------------------------------------
This file in particular has the core stuff and the bot's setup/main event loop.
Cogs in particular go into their respective categories under ./cogs/category.
"""

# Import essentials/builtins
# import asyncio

# from discord.errors import ConnectionClosed, GatewayNotFound, HTTPException, LoginFailure
from discord.ext import commands
from discord.flags import Intents
from sqlalchemy.orm import close_all_sessions
from core.utils import nf_configs, yn

# SQL stuffs
from core.dao import engin
from core.model import initialize_sql, DBSession
from core.model.server import Server

# Import cogs
from cogs.games import Games
from cogs.roger.roger import Roger
from cogs.youtube import NFYouTube
from cogs.ggl_img import NFGoogleImg

# Bot configuration
bot = commands.Bot(
    command_prefix=["nf ", '\\'],
    owner_id=nf_configs['owner_id'],
    intents=Intents(messages=True, guilds=True, members=True, presences=True)
)

initialize_sql(engin)

# Cogs
bot.add_cog(Games(bot, 1))
bot.add_cog(Roger(bot, 2))
bot.add_cog(NFYouTube(bot, 4))
bot.add_cog(NFGoogleImg(bot, 8))


# Bot events
@bot.event
async def on_command_error(ctx, error):
    # this one is just so the logs don't get polluted with
    # "ignoring unknown command" errors
    if isinstance(error, commands.CommandNotFound):
        return
    else:
        raise error


@bot.event
async def on_ready():
    print("NoFuture bot running now. I want to watch some quality comedy...\nPress CTRL+C to terminate.")


# Core commands, mostly debugging stuff
@bot.command('hi')
async def nf_greet(ctx: commands.Context):
    if ctx.author.display_name != ctx.author.name:
        suffix = f"{ctx.author.display_name} (AKA {ctx.author.name})"
    else:
        suffix = ctx.author.name
    await ctx.send(f"Hey there, {suffix}.")


@bot.command('say')
async def nf_say(ctx: commands.Context, *, message):
    if not await bot.is_owner(ctx.author):
        await ctx.send("<:zipper_mouth:808163806051041321>")
    else:
        await ctx.message.delete()
        await ctx.send(message)


@bot.command('die')
async def nf_shutdown(ctx: commands.Context):
    if not await bot.is_owner(ctx.author):
        await ctx.send("I can't die. I am, after all, immortal.")
    else:
        await ctx.send("Fine, fine. I will die for a while, but I'll be back anyway. I am, after all, immortal.")
        await bot.logout()

# After 200 years...
# TODO Improve main event loop down below
# def main():
#     restart = True
#     while restart:
#         if not nf_configs['discord_token']:
#             nf_configs['discord_token'] = input("I couldn't find a token to login with. Type one down below and let's try this again.\n>> ")
#             print("Good. Let's try this. In the future, if you want to skip this prompt, consider looking at ./example_config.yml.")
#         try:
#             bot.run(nf_configs['discord_token'])

#         except GatewayNotFound as e:
#             print(f"Gateway wasn't found, likely a Discord API error.\n{e}")
#         except ConnectionClosed as e:
#             print(f"Connection closed by Discord.\n{e}")
#         except LoginFailure as e:
#             print(f"You gave me the wrong credentials, so Discord didn't let me log in.\n{e}")
#         except HTTPException as e:
#             print(f"Some weird HTTP error happened. More details below.\n{e}")
#         except Exception as e:
#             print(f"Something else went wrong and I'm not sure what. More details below.\n{e}")
#         finally:
#             print("Do you want to restart? Type yes or no below. ('no' will shut me down, obviously.)")
#             restart = yn()

# if __name__ == '__main__':
#     try:
#         main()
#     except Exception as e:
#         print(f"Something went wrong with the main loop. Terminating.\n{e}")

bot.run(nf_configs['discord_token'])
DBSession.commit()
close_all_sessions()  # for SQLAlchemy
print("THAT'S IT! REHABILITATION! FIRST COMES REHABILITATION!")
