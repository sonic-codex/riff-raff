"""Unit tests for MIDI generator"""
import pytest

from midi_generator import (
    generate_midi,
    generate_midi_from_bars,
    get_note_from_word,
)


class TestGetNoteFromWord:
    def test_get_note_from_word(self):
        """Test generating note from word."""
        note = get_note_from_word("test")
        
        assert isinstance(note, int)
        assert 60 <= note <= 71  # Within one octave of middle C
    
    def test_get_note_consistent(self):
        """Test that same word produces same note."""
        note1 = get_note_from_word("hello")
        note2 = get_note_from_word("hello")
        
        assert note1 == note2
    
    def test_get_note_different_words(self):
        """Test that different words may produce different notes."""
        note1 = get_note_from_word("hello")
        note2 = get_note_from_word("world")
        
        # They might be different (not guaranteed, but likely)
        assert isinstance(note1, int)
        assert isinstance(note2, int)
    
    def test_get_note_custom_base(self):
        """Test custom base note."""
        note = get_note_from_word("test", base_note=48)
        
        assert 48 <= note <= 59


class TestGenerateMidi:
    def test_generate_midi_basic(self, tmp_path):
        """Test basic MIDI generation."""
        output = tmp_path / "test.mid"
        lyrics = "My ice glows in the matrix"
        
        result = generate_midi(lyrics, str(output))
        
        assert isinstance(result, str)
    
    def test_generate_midi_from_bars(self, tmp_path):
        """Test generating MIDI from bars."""
        output = tmp_path / "test.mid"
        bars = [
            "My ice glows in the matrix",
            "My drip drips on the runway",
            "My swag teleports in space"
        ]
        
        result = generate_midi_from_bars(bars, str(output))
        
        assert isinstance(result, str)
