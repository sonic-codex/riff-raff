"""Shared utilities (logging, config loader)"""
import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the specified name.

    Args:
        name: Name for the logger (typically __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(name)


def load_json_file(file_path: str) -> Dict[str, Any]:
    """Load a JSON file and return its contents.

    Args:
        file_path: Path to the JSON file

    Returns:
        Dictionary containing the JSON data

    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
    """
    logger = get_logger(__name__)
    path = Path(file_path)

    if not path.exists():
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.debug(f"Successfully loaded JSON from {file_path}")
        return data
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {file_path}: {e}")
        raise


def save_json_file(data: Dict[str, Any], file_path: str, indent: int = 2) -> None:
    """Save data to a JSON file.

    Args:
        data: Dictionary to save as JSON
        file_path: Path where the JSON file should be saved
        indent: Number of spaces for indentation (default: 2)
    """
    logger = get_logger(__name__)
    path = Path(file_path)

    # Create directory if it doesn't exist
    path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
        logger.debug(f"Successfully saved JSON to {file_path}")
    except Exception as e:
        logger.error(f"Error saving JSON to {file_path}: {e}")
        raise


def ensure_directory_exists(directory: str) -> Path:
    """Ensure a directory exists, creating it if necessary.

    Args:
        directory: Path to the directory

    Returns:
        Path object for the directory
    """
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    return path


def validate_range(value: int, min_val: int, max_val: int, name: str) -> int:
    """Validate that a value is within a specified range.

    Args:
        value: Value to validate
        min_val: Minimum allowed value (inclusive)
        max_val: Maximum allowed value (inclusive)
        name: Name of the parameter (for error messages)

    Returns:
        The validated value

    Raises:
        ValueError: If the value is outside the allowed range
    """
    if not min_val <= value <= max_val:
        raise ValueError(f"{name} must be between {min_val} and {max_val}, got {value}")
    return value


def sanitize_filename(filename: str, max_length: int = 255) -> str:
    """Sanitize a filename by removing invalid characters.

    Args:
        filename: Original filename
        max_length: Maximum length for the filename (default: 255)

    Returns:
        Sanitized filename safe for most filesystems
    """
    # Replace invalid characters with underscores
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')

    # Remove any leading/trailing whitespace or dots
    filename = filename.strip('. ')

    # Truncate if too long
    if len(filename) > max_length:
        filename = filename[:max_length]

    # Ensure we have a valid filename
    if not filename:
        filename = "untitled"

    return filename


class Config:
    """Configuration manager for the application."""

    _instance: Optional['Config'] = None
    _config: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def load_config(self, config_path: str = "config.json") -> None:
        """Load configuration from a JSON file.

        Args:
            config_path: Path to the configuration file
        """
        try:
            self._config = load_json_file(config_path)
        except FileNotFoundError:
            # Use default configuration if file doesn't exist
            self._config = self._get_default_config()

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value.

        Args:
            key: Configuration key (supports dot notation, e.g., "app.name")
            default: Default value if key doesn't exist

        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self._config

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default

            if value is None:
                return default

        return value

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value.

        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
        """
        keys = key.split('.')
        config = self._config

        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value

    @staticmethod
    def _get_default_config() -> Dict[str, Any]:
        """Get default configuration values.

        Returns:
            Dictionary containing default configuration
        """
        return {
            "app": {
                "name": "Riff Raff Generator",
                "version": "1.0.0"
            },
            "paths": {
                "data": "data",
                "personas": "personas",
                "saved_lyrics": "data/saved_lyrics.json"
            },
            "generation": {
                "default_flex_level": 7,
                "default_nonsense_juice": 5,
                "max_flex_level": 10,
                "max_nonsense_juice": 10
            }
        }
