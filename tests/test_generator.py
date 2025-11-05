"""Unit tests for lyric generator"""
import pytest

from src.lyrics.generator import LyricGenerator, generate_bars, generate_hook


class TestLyricGenerator:
    def test_generate_bars_basic(self):
        """Test basic bar generation."""
        generator = LyricGenerator()
        result = generator.generate_bars("Neon Alien", "Fashion", flex=7, chaos=5)
        
        assert isinstance(result, str)
        assert len(result) > 0
        # Should have 4 lines (bars)
        lines = result.split('\n')
        assert len(lines) == 4
    
    def test_generate_bars_custom_count(self):
        """Test generating custom number of bars."""
        generator = LyricGenerator()
        result = generator.generate_bars("Beach Riff", "Snacks", flex=5, chaos=5, num_bars=8)
        
        lines = result.split('\n')
        assert len(lines) == 8
    
    def test_generate_hook_basic(self):
        """Test basic hook generation."""
        generator = LyricGenerator()
        result = generator.generate_hook("Snakeskin Tycoon", "Flexing", flex=8, chaos=6)
        
        assert isinstance(result, str)
        assert len(result) > 0
        # Hook should have at least 2 lines
        lines = result.split('\n')
        assert len(lines) >= 2
    
    def test_generate_hook_with_effects(self):
        """Test hook generation with high flex and chaos."""
        generator = LyricGenerator()
        result = generator.generate_hook("Neon Alien", "Sci-Fi", flex=9, chaos=9)
        
        assert isinstance(result, str)
        # Should have extra lines for flex/chaos effects
        lines = result.split('\n')
        assert len(lines) > 2
    
    def test_generate_method_bars_mode(self):
        """Test generate method with bars mode."""
        generator = LyricGenerator()
        result = generator.generate("Neon Alien", "Fashion", mode="4-Bar Verse")
        
        assert isinstance(result, str)
        lines = result.split('\n')
        assert len(lines) == 4
    
    def test_generate_method_hook_mode(self):
        """Test generate method with hook mode."""
        generator = LyricGenerator()
        result = generator.generate("Beach Riff", "Snacks", mode="Hook Generator")
        
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_generate_method_invalid_mode(self):
        """Test generate method with invalid mode."""
        generator = LyricGenerator()
        
        with pytest.raises(ValueError, match="Invalid mode"):
            generator.generate("Neon Alien", "Fashion", mode="Invalid Mode")
    
    def test_different_personas(self):
        """Test generation with different personas."""
        generator = LyricGenerator()
        personas = ["Neon Alien", "Beach Riff", "Snakeskin Tycoon", "Retro Arcade Savage"]
        
        for persona in personas:
            result = generator.generate_bars(persona, "Fashion")
            assert isinstance(result, str)
            assert len(result) > 0
    
    def test_different_themes(self):
        """Test generation with different themes."""
        generator = LyricGenerator()
        themes = ["Fashion", "Flexing", "Snacks", "Sci-Fi", "Random"]
        
        for theme in themes:
            result = generator.generate_bars("Neon Alien", theme)
            assert isinstance(result, str)
            assert len(result) > 0
    
    def test_flex_levels(self):
        """Test different flex levels."""
        generator = LyricGenerator()
        
        for flex_level in [1, 5, 8, 10]:
            result = generator.generate_bars("Neon Alien", "Fashion", flex=flex_level)
            assert isinstance(result, str)
            assert len(result) > 0
    
    def test_chaos_levels(self):
        """Test different chaos levels."""
        generator = LyricGenerator()
        
        for chaos_level in [0, 5, 8, 10]:
            result = generator.generate_bars("Neon Alien", "Fashion", chaos=chaos_level)
            assert isinstance(result, str)
            assert len(result) > 0


class TestConvenienceFunctions:
    def test_generate_bars_function(self):
        """Test the convenience generate_bars function."""
        result = generate_bars("Neon Alien", "Fashion", 7, 5)
        
        assert isinstance(result, str)
        lines = result.split('\n')
        assert len(lines) == 4
    
    def test_generate_hook_function(self):
        """Test the convenience generate_hook function."""
        result = generate_hook("Beach Riff", "Snacks", 7, 5)
        
        assert isinstance(result, str)
        assert len(result) > 0
