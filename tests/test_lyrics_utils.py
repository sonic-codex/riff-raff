"""Unit tests for lyrics utilities"""
import pytest

from src.lyrics.utils import (
    clean_lyric_text,
    format_bar_output,
    get_chaos_phrases,
    get_flex_phrases,
    get_persona_hooks,
    get_theme_objects,
    get_theme_responses,
    get_theme_words,
    parse_generation_params,
)


class TestThemeFunctions:
    def test_get_theme_words(self):
        """Test getting theme words."""
        themes = ["Fashion", "Flexing", "Snacks", "Sci-Fi", "Random"]
        
        for theme in themes:
            words = get_theme_words(theme)
            assert isinstance(words, list)
            assert len(words) > 0
    
    def test_get_theme_objects(self):
        """Test getting theme objects."""
        themes = ["Fashion", "Flexing", "Snacks", "Sci-Fi", "Random"]
        
        for theme in themes:
            objects = get_theme_objects(theme)
            assert isinstance(objects, list)
            assert len(objects) > 0
    
    def test_get_theme_responses(self):
        """Test getting theme responses."""
        themes = ["Fashion", "Flexing", "Snacks", "Sci-Fi", "Random"]
        
        for theme in themes:
            responses = get_theme_responses(theme)
            assert isinstance(responses, list)
            assert len(responses) > 0


class TestPersonaFunctions:
    def test_get_persona_hooks(self):
        """Test getting persona hooks."""
        personas = ["Neon Alien", "Beach Riff", "Snakeskin Tycoon", "Retro Arcade Savage"]
        
        for persona in personas:
            hooks = get_persona_hooks(persona)
            assert isinstance(hooks, list)
            assert len(hooks) > 0
    
    def test_get_unknown_persona_hooks(self):
        """Test getting hooks for unknown persona returns default."""
        hooks = get_persona_hooks("Unknown Persona")
        assert isinstance(hooks, list)
        assert len(hooks) > 0


class TestFlexAndChaosPhrases:
    def test_get_flex_phrases_low(self):
        """Test getting flex phrases for low level."""
        phrases = get_flex_phrases(2)
        assert isinstance(phrases, list)
        assert len(phrases) > 0
    
    def test_get_flex_phrases_medium(self):
        """Test getting flex phrases for medium level."""
        phrases = get_flex_phrases(5)
        assert isinstance(phrases, list)
        assert len(phrases) > 0
    
    def test_get_flex_phrases_high(self):
        """Test getting flex phrases for high level."""
        phrases = get_flex_phrases(9)
        assert isinstance(phrases, list)
        assert len(phrases) > 0
    
    def test_get_chaos_phrases_low(self):
        """Test getting chaos phrases for low level."""
        phrases = get_chaos_phrases(2)
        assert isinstance(phrases, list)
        assert len(phrases) > 0
    
    def test_get_chaos_phrases_medium(self):
        """Test getting chaos phrases for medium level."""
        phrases = get_chaos_phrases(5)
        assert isinstance(phrases, list)
        assert len(phrases) > 0
    
    def test_get_chaos_phrases_high(self):
        """Test getting chaos phrases for high level."""
        phrases = get_chaos_phrases(9)
        assert isinstance(phrases, list)
        assert len(phrases) > 0


class TestTextProcessing:
    def test_clean_lyric_text(self):
        """Test cleaning lyric text."""
        dirty = "My  drip   glows   on the runway."
        clean = clean_lyric_text(dirty)
        
        assert "  " not in clean
        assert clean == "My drip glows on the runway."
    
    def test_format_bar_output(self):
        """Test formatting bars."""
        bars = ["Line 1", "Line 2", "Line 3"]
        formatted = format_bar_output(bars)
        
        assert formatted == "Line 1\nLine 2\nLine 3"


class TestParseGenerationParams:
    def test_parse_valid_params(self):
        """Test parsing valid parameters."""
        params = {
            "flex_level": 7,
            "nonsense": 5,
            "persona": "Neon Alien",
            "theme": "Fashion",
            "mode": "4-Bar Verse"
        }
        
        validated = parse_generation_params(params)
        
        assert validated["flex_level"] == 7
        assert validated["nonsense"] == 5
        assert validated["persona"] == "Neon Alien"
        assert validated["theme"] == "Fashion"
        assert validated["mode"] == "4-Bar Verse"
    
    def test_parse_invalid_flex_level(self):
        """Test parsing invalid flex level."""
        params = {"flex_level": 15}
        
        with pytest.raises(ValueError):
            parse_generation_params(params)
    
    def test_parse_invalid_nonsense(self):
        """Test parsing invalid nonsense level."""
        params = {"nonsense": -1}
        
        with pytest.raises(ValueError):
            parse_generation_params(params)
