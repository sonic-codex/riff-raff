"""Prompt templates & model calls for lyric generation"""
import random
from typing import List, Optional

from src.lyrics.utils import (
    get_chaos_phrases,
    get_flex_phrases,
    get_persona_hooks,
    get_theme_objects,
    get_theme_responses,
    get_theme_words,
)
from src.personas.vocab_loader import load_persona
from src.utils import get_logger

logger = get_logger(__name__)


class LyricGenerator:
    """Generator for Riff Raff style lyrics and hooks."""

    def __init__(self, personas_dir: str = "personas"):
        """Initialize the lyric generator.

        Args:
            personas_dir: Directory containing persona JSON files
        """
        self.personas_dir = personas_dir

    def generate_bars(
        self,
        persona: str,
        theme: str,
        flex: int = 7,
        chaos: int = 5,
        num_bars: int = 4
    ) -> str:
        """Generate verse bars with persona and theme influence.

        Args:
            persona: Persona name (e.g., "Neon Alien")
            theme: Theme name (e.g., "Fashion")
            flex: Flex level (1-10)
            chaos: Nonsense juice level (0-10)
            num_bars: Number of bars to generate (default: 4)

        Returns:
            Generated bars as a string with newlines between bars
        """
        logger.info(f"Generating {num_bars} bars with persona={persona}, theme={theme}")

        vocab, styles = load_persona(persona, self.personas_dir)
        theme_words = get_theme_words(theme)

        # Combine vocab with theme words
        all_vocab = vocab + theme_words

        bars = []
        for i in range(num_bars):
            # Select subject with persona/theme bias
            if random.random() < 0.7:  # 70% chance to use persona/theme vocab
                subject = random.choice(all_vocab)
            else:
                subject = random.choice(vocab)

            # Select verb with persona style bias
            if random.random() < 0.6:  # 60% chance to use persona styles
                verb = random.choice(styles)
            else:
                verb = random.choice(["glow", "drip", "hiss", "teleport", "breathe", "bounce"])

            # Theme-specific objects
            obj = random.choice(get_theme_objects(theme))

            # Create the bar
            bar = f"My {subject} {verb}s {obj}."

            # Add flex level effects
            if flex > 7:
                flex_phrases = get_flex_phrases(flex)
                bar += f" {random.choice(flex_phrases)}"

            # Add chaos/nonsense effects
            if chaos > 7:
                chaos_phrases = get_chaos_phrases(chaos)
                bar += f" {random.choice(chaos_phrases)}"

            bars.append(bar)

        return "\n".join(bars)

    def generate_hook(
        self,
        persona: str,
        theme: str,
        flex: int = 7,
        chaos: int = 5,
        num_repeats: int = 2
    ) -> str:
        """Generate hook with persona and theme influence.

        Args:
            persona: Persona name
            theme: Theme name
            flex: Flex level (1-10)
            chaos: Nonsense juice level (0-10)
            num_repeats: Number of times to repeat the hook pattern (default: 2)

        Returns:
            Generated hook as a string
        """
        logger.info(f"Generating hook with persona={persona}, theme={theme}")

        # Get persona-specific hook bases
        hook_bases = get_persona_hooks(persona)

        # Get theme-specific responses
        responses = get_theme_responses(theme)

        # Select hook base and response
        base = random.choice(hook_bases)
        response = random.choice(responses)

        hook = []
        for _ in range(num_repeats):
            hook.append(f"{base}... {response}")

        # Add flex/chaos effects
        result = "\n".join(hook)
        if flex > 8:
            result += f"\n{random.choice(get_flex_phrases(flex))}"
        if chaos > 8:
            result += f"\n{random.choice(get_chaos_phrases(chaos))}"

        return result

    def generate(
        self,
        persona: str,
        theme: str,
        mode: str = "4-Bar Verse",
        flex: int = 7,
        chaos: int = 5
    ) -> str:
        """Generate lyrics based on mode.

        Args:
            persona: Persona name
            theme: Theme name
            mode: Generation mode ("4-Bar Verse" or "Hook Generator")
            flex: Flex level (1-10)
            chaos: Nonsense juice level (0-10)

        Returns:
            Generated lyrics

        Raises:
            ValueError: If mode is invalid
        """
        if mode == "4-Bar Verse":
            return self.generate_bars(persona, theme, flex, chaos)
        elif mode == "Hook Generator":
            return self.generate_hook(persona, theme, flex, chaos)
        else:
            raise ValueError(f"Invalid mode: {mode}. Must be '4-Bar Verse' or 'Hook Generator'")


# Convenience functions for backward compatibility with generator_core.py
def generate_bars(persona: str, theme: str, flex: int, chaos: int) -> str:
    """Generate 4-bar verse with persona and theme influence.

    Args:
        persona: Persona name
        theme: Theme name
        flex: Flex level
        chaos: Nonsense juice level

    Returns:
        Generated bars
    """
    generator = LyricGenerator()
    return generator.generate_bars(persona, theme, flex, chaos)


def generate_hook(persona: str, theme: str, flex: int, chaos: int) -> str:
    """Generate hook with persona and theme influence.

    Args:
        persona: Persona name
        theme: Theme name
        flex: Flex level
        chaos: Nonsense juice level

    Returns:
        Generated hook
    """
    generator = LyricGenerator()
    return generator.generate_hook(persona, theme, flex, chaos)
