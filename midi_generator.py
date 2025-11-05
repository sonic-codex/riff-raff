# Melody/MIDI creation from lyrics
"""MIDI generation from lyrics with simple beat patterns."""
import random
from pathlib import Path
from typing import List, Optional

try:
    import mido
    from mido import Message, MidiFile, MidiTrack
    MIDO_AVAILABLE = True
except ImportError:
    MIDO_AVAILABLE = False
    print("Warning: mido not installed. MIDI generation will be simulated.")


def get_note_from_word(word: str, base_note: int = 60) -> int:
    """Generate a MIDI note number based on a word.

    Args:
        word: Input word to generate note from
        base_note: Base MIDI note (default: 60 = Middle C)

    Returns:
        MIDI note number (0-127)
    """
    # Simple hash-based note generation
    hash_val = sum(ord(c) for c in word.lower())
    offset = hash_val % 12  # Stay within one octave
    return base_note + offset


def create_simple_beat(tempo: int = 120, num_bars: int = 4) -> Optional[MidiTrack]:
    """Create a simple drum/beat track.

    Args:
        tempo: Tempo in BPM
        num_bars: Number of bars to generate

    Returns:
        MIDI track with drum pattern, or None if mido not available
    """
    if not MIDO_AVAILABLE:
        return None

    track = MidiTrack()

    # Set tempo (microseconds per beat)
    tempo_value = int(60000000 / tempo)
    track.append(mido.MetaMessage('set_tempo', tempo=tempo_value))

    # Simple 4/4 beat pattern
    # MIDI channel 9 (index 10) is reserved for drums
    kick = 36  # Bass drum
    snare = 38  # Snare
    hihat = 42  # Closed hi-hat

    ticks_per_beat = 480
    ticks_per_bar = ticks_per_beat * 4

    for bar in range(num_bars):
        # Beat 1: Kick + Hi-hat
        track.append(Message('note_on', channel=9, note=kick, velocity=100, time=0))
        track.append(Message('note_on', channel=9, note=hihat, velocity=80, time=0))
        track.append(Message('note_off', channel=9, note=kick, velocity=0, time=ticks_per_beat // 4))
        track.append(Message('note_off', channel=9, note=hihat, velocity=0, time=0))

        # Beat 2: Snare + Hi-hat
        track.append(Message('note_on', channel=9, note=snare, velocity=90, time=ticks_per_beat - ticks_per_beat // 4))
        track.append(Message('note_on', channel=9, note=hihat, velocity=80, time=0))
        track.append(Message('note_off', channel=9, note=snare, velocity=0, time=ticks_per_beat // 4))
        track.append(Message('note_off', channel=9, note=hihat, velocity=0, time=0))

        # Beat 3: Kick + Hi-hat
        track.append(Message('note_on', channel=9, note=kick, velocity=100, time=ticks_per_beat - ticks_per_beat // 4))
        track.append(Message('note_on', channel=9, note=hihat, velocity=80, time=0))
        track.append(Message('note_off', channel=9, note=kick, velocity=0, time=ticks_per_beat // 4))
        track.append(Message('note_off', channel=9, note=hihat, velocity=0, time=0))

        # Beat 4: Snare + Hi-hat
        track.append(Message('note_on', channel=9, note=snare, velocity=90, time=ticks_per_beat - ticks_per_beat // 4))
        track.append(Message('note_on', channel=9, note=hihat, velocity=80, time=0))
        track.append(Message('note_off', channel=9, note=snare, velocity=0, time=ticks_per_beat // 4))
        track.append(Message('note_off', channel=9, note=hihat, velocity=0, time=0))

    return track


def generate_midi(
    lyrics: str,
    output_path: str = "output.mid",
    tempo: int = 120,
    base_note: int = 60
) -> str:
    """Generate MIDI file from lyrics.

    Args:
        lyrics: Input lyrics text
        output_path: Path to save the MIDI file
        tempo: Tempo in BPM (default: 120)
        base_note: Base MIDI note (default: 60 = Middle C)

    Returns:
        Path to the generated MIDI file
    """
    if not MIDO_AVAILABLE:
        print(f"MIDI generation simulated for lyrics: {lyrics[:50]}...")
        return "midi_file.mid"

    # Create MIDI file
    mid = MidiFile()

    # Create melody track
    melody_track = MidiTrack()
    mid.tracks.append(melody_track)

    # Set tempo
    tempo_value = int(60000000 / tempo)
    melody_track.append(mido.MetaMessage('set_tempo', tempo=tempo_value))

    # Parse lyrics and generate notes
    words = lyrics.split()
    ticks_per_beat = 480
    note_duration = ticks_per_beat // 2  # Eighth notes

    for i, word in enumerate(words):
        # Generate note from word
        note = get_note_from_word(word, base_note)

        # Add some variation
        velocity = random.randint(70, 100)

        # Note on
        melody_track.append(
            Message('note_on', note=note, velocity=velocity, time=0 if i == 0 else note_duration)
        )

        # Note off
        melody_track.append(
            Message('note_off', note=note, velocity=0, time=note_duration)
        )

    # Create beat track
    num_bars = max(1, len(words) // 4)
    beat_track = create_simple_beat(tempo, num_bars)
    if beat_track:
        mid.tracks.append(beat_track)

    # Save MIDI file
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    mid.save(str(output_file))

    print(f"MIDI file generated: {output_path}")
    return str(output_path)


def generate_midi_from_bars(
    bars: List[str],
    output_path: str = "output.mid",
    tempo: int = 120
) -> str:
    """Generate MIDI from a list of bars.

    Args:
        bars: List of bar strings
        output_path: Path to save the MIDI file
        tempo: Tempo in BPM

    Returns:
        Path to the generated MIDI file
    """
    # Join bars into single lyrics string
    lyrics = " ".join(bars)
    return generate_midi(lyrics, output_path, tempo)
