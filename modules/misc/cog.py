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

    @commands.command(name="hint")
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
    @commands.command(name="pranks", aliases=["puzzle1"])
    async def pranks(self, ctx):
        """
        Usage : `~pranks`
        """
        logging_utils.log_command("pranks", ctx.guild, ctx.channel, ctx.author)
        m1 = "<#030042000000100050060004040000005026000000000000000000000000000000000000000000000000000000000000000000000000000000000000>"
        m2 = "<#001100010100000001001100100000100001000000000000000000000000000000000000000000000000000000000000000000000000000000000000>"
        m3 = "<#683248722000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000>"
        await ctx.send(m1)
        await ctx.send(m2)
        await ctx.send(m3)

    @command_predicates.is_tester()
    @commands.command(name="potato", aliases=["puzzle2"])
    async def potato(self, ctx):
        """
        Usage : `~potato`
        """
        logging_utils.log_command("potato", ctx.guild, ctx.channel, ctx.author)
        m1 = "https://cdn.discordapp.com/attachments/738306742139748422/955697060697501746/120.png"
        await ctx.send(m1)

    @command_predicates.is_tester()
    @commands.command(name="pariah", aliases=["puzzle3"])
    async def pariah(self, ctx):
        """
        Usage : `~pariah`
        """
        logging_utils.log_command("pariah", ctx.guild, ctx.channel, ctx.author)
        loc = "files/sounding.zip"
        file = nextcord.File(loc)
        await ctx.send(file=file)

    @command_predicates.is_tester()
    @commands.command(name="poetry", aliases=["puzzle4"])
    async def poetry(self, ctx):
        """
        Usage : `~poetry`
        """
        logging_utils.log_command("poetry", ctx.guild, ctx.channel, ctx.author)
        m1 = "__On__e __star__ in __every__ __same__ one __?__ Ba__ttle__ __who__ ?Add __sect__ors __upon__ __it.__"
        await ctx.send(m1)

    @command_predicates.is_tester()
    @commands.command(name="polska", aliases=["puzzle5"])
    async def polska(self, ctx):
        """
        Usage : `~polska`
        """
        logging_utils.log_command("polska", ctx.guild, ctx.channel, ctx.author)
        m1 = "https://cdn.discordapp.com/attachments/738306742139748422/955691396109565952/irrational.png"
        await ctx.send(m1)

    @command_predicates.is_tester()
    @commands.command(name="pirate", aliases=["puzzle6"])
    async def pirate(self, ctx):
        """
        Usage : `~pirate`
        """
        logging_utils.log_command("pirate", ctx.guild, ctx.channel, ctx.author)
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


def setup(bot):
    bot.add_cog(MiscCog(bot))
