"""
Module: song_generator

Module with functions for PSA #4 of COMP 110 (Fall 2024.

Authors:
1) Alejandro Torres- atorres1@sandiegoedu
2) Nachi- USD Email Address
"""

import sound

# Do NOT modify the scale_volume function
def scale_volume(original_sound, factor):
    """
    Decreases the volume of a sound object by a specified factor.

    Paramters:
    original_sound (type; Sound): The sound object whose volume is to be decreased.
    factor (type: float): The factor by which the volume is to be decreased.

    Returns:
    (type: Sound) A new sound object that is a copy of original_sound, but with volumes
    scaled by factor.
    """

    scaled_sound = sound.copy(original_sound)

    for smpl in scaled_sound:
        # Scale left channel of smpl
        current_left = smpl.left
        scaled_left = round(current_left * factor)
        smpl.left = scaled_left

        # Scale right channel of smpl
        current_right = smpl.right
        scaled_right = round(current_right * factor)
        smpl.right = scaled_right

    return scaled_sound


def mix_sounds(snd1, snd2):
    """
    Mixes together two sounds (snd1 and snd2) into a single sound.
    If the sounds are of different length, the mixed sound will be the length
    of the longer sound.

    This returns a new sound: it does not modify either of the original
    sounds.

    Parameters:
    snd1 (type: Sound) - The first sound to mix
    snd2 (type: Sound) - The second sound to mix

    Returns:
    (type: Sound) A Sound object that combines the two parameter sounds into a
    single, overlapping sound.
    """
    if len(snd1)>len(snd2):
        mixed_snd = snd1.copy()
        other_snd = snd2
    else:
        mixed_snd = snd2.copy()
        other_snd = snd1
    for i in range (len(other_snd)):
        mix_smpl = mixed_snd[i]
        other_smpl = other_snd[i]
        new_left = mix_smpl.left + other_smpl.left
        new_right = mix_smpl.right + other_smpl.right
        mix_smpl.left = new_left
        mix_smpl.right = new_right

    return mixed_snd




def song_generator(notestring):
    """
    Generates a sound object containing a song specified by the notestring.

    Parameter:
    notestring (type: string) - A string of musical notes and characters to
    change the volume and/or octave of the song.

    Returns:
    (type: Sound) A song generated from the notestring given as a paramter.
    """
    song_acc = sound.create_silent_sound(1)
    note_length = 14700
    multiplier = 0
    octave = 0
    volume_multiplier = 1
    first_channel = None

    if notestring[0] == "[":
        end = notestring.find("]")
        bpm = int(notestring[1:end])
        bps = bpm/60
        note_length = round(44100//bps)
        print(note_length)

    for i in range (len(notestring)):
        ch = notestring[i]
        if multiplier > 0:
            actual_length = note_length * multiplier
            multiplier = 0
        else:
            actual_length = note_length
        if ch in "ABCDEFG":
            song_acc = song_acc + scale_volume(sound.Note(ch, actual_length, octave), volume_multiplier)
        elif ch == "p":
            song_acc = song_acc + scale_volume(sound.create_silent_sound(actual_length), volume_multiplier)
        elif ch.isdigit():
            multiplier = int(ch)
        elif ch == ">":
            octave = octave + 1
        elif ch == "<":
            octave = octave - 1
        elif ch == "+":
            volume_multiplier = volume_multiplier + 0.2
        elif ch == "-":
            volume_multiplier = volume_multiplier - 0.2
        elif ch == "|":
            first_channel = song_acc
            song_acc = sound.create_silent_sound(1)
        if first_channel is not None:
            song_acc = mix_sounds(first_channel, song_acc)
            
        return song_acc
                            



"""
Don't modify anything below this point.
"""

def main():
    """
    Asks the user for a notestring, generates the song from that
    notestring, then plays the resulting song.
    """
    import sounddevice
    print("Enter a notestring (without quotes):")
    ns = input()
    song = song_generator(ns)
    song.play()
    sounddevice.wait()

if __name__ == "__main__":
    main()
