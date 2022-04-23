import shutil

from modules.perfect_pitch import perfect_pitch_constants
import os
import string
import constants
import numpy as np


class Note:
    def __init__(self, letter, duration, octave, instrument):
        """Arguments:
        - letter: e.g. C, E, G, and R means rest
        - duration: e.g. quarter, whole, half, sixteenth
        - octave: e.g. 0, 1, .., 7
        - instrument: e.g. piano, trumpet, etc."""
        self.letter = letter
        self.duration = duration
        # Rest notes don't have octave, instrument, or files
        if letter == "R":
            self.octave = None
            self.instrument = None
            self.path = None
        else:
            self.octave = octave
            self.instrument = instrument
            # Not Done: is this the best way to check if a note is inside an instrument's range?
            proposed_path = os.path.join(
                os.getcwd(),
                constants.MODULES_DIR,
                perfect_pitch_constants.PERFECT_PITCH.lower().replace(" ", "_"),
                perfect_pitch_constants.MUSIC,
                self.instrument,
                perfect_pitch_constants.NOTES,
                f"{self.letter}{self.octave}.mp3",
            )
            if os.path.exists(proposed_path):
                self.path = proposed_path
            else:
                self.path = os.path.join(
                    os.getcwd(),
                    constants.MODULES_DIR,
                    perfect_pitch_constants.PERFECT_PITCH.lower().replace(" ", "_"),
                    perfect_pitch_constants.MUSIC,
                    "piano",
                    perfect_pitch_constants.NOTES,
                    f"{self.letter}{self.octave}.mp3",
                )


