# Roger memes, yoinked off Daedalus.
# Will only work on our own server or the hub guild (for debug purposes).
#
# I also have no plans whatsoever to translate the stuff below.

import requests

from core.utils import split_args
from discord import Message
from discord.ext import commands
from discord.embeds import Embed
from discord.colour import Colour
from random import randint
from core.utils import nf_configs, yaml


def ferozes():
    def predicate(ctx):
        return ctx.guild.id in (567817989806882818, nf_configs['hub_guild'])
    return commands.check(predicate)


class Roger(commands.Cog, name='Roger'):
    def __init__(self, bot):
        self.bot = bot
        with open('./src/cogs/roger/responses.yml', mode='r', encoding='utf-8') as file:
            self.roger_responses = yaml.load(file)['eight_ball']
    
    @commands.group(name='roger')
    @ferozes()
    async def roger(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            arguments = split_args(ctx.message.content)
            if not arguments:
                await ctx.send("O que é, desgraça?")
            else:
                await ctx.send(
                    "Cahf ah nafl mglw'nafh hh' ahor syha'h ah'legeth, ng llll or'azath syha'hnahh n'ghftephai n'gha ahornah ah'mglw'nafh"
                )

    @roger.command(name='?')
    async def roger_foto(self, ctx: commands.Context):
        """Você perguntou? O Roger aparece!"""
        msg: Message = await ctx.send("Invocando o Roger...")
        try:
            roger_img = self._fetch_roger_image()
            embed = Embed(description=roger_img[0], colour=Colour(randint(0x000000, 0xFFFFFF)))
            embed.set_image(url=roger_img[1])

            if roger_img[0].lower() == "julio_cobra":
                ct = 'Cacilda, agora a cobra fumou. Você tirou o julio_cobra.'
            else:
                ct = None
            await msg.edit(content=ct, embed=embed)

        except Exception as e:
            await msg.edit("Ih, deu zica.")
            print(f"Zica thrown: {e}")

    @roger.command(name='responde:')
    async def roger_responde(self, ctx: commands.Context):
        """
        Roger responde: Eu sou bom programador?

        Roger diz: SE LASCAR
        """
        if len(split_args(ctx.message.content)) >= 2:
            await ctx.send(f"<@450731404532383765> diz: {self.roger_responses[randint(1, len(self.roger_responses.keys()))]}")
        else:
            await ctx.send(f"<@450731404532383765> diz: Se lascar, pergunta alguma coisa!")

    def _fetch_roger_image(self):
        endpoint = "https://api.imgur.com/3/album/xv4Jn5D/images"
        response = requests.get(url=endpoint, headers={'Authorization': f"Client-ID {nf_configs['api_tokens']['imgur']}"}).json()['data']
        image = response[randint(0, len(response) - 1)]

        return (image['description'], image['link'])
