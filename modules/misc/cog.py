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

    @commands.command(name="pranks")
    async def pranks(self, ctx):
        """
        Usage : `~pranks`
        """
        logging_utils.log_command("pranks", ctx.guild, ctx.channel, ctx.author)
        message1 = "<#5324614613526251433146252435161562340000000000000000000000000000000000000000000000000000000000000000000000000000000>"
        message2 = "<#0001111101101101100000111010000010100000000000000000000000000000000000000000000000000000000000000000000000000000000>"
        message3 = "<#6832487220000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000>" 
        await ctx.send(message=message1)
        await ctx.send(message=message2)
        await ctx.send(message=message3)

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
