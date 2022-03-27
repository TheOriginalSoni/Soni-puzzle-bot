import nextcord
import os
from nextcord.ext import commands
from emoji import UNICODE_EMOJI
from typing import Union
import constants
from utils import discord_utils, logging_utils, command_predicates


class MiscCog(commands.Cog, name="Misc"):
    """A collection of Misc useful/fun commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="hint", aliases = ["help"])
    async def hint(self, ctx):
        """
        Usage : `~hint`
        """
        logging_utils.log_command("hint", ctx.guild, ctx.channel, ctx.author)
        embed = discord_utils.create_embed()
        embed.add_field(
            name=f"Hint!!",
            value=f"Hints will be given at Arithmancy to those who ask for it! Just tag @hint like usual!",
            inline=False,
        )
        await ctx.send(embed=embed)

    @command_predicates.is_tester()
    @commands.command(name="part0", aliases=["puzzle0"])
    async def part0(self, ctx):
        logging_utils.log_command("part0", ctx.guild, ctx.channel, ctx.author)
        embed = discord_utils.create_embed()
        embed.add_field(
            name=f"???",
            value=f"Part 0 was finding the correct link on https://arithmancy.ueuo.com/ Since you're here, you already solved it. Right??????",
            inline=False,
        )
        await ctx.send(embed=embed)

    @command_predicates.is_tester()
    @commands.command(name="part0ans", aliases=["pranks"])
    async def part0ans(self, ctx):
        logging_utils.log_command("part0ans", ctx.guild, ctx.channel, ctx.author)
        embed = discord_utils.create_embed()
        embed.add_field(
            name=f"Correct!!",
            value=f"Part 0 completed!",
            inline=False,
        )
        await ctx.send(embed=embed)

    @command_predicates.is_tester()
    @commands.command(name="part1", aliases=["puzzle1"])
    async def pranks(self, ctx):
        logging_utils.log_command("puzzle1", ctx.guild, ctx.channel, ctx.author)
        m1 = "<#030042000000100050060004040000005026000000000000000000000000000000000000000000000000000000000000000000000000000000000000>"
        m2 = "<#001100010100000001001100100000100001000000000000000000000000000000000000000000000000000000000000000000000000000000000000>"
        m3 = "<#683248722000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000>"
        await ctx.send(m1)
        await ctx.send(m2)
        await ctx.send(m3)

    @command_predicates.is_tester()
    @commands.command(name="part1ans", aliases=["potato"])
    async def part1ans(self, ctx):
        logging_utils.log_command("part1ans", ctx.guild, ctx.channel, ctx.author)
        embed = discord_utils.create_embed()
        embed.add_field(
            name=f"Correct!!",
            value=f"Part 1 completed!",
            inline=False,
        )
        await ctx.send(embed=embed)

    @command_predicates.is_tester()
    @commands.command(name="part2", aliases=["puzzle2"])
    async def part2(self, ctx):
        logging_utils.log_command("part2", ctx.guild, ctx.channel, ctx.author)
        m1 = "https://cdn.discordapp.com/attachments/824774417649106955/957458640523116584/120.png"
        await ctx.send(m1)

    @command_predicates.is_tester()
    @commands.command(name="part2ans", aliases=["pariah"])
    async def part2ans(self, ctx):
        logging_utils.log_command("part2ans", ctx.guild, ctx.channel, ctx.author)
        embed = discord_utils.create_embed()
        embed.add_field(
            name=f"Correct!!",
            value=f"Part 2 completed!",
            inline=False,
        )
        await ctx.send(embed=embed)

    @command_predicates.is_tester()
    @commands.command(name="part3", aliases=["puzzle3"])
    async def puzzle3(self, ctx):
        logging_utils.log_command("puzzle3", ctx.guild, ctx.channel, ctx.author)
        m1 = "__On__e __star__ in __every__ __same__ one __?__ Ba__ttle__ __who__ ?Add __sect__ors __upon__ __it.__"
        await ctx.send(m1)

    @command_predicates.is_tester()
    @commands.command(name="part3ans", aliases=["poetry"])
    async def part3ans(self, ctx):
        logging_utils.log_command("part3ans", ctx.guild, ctx.channel, ctx.author)
        embed = discord_utils.create_embed()
        embed.add_field(
            name=f"Correct!!",
            value=f"Part 3 completed!",
            inline=False,
        )
        await ctx.send(embed=embed)

    @command_predicates.is_tester()
    @commands.command(name="part4", aliases=["puzzle4"])
    async def part4(self, ctx):
        logging_utils.log_command("part4", ctx.guild, ctx.channel, ctx.author)
        loc = "files/phone.zip"
        file = nextcord.File(loc)
        await ctx.send(file=file)

    @command_predicates.is_tester()
    @commands.command(name="part4ans", aliases=["polska"])
    async def part4ans(self, ctx):
        logging_utils.log_command("part4ans", ctx.guild, ctx.channel, ctx.author)
        embed = discord_utils.create_embed()
        embed.add_field(
            name=f"Correct!!",
            value=f"Part 4 completed!",
            inline=False,
        )
        await ctx.send(embed=embed)

    @command_predicates.is_tester()
    @commands.command(name="part5", aliases=["puzzle5"])
    async def part5(self, ctx):
        logging_utils.log_command("part5", ctx.guild, ctx.channel, ctx.author)
        m1 = "https://cdn.discordapp.com/attachments/738306742139748422/955691396109565952/irrational.png"
        await ctx.send(m1)

    @command_predicates.is_tester()
    @commands.command(name="part5ans", aliases=["pirate"])
    async def part5ans(self, ctx):
        logging_utils.log_command("part5ans", ctx.guild, ctx.channel, ctx.author)
        embed = discord_utils.create_embed()
        embed.add_field(
            name=f"Correct!!",
            value=f"Part 5 completed!",
            inline=False,
        )
        await ctx.send(embed=embed)

    @command_predicates.is_tester()
    @commands.command(name="part6", aliases=["puzzle6"])
    async def part6(self, ctx):
        logging_utils.log_command("part6", ctx.guild, ctx.channel, ctx.author)
        m1 = "**Including itself, what is the quickest way out of this hellscape?**\n\n Note - This is the last puzzle and goes into submission box. \n\n Also while we're here, what's your favourite thing about Arithmancy?"
        await ctx.send(m1)

    ###################
    # BOTSAY COMMANDS #
    ###################

    @command_predicates.is_trusted()
    @commands.command(name="botsay")
    async def botsay(self, ctx, channel_id_or_name: str, *args):
        """Say something in another channel

        Permission Category : Trusted roles only.
        Usage: `~botsay channelname Message`
        Usage: `~botsay #channelmention Longer Message`
        """
        logging_utils.log_command("botsay", ctx.guild, ctx.channel, ctx.author)
        embed = discord_utils.create_embed()

        if len(args) < 1:
            embed = discord_utils.create_no_argument_embed("Message")
            await ctx.send(embed=embed)
            return

        message = " ".join(args)
        guild = ctx.message.guild

        try:
            channel = await commands.TextChannelConverter().convert(
                ctx, channel_id_or_name
            )
        except ValueError:
            embed.add_field(
                name=f"{constants.FAILED}!",
                value=f"Error! The channel `{channel_id_or_name}` was not found",
            )
            await ctx.send(embed=embed)
            return

        try:
            await channel.send(message)
        except nextcord.Forbidden:
            embed.add_field(
                name=f"{constants.FAILED}!",
                value=f"Forbidden! The bot is unable to speak on {channel.mention}! Have you checked if "
                f"the bot has the required permisisons?",
            )
            await ctx.send(embed=embed)
            return

        embed.add_field(
            name=f"{constants.SUCCESS}!",
            value=f"Message sent to {channel.mention}: {message}!",
        )
        # reply to user
        await ctx.send(embed=embed)

    @command_predicates.is_trusted()
    @commands.command(name="botsayembed")
    async def botsayembed(self, ctx, channel_id_or_name: str, *args):
        """Say something in another channel, but as an embed

        Permission Category : Trusted roles only.
        Usage: `~botsayembed channelname Message`
        Usage: `~botsayembed #channelmention Longer Message`
        """
        logging_utils.log_command("botsayembed", ctx.guild, ctx.channel, ctx.author)
        embed = discord_utils.create_embed()

        if len(args) < 1:
            embed = discord_utils.create_no_argument_embed("Message")
            await ctx.send(embed=embed)
            return

        message = " ".join(args)

        try:
            channel = await commands.TextChannelConverter().convert(
                ctx, channel_id_or_name
            )
        except ValueError:
            embed.add_field(
                name=f"{constants.FAILED}!",
                value=f"Error! The channel `{channel_id_or_name}` was not found",
            )
            await ctx.send(embed=embed)
            return

        try:
            sent_embed = discord_utils.create_embed()
            sent_embed.description = message
            await channel.send(embed=sent_embed)
        except nextcord.Forbidden:
            embed.add_field(
                name=f"{constants.FAILED}!",
                value=f"Forbidden! The bot is unable to speak on {channel.mention}! Have you checked if "
                f"the bot has the required permisisons?",
            )
            await ctx.send(embed=embed)
            return

        # reply to user
        sent_embed.add_field(
            name=f"{constants.SUCCESS}!",
            value=f"Embed sent to {channel.mention}",
            inline=False,
        )
        await ctx.send(embed=sent_embed)


    @commands.command(name="getsource")
    async def getsource(self, ctx):
        """Gives the discord formatted source code for a specific message in the channel.
        This command must be a reply

        Usage: `~getsource` (as a reply to the message)
        """
        logging_utils.log_command("getsource", ctx.guild, ctx.channel, ctx.author)
        embed = discord_utils.create_embed()

        # If not direct reply to another message
        if not ctx.message.reference:
            embed.add_field(
                name=f"{constants.FAILED}!",
                value=f"The command `~getsource` can only be used as a reply to another message.",
                inline=False,
            )
            await ctx.send(embed=embed)
            return

        orig_msg = ctx.message.reference.resolved
        if orig_msg.content is None or len(orig_msg.content) == 0:
            embed.add_field(
                name=f"{constants.FAILED}!",
                value=f"The replied message has no content to `~getsource` from. Is it a bot or system message?",
                inline=False,
            )
            await ctx.send(embed=embed)
            return

        msg = "```" + orig_msg.content + "```"
        embed.add_field(
            name=f"{constants.SUCCESS}!",
            value=f"{msg}",
            inline=False,
        )
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(MiscCog(bot))
