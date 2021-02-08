import requests
from core.utils import nf_configs
from discord.colour import Colour
from discord.embeds import Embed
from discord.ext import commands
from random import randint
from urllib.parse import urlencode


class NFGoogleImg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command('img')
    async def google_image_search(self, ctx: commands.Context, *, terms=None):
        """Sends an embed containing the first image found in Google for the specified terms."""
        if not terms:
            await ctx.send("Well I can't go searching for nothing now, can I? Give me something to search for.")
            return

        result = requests.get(url=self._build_searchstr(terms)).json()['items']
        if not result:
            await ctx.send("Tough luck, no results found.")
            return
        else:
            embed = Embed(description="Image first result:", colour=Colour(randint(0x000000, 0xFFFFFF)))
            embed.set_image(url=result[0]['link'])
            await ctx.send(embed=embed)
    
    @commands.command('img-list')
    async def list_google_image_search(self, ctx: commands.Context, *, terms=None):
        """Sends an embed containing links to the first 5 Google Image Search matches for the specified terms."""
        if not terms:
            await ctx.send("Well I can't go searching for nothing now, can I? Give me something to search for.")
            return
        
        results = requests.get(url=self._build_searchstr(terms, 5)).json()['items']
        if not results:
            await ctx.send("Tough luck, no results found.")
            return
        else:
            desc = [f"{i + 1}. [{results[i]['title']}]({results[i]['link']})" for i in range(0, len(results))]
            embed = Embed(description='\n'.join(desc), colour=Colour(randint(0x000000, 0xFFFFFF)))
            await ctx.send(embed=embed)

    def _build_searchstr(self, terms: str, num: int = 1):
        """Builds a query string for a Google Image search, with ther number and terms specified."""
        query = {
            'cx': nf_configs['api_tokens']['ggl_images_cx'],
            'key': nf_configs['api_tokens']['ggl_images_api'],
            'num': num,
            'searchType': 'image',
            'q': terms
        }
        return "https://customsearch.googleapis.com/customsearch/v1?" + urlencode(query)
