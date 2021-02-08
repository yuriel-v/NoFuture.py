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
from discord.ext import commands
from discord.flags import Intents
from sqlalchemy.orm import close_all_sessions
from core.utils import nf_configs

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

# Cogs
bot.add_cog(Games(bot))
bot.add_cog(Roger(bot))
bot.add_cog(NFYouTube(bot))
bot.add_cog(NFGoogleImg(bot))

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
bot.run(nf_configs['discord_token'])
#close_all_sessions()  # for SQLAlchemy
print("THAT'S IT! REHABILITATION! FIRST COMES REHABILITATION!")