class Tune:
    """A tune to be combined by FFMPEG as audio"""

    def __init__(self, channel_name):
        """Set default parameters"""
        # Speed of tune
        self.meter = 1
        # Time between notes
        self.default_interval = 500
        # Length of 1 note (1 is quarter, 4 is whole, etc.)
        self.default_duration = 1
        # octave to set each note to (unless otherwise specified)
        self.default_octave = 4
        self.instrument = perfect_pitch_constants.PIANO
        self.notes = []
        # Used for creating output file
        self.channel_name = channel_name

    def process_args(self, args) -> None:
        """Handle input arguments into meter, octave, instrument, and notes
        - meter: {m, meter}={float>0}
        - octave: {o, octave}={int\in[0,...,7]}
        - instrument: {piano}
        -
        """
        for arg in args:
            # Check if arg is meter
            # NOTE: we will only accept one meter, and so first one wins
            if arg.startswith("m=") or arg.startswith("meter="):
                try:
                    self.meter = float(arg.split("=")[-1])
                except ValueError:
                    print(f"{arg} is not a meter")
                    # If they do not properly supply the meter, just ignore it and keep the default
                    pass
            elif arg.startswith("o=") or arg.startswith("octave="):
                try:
                    self.default_octave = int(arg.split("=")[-1])
                except ValueError:
                    print(f"{arg} is not an octave")
                    # If they do not properly supply the octave, just ignore it and keep the default
                    pass
            # Not Done:: add instrument handling here
            elif arg.startswith("i=") or arg.startswith("instrument="):
                self.instrument = arg.split("=")[-1].lower()
            # Right now there is only piano so
            # if the arg is not a meter or an octave then it must be a note
            else:
                try:
                    # Not Done:: Let's you stack multiple notes at the same time, but it doesn't work very well...
                    # if 'v' in arg:
                    #    for chord_idx, chord_note in enumerate(arg.split('v')):
                    #        self.notes.append(self.get_note(chord_note))
                    #        if chord_idx < len(arg.split('v')) - 1:
                    #            self.notes[-1].duration = 0
                    # else:
                    self.notes.append(self.get_note(arg))
                except KeyError:
                    print(f"{arg} is not a note")
                    # If it's not in the note dict, then it must be some random dead argument
                    pass

    def get_note(self, note) -> Note:
        """Process one note str
        Notes can come in one of 8 formats (Not Done: instrument?)
        A pure natural note, no octave e.g. C
        A note with flat or sharp e.g. Eb
        A natural note with octave e.g. C4
        A note with flat/sharp and octave, e.g. F#3
        Or at the end it can have a duration e.g. w, h, q, e, s for now with d to represent dotted notes
        Like C4s, Ab3ed
        Or, for noobs, you can do L<duration>, e.g. C4L2 to represent a half note, C4L0.5 to represent an eighth
        """
        # Get duration, which can come in two forms. "L" or dotted
        # "L" duration
        if len(note.split("L")) > 1:
            split_note = note.split("L")
            duration = float(split_note[1])
            note = split_note[0]
        # Duration includes a dot (e.g. wd, hd, ...)
        elif note[-2:] in perfect_pitch_constants.DURATIONS:
            duration = perfect_pitch_constants.DURATIONS[note[-2:]]
            note = note[:-2]
        # Standard duration (e.g. w, h, e, s)
        elif note[-1:] in perfect_pitch_constants.DURATIONS:
            duration = perfect_pitch_constants.DURATIONS[note[-1:]]
            note = note[:-1]
        # No duration provided
        else:
            duration = self.default_duration
        # Next, check if last character is an int for octave
        try:
            octave = int(note[-1])
            # Remove octave from note
            note = note[:-1]
        except ValueError:
            octave = self.default_octave
        # Not Done: instrument?
        instrument = self.instrument
        # Get the letter (handle sharps and flats in a lookup table)
        letter = perfect_pitch_constants.CLEANED_NOTES[note]

        return Note(letter, duration, octave, instrument)

    async def create_tune(self) -> str:
        """Use FFMPEG to mix the notes, and return the path of the mixed audio"""
        # Store the tune here. NOTE: only one tune per channel, for scaling reasons and within arithmancy puzzling.
        # Not Done: Maybe fix later?
        output_dir = os.path.join(
            os.getcwd(),
            constants.MODULES_DIR,
            perfect_pitch_constants.PERFECT_PITCH.lower().replace(" ", "_"),
            perfect_pitch_constants.MUSIC,
            perfect_pitch_constants.TUNES,
            self.channel_name,
        )
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
            os.mkdir(output_dir)
        final_output_path = os.path.join(output_dir, "tune.mp3")
        # R represents a resting note, which we want for the timing but we do not want to use as an input since
        # it doesn't have a path.
        # Get all non-resting notes
        input_notes = list(
            filter(lambda x: x.letter != perfect_pitch_constants.REST, self.notes)
        )
        input_paths = [f"-i {note.path}" for note in input_notes]
        # We need to keep track of where each note should come in the tune.
        # Each note after the first will need to be delayed by some amount
        delay = 0

        time_indices = []
        # We enumerate over notes and not input notes here because
        # We don't actually add REST to the song (input_notes), but we need to keep track of rest's time delays.
        for idx, note in enumerate(self.notes):
            if idx > 0:
                delay += (
                    self.default_interval * self.notes[idx - 1].duration / self.meter
                )
            else:
                delay = 0
            if not note.letter == perfect_pitch_constants.REST:
                time_indices.append(delay)
        # We only need this to be a numpy array if there is more than 1 partition
        # I think the code should diverge if there is
        # FFMPEG has a limit of about 26 audio input tracks, so we need to partition if there are more than
        # 26 notes

        # The code for one partition can be much easier than multiple partitions, so I think we should handle them
        # differently
        if len(input_notes) <= perfect_pitch_constants.MAX_PARTITION_SIZE:
            filter_complex = "".join(
                [
                    f"[{idx}]atrim=0:{input_notes[idx].duration+0.125},adelay={time_indices[idx]}|{time_indices[idx]}[{letter}];"
                    for idx, letter in zip(
                        range(len(time_indices)), list(string.ascii_lowercase)
                    )
                ]
            )
            mix = "".join(
                [
                    f"[{letter}]"
                    for _, letter in zip(time_indices, list(string.ascii_lowercase))
                ]
            )
            # Call ffmpeg from the command line
            os.system(
                f"ffmpeg -y {' '.join(input_paths)} -filter_complex "
                f"'{filter_complex}{mix}amix=inputs={len(time_indices)}:dropout_transition=1000,volume={perfect_pitch_constants.VOLUME},loudnorm' {final_output_path}"
            )
            # Not Done: optimize ffmpeg-normalize
            # os.system(
            #    f"ffmpeg-normalize -f -c:a libmp3lame {final_output_path} -o {final_output_path}"
            # )
        # Multi-Partition Case
        else:
            # Split notes into equal-part partitions
            # num paritions: ceil(35 / 25) = 2
            # partition size: ceil(35 / 2) = 18
            num_partitions = int(
                np.ceil(len(input_notes) / perfect_pitch_constants.MAX_PARTITION_SIZE)
            )
            partition_size = int(np.ceil(len(input_notes) / num_partitions))

            relative_time_indices = np.array(time_indices).copy()
            # Store time indices to merge each partition
            merge_time_indices = []
            merge_paths = []
            # Collect all partition parts
            # This is the ffmpeg mixing part, where we add each note at the specified delay

            for partition_idx in range(num_partitions):
                partition_start_index = partition_idx * partition_size
                partition_output_path = os.path.join(
                    output_dir, f"partition{partition_idx}.mp3"
                )
                merge_paths.append(f"-i {partition_output_path}")

                # Get all notes, file paths, and time indices for that partition
                partition_input_notes = input_notes[
                    partition_start_index : partition_start_index + partition_size
                ]
                partition_input_paths = input_paths[
                    partition_start_index : partition_start_index + partition_size
                ]
                partition_time_indices = relative_time_indices[
                    partition_start_index : partition_start_index + partition_size
                ]
                # Keep track of the times we will need to merge each partition back in at the end
                # Not Done: We're doing something a little funky with the time...
                # Either we have to do -1 in the index of merge_time_indices, or we have to subtract the next index for
                # relative time indices. Technically, the latter way is more correct. the current way kinda looks cleaner.
                merge_time_indices.append(
                    time_indices[partition_idx * partition_size - 1]
                    if partition_idx > 0
                    else 0
                )
                # Relative time indices keeps track of the delays relative to that partition.
                # The start of partition 2 should have time 0, so we need to subtract the lar.... see Note above
                relative_time_indices = (
                    relative_time_indices - partition_time_indices[-1]
                )
                # Create the filter_complex part of the ffmpeg string. This is the part that
                filter_complex = "".join(
                    [
                        f"[{idx}]atrim=0:{partition_input_notes[idx].duration+0.125},"
                        f"adelay={partition_time_indices[idx]}|{partition_time_indices[idx]}[{letter}];"
                        for idx, letter in zip(
                            range(len(partition_input_notes)),
                            list(string.ascii_lowercase),
                        )
                    ]
                )
                mix = "".join(
                    [
                        f"[{letter}]"
                        for _, letter in zip(
                            partition_input_notes, list(string.ascii_lowercase)
                        )
                    ]
                )

                os.system(
                    f"ffmpeg -y {' '.join(partition_input_paths)} -filter_complex "
                    f"'{filter_complex}{mix}amix=inputs={len(partition_input_notes)}:dropout_transition=1000,"
                    f"volume={perfect_pitch_constants.VOLUME},loudnorm' {partition_output_path}"
                )

            # AFTER EACH PARTITION HAS BEEN CREATED, REMERGE THE PARTITIONS
            filter_complex = "".join(
                [
                    f"[{idx}]adelay={merge_time_indices[idx]}|{merge_time_indices[idx]}[{letter}];"
                    for idx, letter in zip(
                        range(len(merge_time_indices)), list(string.ascii_lowercase)
                    )
                ]
            )
            mix = "".join(
                [
                    f"[{letter}]"
                    for _, letter in zip(
                        merge_time_indices, list(string.ascii_lowercase)
                    )
                ]
            )
            # Call ffmpeg from the command line
            os.system(
                f"ffmpeg -y {' '.join(merge_paths)} -filter_complex "
                f"'{filter_complex}{mix}amix=inputs={len(merge_time_indices)},"
                f"volume={perfect_pitch_constants.VOLUME},loudnorm' {final_output_path}"
            )
            # Not Done: ffmpeg-normalize is too slow for now
            # os.system(
            #    f"ffmpeg-normalize -f -c:a libmp3lame {final_output_path} -o {final_output_path}"
            # )

        return final_output_path
