"""Unit tests for persona vocab loader"""
import json
from pathlib import Path

import pytest

from src.personas.vocab_loader import PersonaVocabLoader, load_persona


class TestPersonaVocabLoader:
    def test_load_base_persona(self):
        """Test loading base persona."""
        loader = PersonaVocabLoader()
        vocab, styles = loader.load_persona("NonExistentPersona")
        
        # Should load base persona when specific one doesn't exist
        assert isinstance(vocab, list)
        assert isinstance(styles, list)
        assert len(vocab) > 0
        assert len(styles) > 0

    def test_load_neon_alien_persona(self):
        """Test loading Neon Alien persona."""
        loader = PersonaVocabLoader()
        vocab, styles = loader.load_persona("Neon Alien")
        
        # Should have combined base + persona vocab
        assert isinstance(vocab, list)
        assert isinstance(styles, list)
        assert len(vocab) > 0
    
    def test_cache_functionality(self):
        """Test that caching works."""
        loader = PersonaVocabLoader()
        
        # Load twice
        vocab1, styles1 = loader.load_persona("Neon Alien")
        vocab2, styles2 = loader.load_persona("Neon Alien")
        
        # Should get same objects from cache
        assert vocab1 == vocab2
        assert styles1 == styles2
    
    def test_clear_cache(self):
        """Test clearing the cache."""
        loader = PersonaVocabLoader()
        loader.load_persona("Neon Alien")
        
        loader.clear_cache()
        
        # Cache should be empty
        assert len(loader._cache) == 0
    
    def test_list_available_personas(self):
        """Test listing available personas."""
        loader = PersonaVocabLoader()
        personas = loader.list_available_personas()
        
        assert isinstance(personas, list)
        # Should have at least the personas we created
        assert "Neon Alien" in personas or "Beach Riff" in personas
    
    def test_validate_persona_file(self):
        """Test validating persona files."""
        loader = PersonaVocabLoader()
        
        # Base persona should be valid
        is_valid = loader.validate_persona_file("personas/base.json")
        assert is_valid is True


class TestLoadPersonaFunction:
    def test_load_persona_function(self):
        """Test the convenience load_persona function."""
        vocab, styles = load_persona("Neon Alien")
        
        assert isinstance(vocab, list)
        assert isinstance(styles, list)
        assert len(vocab) > 0
        assert len(styles) > 0


class TestPersonaVocabLoaderEdgeCases:
    def test_missing_base_persona(self, tmp_path):
        """Test behavior when base persona is missing."""
        loader = PersonaVocabLoader(str(tmp_path))
        
        with pytest.raises(FileNotFoundError):
            loader.load_persona("Any Persona")
    
    def test_list_personas_no_directory(self, tmp_path):
        """Test listing personas when directory doesn't exist."""
        loader = PersonaVocabLoader(str(tmp_path / "nonexistent"))
        personas = loader.list_available_personas()
        
        assert personas == []
    
    def test_validate_invalid_persona_file(self, tmp_path):
        """Test validating an invalid persona file."""
        invalid_file = tmp_path / "invalid.json"
        invalid_file.write_text('{"invalid": "structure"}')
        
        loader = PersonaVocabLoader()
        is_valid = loader.validate_persona_file(str(invalid_file))
        
        assert is_valid is False
    
    def test_validate_nonexistent_file(self, tmp_path):
        """Test validating a nonexistent file."""
        loader = PersonaVocabLoader()
        is_valid = loader.validate_persona_file(str(tmp_path / "nonexistent.json"))
        
        assert is_valid is False
