import constants
import nextcord
import re
from nextcord.ext import commands
from utils import discord_utils, logging_utils, command_predicates
from modules.music_race import music_race_constants
import os
import numpy as np
import string


def get_partition_mapping():
    map = {}
    for answer in music_race_constants.ANSWERS:
        for idx, letter in enumerate(answer):
            if letter in map:
                map[letter].append(f"{answer}_part_{idx}")
            else:
                map[letter] = [f"{answer}_part_{idx}"]
    for letter in filter(lambda x: x not in map, string.ascii_uppercase):
        map[letter] = ["silence"]
    return map


class MusicRace(commands.Cog, name="Music Race"):
    """Puzzle for Arithmancy June 2020! Identify each of the movies based on their theme songs!"""

    def __init__(self, bot):
        self.bot = bot
        self.partition_map = get_partition_mapping()

    @command_predicates.is_tester()
    @commands.command(name="notesaw", aliases=["musicpuzzleinfo"])
    async def musicpuzzleinfo(self, ctx):
        """Give the users everything they need to know about the puzzle

        Usage: `~notesaw`
        """
        logging_utils.log_command("notesaw", ctx.guild, ctx.channel, ctx.author)
        embed = discord_utils.create_embed()

        embed.add_field(
            name=f"Welcome to Notesaw!",
            value=f"To start the puzzle, use `{ctx.prefix}guesstune`. "
            f"For example, try `{ctx.prefix}guesstune PIANO`. Have fun!",
            inline=False,
        )
        embed.add_field(
            name=f"Notice",
            value=f"Headphone users! We recommend turning the volume down a bit. Some minor glitches might "
            f"hurt your ear",
            inline=False,
        )
        await ctx.send(embed=embed)

    @command_predicates.is_tester()
    @commands.command(name="guesstune")
    async def guesstune(self, ctx, *args):
        """Take a user's guess and give them a response based on what letters they provided

        Usage: `~guesstune (WORD)`
        """
        logging_utils.log_command("guesstune", ctx.guild, ctx.channel, ctx.author)
        embed = discord_utils.create_embed()

        if len(args) < 1:
            embed = discord_utils.create_no_argument_embed("word")
            await ctx.send(embed=embed)
            return

        # Replace any non-letters
        word = re.sub("[^A-Z]+", "", "".join(args).upper())

        if len(word) < 1 or len(word) > 20:
            embed.add_field(
                name=f"{constants.FAILED}!",
                value=f"Word provided `{word}` is not between 1-20 letters",
            )
            await ctx.send(embed=embed)
            return

        if word in music_race_constants.ANSWERS:
            final_song_path = os.path.join(
                music_race_constants.PUZZLE_OUTPUTS_DIR,
                word + f"_final{music_race_constants.MP3_EXTENSION}",
            )
            if not os.path.exists(final_song_path):
                delay = (
                    music_race_constants.ANSWERS[word][music_race_constants.DELAY]
                    * 1000
                )
                os.system(
                    f"ffmpeg -y -hide_banner -loglevel error -i {os.path.join(music_race_constants.PUZZLE_FULL_SONGS_DIR, word + music_race_constants.MP3_EXTENSION)} -filter_complex 'adelay={delay}|{delay}' {final_song_path}"
                )
                # Not done: ffmpeg-normalize is too slow for now. Try to optimize later.
                # os.system(
                #    f"ffmpeg-normalize -f -c:a libmp3lame {output_path} -o {output_path}"
                # )
            embed.add_field(
                name=f"Well done! You guessed {word}!",
                value=f"\nTo play this tune yourself, use this command. (See {ctx.prefix}playtunehelp for more help)"
                f"\n\n`{music_race_constants.ANSWERS[word][music_race_constants.TUNE]}`",
            )
            await ctx.send(embed=embed)
            await ctx.send(
                file=nextcord.File(
                    final_song_path,
                    filename=f"{list(music_race_constants.ANSWERS).index(word)+1} of {len(music_race_constants.ANSWERS)}.mp3",
                )
            )
            return

        # We need to figure out the longest substring that is part of the answer
        # Add that duration of the song.
        # Afterwards, we need to find all the remaining letters
        # and add random partitions, or silence.
        finalanswer = []
        delay = 0
        # For each letter we match, we can add that to the start of our output song
        for i in range(len(word)):
            found_song = False
            x = word[0 : (i + 1)]
            # Matches one of the songs
            for answer in music_race_constants.ANSWERS:
                if answer.startswith(x):
                    finalanswer.append((f"{answer}_part_{i}", delay))
                    found_song = True
                    break
            # Newly added character is not the start to a song
            if not found_song:
                # Get a random clip with that letter
                if word[i] in self.partition_map:
                    finalanswer.append(
                        (np.random.choice(self.partition_map[word[i]]), delay)
                    )
            # Increments
            delay += 3

        # debug_output_msg = ""
        # for ans in finalanswer:
        #    debug_output_msg += f"{ans[1]}-{ans[1]+3}: {ans[0]}\n"
        # Not done: Remove once we are more certain about how this works. It ruins the puzzle, obviously
        # await ctx.send(debug_output_msg)
        # print(word)
        # print(debug_output_msg)

        inputs = "".join(
            [
                f"-i {os.path.join(music_race_constants.PUZZLE_PARTIAL_SONGS_DIR, finalanswer[idx][0] + '.mp3')} "
                for idx in range(len(finalanswer))
            ]
        )
        # Otherwise, we just chop each song into 3s bits, with 0.5s between them
        filter_complex = "".join(
            [
                f"[{idx}]atrim=0:{music_race_constants.SONG_SNIPPET_LENGTH},adelay={finalanswer[idx][1]*1000+500*idx}|{finalanswer[idx][1]*1000+500*idx},volume={music_race_constants.VOLUME/2}[{letter}];"
                for idx, letter in zip(range(len(finalanswer)), string.ascii_lowercase)
            ]
        )
        mix = "".join(
            [
                f"[{letter}]"
                for _, letter in zip(finalanswer, list(string.ascii_lowercase))
            ]
        )

        output_dir = os.path.join(
            music_race_constants.PUZZLE_OUTPUTS_DIR, ctx.channel.name
        )
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        output_path = os.path.join(output_dir, f"{word}.mp3")
        os.system(
            f"ffmpeg -y -hide_banner -loglevel error {inputs} -preset veryfast "
            + f"-filter_complex '{filter_complex}{mix}amix=inputs={len(finalanswer)}:dropout_transition=1000,volume={music_race_constants.VOLUME/2},loudnorm' "
            f"{output_path}"
        )
        # Not done: ffmpeg-normalize is too slow for now. Try to optimize later.
        # os.system(
        #    f"ffmpeg-normalize -f -c:a libmp3lame {output_path} -o {output_path}"
        # )
        await ctx.send(file=nextcord.File(output_path))


def setup(bot):
    bot.add_cog(MusicRace(bot))
