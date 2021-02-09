import requests

from discord.colour import Colour
from discord.embeds import Embed
from discord.ext import commands
from random import randint


class Games(commands.Cog):
    def __init__(self, bot, id):
        self.cog_id = id
        self.bot = bot

    @commands.command('rps')
    async def rock_paper_scissors(ctx: commands.Context, *, choice: str = None):
        """It's rock-paper-scissors. Rock beats paper, paper beats scissors, scissors beats rock."""
        rps = {'r': 'rock', 'p': 'paper', 's': 'scissors'}

        async def send_msg():
            string = f"I pick {rps[tuple(rps.keys())[bot_choice]]}! "
            if outcome == 0:
                string += "I win!"
            elif outcome == 1:
                string += "Oh, we draw."
            else:
                string += "Damn, I lost..."
            await ctx.send(string)

        if not choice:
            await ctx.send("Well, we can't play rock-paper-scissors if you don't pick anything.")
        elif choice.lower() not in rps.keys() and choice.lower() not in rps.values():
            await ctx.send("Then I pick ice and freeze your ass outta here! <:ice_cube:808205401710657546>")
        else:
            choice = tuple(rps.keys()).index(choice[0].lower())
            bot_choice = randint(0, 2)

            # choices:
            # 0 = rock
            # 1 = paper
            # 2 = scissors
            if choice == 0:
                if bot_choice == 0:
                    outcome = 1
                elif bot_choice == 1:
                    outcome = 0
                else:
                    outcome = 2
            elif choice == 1:
                if bot_choice == 0:
                    outcome = 2
                elif bot_choice == 1:
                    outcome = 1
                else:
                    outcome = 0
            else:
                if bot_choice == 0:
                    outcome = 0
                elif bot_choice == 1:
                    outcome = 2
                else:
                    outcome = 1

            await send_msg()

    @commands.command(name='8ball')
    async def eight_ball(self, ctx: commands.Context):
        """Queries the omniscient 8-Ball for an answer."""
        eightball_replies = {
            1: "As I see it, yes.",
            2: "Ask again later.",
            3: "Better not tell you now.",
            4: "Cannot predict now.",
            5: "Concentrate and ask again.",
            6: "Don't count on it.",
            7: "It is certain.",
            8: "It is decidedly so.",
            9: "Most likely.",
            10: "My reply is no.",
            11: "My sources say no.",
            12: "Outlook not so good.",
            13: "Outlook good.",
            14: "Reply hazy, try again.",
            15: "Signs point to yes.",
            16: "Very doubtful.",
            17: "Without a doubt.",
            18: "Yes.",
            19: "Yes - definitely.",
            20: "You may rely on it."
        }
        await ctx.send(f"{ctx.message.author.mention}: {eightball_replies[randint(1, 20)]}")

    @commands.command('dog')
    async def random_dog(self, ctx: commands.Context):
        """Sends a random dog. Woof!"""
        filename = requests.get('https://random.dog/woof.json?filter=mp4,webm').json()['url']
        embed = Embed(description='Woof!', colour=Colour(randint(0x000000, 0xFFFFFF)))
        embed.set_image(url=filename)
        await ctx.send(embed=embed)

    @commands.command('cat')
    async def random_cat(self, ctx: commands.Context):
        """Sends a random cat. Meow!"""
        filename = requests.get('http://aws.random.cat/meow').json()['file']
        embed = Embed(description='Meow!', colour=Colour(randint(0x000000, 0xFFFFFF)))
        embed.set_image(url=filename)
        await ctx.send(embed=embed)
