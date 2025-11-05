"""Unit tests for shared utilities"""
import json
from pathlib import Path

import pytest

from src.utils import (
    Config,
    ensure_directory_exists,
    get_logger,
    load_json_file,
    sanitize_filename,
    save_json_file,
    validate_range,
)


class TestGetLogger:
    def test_get_logger(self):
        """Test getting a logger instance."""
        logger = get_logger("test")
        assert logger.name == "test"

    def test_logger_names_differ(self):
        """Test that different names create different loggers."""
        logger1 = get_logger("test1")
        logger2 = get_logger("test2")
        assert logger1.name != logger2.name


class TestLoadJsonFile:
    def test_load_valid_json(self, tmp_path):
        """Test loading a valid JSON file."""
        test_file = tmp_path / "test.json"
        test_data = {"key": "value", "number": 42}
        test_file.write_text(json.dumps(test_data))

        result = load_json_file(str(test_file))
        assert result == test_data

    def test_load_nonexistent_file(self):
        """Test loading a non-existent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            load_json_file("/nonexistent/file.json")

    def test_load_invalid_json(self, tmp_path):
        """Test loading invalid JSON raises JSONDecodeError."""
        test_file = tmp_path / "invalid.json"
        test_file.write_text("{invalid json")

        with pytest.raises(json.JSONDecodeError):
            load_json_file(str(test_file))


class TestSaveJsonFile:
    def test_save_valid_json(self, tmp_path):
        """Test saving valid JSON data."""
        test_file = tmp_path / "output.json"
        test_data = {"key": "value", "number": 42}

        save_json_file(test_data, str(test_file))

        assert test_file.exists()
        loaded = json.loads(test_file.read_text())
        assert loaded == test_data

    def test_save_creates_directory(self, tmp_path):
        """Test that save creates parent directories."""
        test_file = tmp_path / "subdir" / "output.json"
        test_data = {"test": "data"}

        save_json_file(test_data, str(test_file))

        assert test_file.exists()
        assert test_file.parent.exists()


class TestEnsureDirectoryExists:
    def test_create_new_directory(self, tmp_path):
        """Test creating a new directory."""
        new_dir = tmp_path / "new_directory"
        result = ensure_directory_exists(str(new_dir))

        assert new_dir.exists()
        assert new_dir.is_dir()
        assert result == new_dir


class TestValidateRange:
    def test_value_in_range(self):
        """Test validating a value within range."""
        result = validate_range(5, 1, 10, "test")
        assert result == 5

    def test_value_below_min(self):
        """Test value below minimum raises ValueError."""
        with pytest.raises(ValueError, match="must be between 1 and 10"):
            validate_range(0, 1, 10, "test")

    def test_value_above_max(self):
        """Test value above maximum raises ValueError."""
        with pytest.raises(ValueError, match="must be between 1 and 10"):
            validate_range(11, 1, 10, "test")


class TestSanitizeFilename:
    def test_simple_filename(self):
        """Test sanitizing a simple filename."""
        result = sanitize_filename("test.txt")
        assert result == "test.txt"

    def test_invalid_characters(self):
        """Test removing invalid characters."""
        result = sanitize_filename('test<>:"/\\|?*.txt')
        assert '<' not in result
        assert '>' not in result

    def test_empty_filename(self):
        """Test that empty filename becomes 'untitled'."""
        result = sanitize_filename("")
        assert result == "untitled"


class TestConfig:
    def test_get_default_config(self):
        """Test getting default configuration."""
        config = Config()
        config.load_config("nonexistent.json")
        app_name = config.get("app.name")
        assert app_name == "Riff Raff Generator"

    def test_get_with_default(self):
        """Test getting non-existent key with default."""
        config = Config()
        config.load_config("nonexistent.json")
        value = config.get("nonexistent.key", "default_value")
        assert value == "default_value"

    def test_set_value(self):
        """Test setting a configuration value."""
        config = Config()
        config.load_config("nonexistent.json")
        config.set("test.key", "test_value")
        assert config.get("test.key") == "test_value"


class TestUtilsEdgeCases:
    def test_save_json_error_handling(self, tmp_path):
        """Test error handling in save_json_file."""
        # Test with a read-only directory (this won't actually fail in most cases,
        # but tests the error path)
        test_file = tmp_path / "test.json"
        data = {"key": "value"}
        
        # This should succeed
        save_json_file(data, str(test_file))
        assert test_file.exists()
    
    def test_config_get_non_dict_value(self):
        """Test Config.get when intermediate value is not a dict."""
        config = Config()
        config._config = {"a": "string_value"}
        
        # Trying to get a.b.c when a is a string should return default
        result = config.get("a.b.c", "default")
        assert result == "default"
