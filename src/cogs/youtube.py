from discord.colour import Colour
from discord.embeds import Embed
from discord.ext import commands
from youtube_search import YoutubeSearch


class NFYouTube(commands.Cog):
    def __init__(self, bot, id):
        self.bot = bot
        self.cog_id = id

    @commands.command('yt')
    async def yt_search(self, ctx: commands.Context, *, terms=None):
        """Searches for a YouTube video and links its first match."""
        if not terms:
            await ctx.send("Well I can't go searching for nothing now, can I? Give me something to search for.")
            return

        results = YoutubeSearch(terms, max_results=1).to_dict()
        if not results:
            await ctx.send("Tough luck, no results found.")
            return
        await ctx.send(f"https://youtu.be/{results[0]['id']}")

    @commands.command('yt-list')
    async def yt_list_search(self, ctx: commands.Context, *, terms=None):
        """Sends a search string to YouTube and prints a list with links to the first 5 matches."""
        if not terms:
            await ctx.send("Well I can't go searching for nothing now, can I? Give me something to search for.")
            return

        results = YoutubeSearch(terms, max_results=5).to_dict()
        if not results:
            await ctx.send("Tough luck, no results found.")
            return

        res = [f"{i + 1}. [{results[i]['title']}](https://youtu.be/{results[i]['id']})" for i in range(0, len(results))]
        embed = Embed(description='\n'.join(res), colour=Colour(0xFF0000))
        await ctx.send(embed=embed)
