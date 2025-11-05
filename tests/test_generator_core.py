"""Unit tests for generator_core"""
import pytest

from generator_core import generate_bars, generate_hook, get_theme_words, load_persona


class TestGeneratorCore:
    def test_load_persona(self):
        """Test loading a persona."""
        vocab, styles = load_persona("Neon Alien")
        
        assert isinstance(vocab, list)
        assert isinstance(styles, list)
        assert len(vocab) > 0
        assert len(styles) > 0
    
    def test_get_theme_words(self):
        """Test getting theme words."""
        words = get_theme_words("Fashion")
        
        assert isinstance(words, list)
        assert len(words) > 0
        assert "drip" in words or "flex" in words
    
    def test_generate_bars(self):
        """Test generating bars."""
        result = generate_bars("Neon Alien", "Fashion", 7, 5)
        
        assert isinstance(result, str)
        assert len(result) > 0
        lines = result.split('\n')
        assert len(lines) == 4
    
    def test_generate_hook(self):
        """Test generating hook."""
        result = generate_hook("Beach Riff", "Snacks", 7, 5)
        
        assert isinstance(result, str)
        assert len(result) > 0
