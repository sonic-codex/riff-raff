"""Unit tests for vault manager"""
import json
from pathlib import Path

import pytest

from vault_manager import load_lyrics, save_lyrics


class TestVaultManager:
    def test_save_and_load_lyrics(self, tmp_path):
        """Test saving and loading lyrics."""
        test_file = tmp_path / "lyrics.json"
        test_lyrics = [
            {
                "text": "Test lyrics",
                "persona": "Neon Alien",
                "theme": "Fashion"
            }
        ]
        
        save_lyrics(test_lyrics, str(test_file))
        loaded = load_lyrics(str(test_file))
        
        assert loaded == test_lyrics
    
    def test_load_nonexistent_file(self, tmp_path):
        """Test loading non-existent file returns empty list."""
        test_file = tmp_path / "nonexistent.json"
        
        result = load_lyrics(str(test_file))
        
        assert result == []
    
    def test_save_overwrites_file(self, tmp_path):
        """Test that save overwrites existing file."""
        test_file = tmp_path / "lyrics.json"
        
        # Save first set
        lyrics1 = [{"text": "First"}]
        save_lyrics(lyrics1, str(test_file))
        
        # Save second set
        lyrics2 = [{"text": "Second"}]
        save_lyrics(lyrics2, str(test_file))
        
        # Should have second set
        loaded = load_lyrics(str(test_file))
        assert loaded == lyrics2
