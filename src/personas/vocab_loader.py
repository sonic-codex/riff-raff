"""Load & manage persona vocab"""
import os
from pathlib import Path
from typing import Dict, List, Tuple

from src.utils import get_logger, load_json_file


logger = get_logger(__name__)


class PersonaVocabLoader:
    """Load and manage persona-specific vocabulary and styles."""

    def __init__(self, personas_dir: str = "personas"):
        """Initialize the vocab loader.

        Args:
            personas_dir: Directory containing persona JSON files
        """
        self.personas_dir = Path(personas_dir)
        self._cache: Dict[str, Tuple[List[str], List[str]]] = {}

    def load_persona(self, persona_name: str) -> Tuple[List[str], List[str]]:
        """Load persona-specific vocabulary and styles.

        Args:
            persona_name: Name of the persona (e.g., "Neon Alien")

        Returns:
            Tuple of (vocab list, styles list)

        Raises:
            FileNotFoundError: If the base persona file doesn't exist
        """
        # Check cache first
        if persona_name in self._cache:
            logger.debug(f"Loading persona '{persona_name}' from cache")
            return self._cache[persona_name]

        # Load base persona
        base_file = self.personas_dir / "base.json"
        if not base_file.exists():
            raise FileNotFoundError(f"Base persona file not found: {base_file}")

        base_data = load_json_file(str(base_file))
        vocab = base_data.get('vocab', [])
        styles = base_data.get('styles', [])

        # Load specific persona if it exists
        persona_file = self.personas_dir / f"{persona_name.lower().replace(' ', '_')}.json"
        if persona_file.exists():
            logger.info(f"Loading persona-specific vocab from {persona_file}")
            persona_data = load_json_file(str(persona_file))

            # Merge base and persona-specific vocab
            vocab = vocab + persona_data.get('vocab', [])
            styles = styles + persona_data.get('styles', [])
        else:
            logger.warning(f"Persona file not found: {persona_file}, using base only")

        # Cache the result
        result = (vocab, styles)
        self._cache[persona_name] = result

        return result

    def clear_cache(self) -> None:
        """Clear the persona cache."""
        self._cache.clear()
        logger.debug("Persona cache cleared")

    def list_available_personas(self) -> List[str]:
        """List all available personas based on JSON files in the personas directory.

        Returns:
            List of persona names (without .json extension)
        """
        if not self.personas_dir.exists():
            logger.warning(f"Personas directory not found: {self.personas_dir}")
            return []

        personas = []
        for file in self.personas_dir.glob("*.json"):
            if file.stem != "base":
                # Convert filename to persona name (e.g., "neon_alien" -> "Neon Alien")
                persona_name = file.stem.replace('_', ' ').title()
                personas.append(persona_name)

        return sorted(personas)

    def validate_persona_file(self, persona_file: str) -> bool:
        """Validate that a persona file has the required structure.

        Args:
            persona_file: Path to the persona JSON file

        Returns:
            True if valid, False otherwise
        """
        try:
            data = load_json_file(persona_file)

            # Check for required fields
            if 'vocab' not in data or not isinstance(data['vocab'], list):
                logger.error(f"Invalid persona file {persona_file}: missing or invalid 'vocab'")
                return False

            if 'styles' not in data or not isinstance(data['styles'], list):
                logger.error(f"Invalid persona file {persona_file}: missing or invalid 'styles'")
                return False

            return True

        except Exception as e:
            logger.error(f"Error validating persona file {persona_file}: {e}")
            return False


# Convenience function for backward compatibility
def load_persona(persona_name: str, personas_dir: str = "personas") -> Tuple[List[str], List[str]]:
    """Load persona-specific vocabulary and styles.

    This is a convenience function that creates a PersonaVocabLoader and loads the persona.

    Args:
        persona_name: Name of the persona
        personas_dir: Directory containing persona JSON files

    Returns:
        Tuple of (vocab list, styles list)
    """
    loader = PersonaVocabLoader(personas_dir)
    return loader.load_persona(persona_name)
