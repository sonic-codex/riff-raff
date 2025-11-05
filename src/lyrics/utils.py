"""Preprocessing, post-processing for lyrics"""
import re
from typing import Dict, List

from src.utils import get_logger

logger = get_logger(__name__)


def get_theme_words(theme: str) -> List[str]:
    """Get theme-specific vocabulary.

    Args:
        theme: Theme name (Fashion, Flexing, Snacks, Sci-Fi, Random)

    Returns:
        List of theme-specific words
    """
    theme_vocab = {
        "Fashion": [
            "drip", "flex", "swag", "style", "designer", "couture",
            "runway", "trend", "threads", "fit", "outfit", "look"
        ],
        "Flexing": [
            "ice", "diamonds", "gold", "luxury", "wealth", "money",
            "boss", "king", "crown", "throne", "empire", "platinum"
        ],
        "Snacks": [
            "gummy bears", "skittles", "candy", "sweets", "treats",
            "snacks", "food", "munchies", "sugar", "chocolate", "cookies"
        ],
        "Sci-Fi": [
            "laser", "spaceship", "galaxy", "matrix", "cyber", "future",
            "tech", "alien", "robot", "hologram", "warp", "quantum"
        ],
        "Random": [
            "random", "wild", "crazy", "insane", "bonkers", "wacky",
            "nuts", "mad", "chaos", "weird", "bizarre", "strange"
        ]
    }
    return theme_vocab.get(theme, theme_vocab["Random"])


def get_theme_objects(theme: str) -> List[str]:
    """Get theme-specific objects/locations for bars.

    Args:
        theme: Theme name

    Returns:
        List of theme-appropriate objects/locations
    """
    theme_objects = {
        "Fashion": [
            "on the runway", "in the club", "at the show", "in the scene",
            "on the street", "in the mirror", "at the party", "on the gram"
        ],
        "Flexing": [
            "in my mansion", "on my wrist", "in my bank", "at the top",
            "in the game", "on my neck", "in my garage", "at the club"
        ],
        "Snacks": [
            "in my mouth", "in my bag", "on my plate", "in my stash",
            "in my pocket", "on the table", "in the fridge", "in the jar"
        ],
        "Sci-Fi": [
            "in the matrix", "in space", "in the future", "in cyberspace",
            "in the galaxy", "on Mars", "in the simulation", "through time"
        ],
        "Random": [
            "in the club", "in my trunk", "from the ceiling", "on my wrist",
            "in the matrix", "at the zoo", "in the clouds", "underwater"
        ]
    }
    return theme_objects.get(theme, theme_objects["Random"])


def get_persona_hooks(persona: str) -> List[str]:
    """Get persona-specific hook bases.

    Args:
        persona: Persona name

    Returns:
        List of hook opening phrases for this persona
    """
    persona_hooks = {
        "Neon Alien": [
            "Came through drippin'", "High-waist flex", "Mood ring activated",
            "Pulled up neon", "Beam me up", "Chrome everything"
        ],
        "Beach Riff": [
            "Surf's up", "Beach vibes", "Wave check", "Sand in my shoes",
            "Ocean breeze", "Tidal wave", "Shoreline flex"
        ],
        "Snakeskin Tycoon": [
            "Money moves", "Boss status", "Empire building", "Gold standard",
            "Luxury life", "CEO flow", "Diamond district"
        ],
        "Retro Arcade Savage": [
            "Game over", "High score", "Level up", "Power move",
            "Arcade king", "Combo breaker", "Extra life"
        ]
    }
    return persona_hooks.get(persona, [
        "Came through drippin'", "High-waist flex",
        "Mood ring activated", "Pulled up neon"
    ])


def get_theme_responses(theme: str) -> List[str]:
    """Get theme-specific hook responses.

    Args:
        theme: Theme name

    Returns:
        List of theme-appropriate responses
    """
    theme_responses = {
        "Fashion": [
            "Michelle Obama", "Skittles and drama", "tuned like Nirvana",
            "snakes in pajamas", "designer flow", "runway mode"
        ],
        "Flexing": [
            "money moves", "boss status", "king energy", "flex game",
            "wealth mode", "platinum style", "diamond dreams"
        ],
        "Snacks": [
            "candy crush", "sweet dreams", "sugar rush", "treat yourself",
            "snack attack", "gummy bear gang", "skittle squad"
        ],
        "Sci-Fi": [
            "matrix mode", "cyber flex", "future vibes", "alien tech",
            "space age", "laser beams", "quantum leap"
        ],
        "Random": [
            "Michelle Obama", "Skittles and drama", "tuned like Nirvana",
            "snakes in pajamas", "absolute chaos", "wild energy"
        ]
    }
    return theme_responses.get(theme, theme_responses["Random"])


def get_flex_phrases(level: int = 7) -> List[str]:
    """Get flex-appropriate phrases based on flex level.

    Args:
        level: Flex level (1-10)

    Returns:
        List of flex phrases
    """
    if level <= 3:
        return ["Nice.", "Cool.", "Yeah.", "Uh-huh."]
    elif level <= 6:
        return ["Flexin'!", "Drippin'!", "Sauce!", "Swag!"]
    else:
        return [
            "Yuh!", "Flexed too hard!", "Chromed out DNA!",
            "Too much sauce!", "Drippin'!", "Versace everything!"
        ]


def get_chaos_phrases(level: int = 5) -> List[str]:
    """Get chaos/nonsense phrases based on nonsense juice level.

    Args:
        level: Nonsense juice level (0-10)

    Returns:
        List of chaos phrases
    """
    if level <= 3:
        return ["Cool.", "Nice.", "Yep."]
    elif level <= 6:
        return ["What!", "Yo!", "Huh!", "Crazy!"]
    else:
        return [
            "What!", "Insane!", "Bonkers!", "Wild!", "Crazy!",
            "Absolute madness!", "No way!", "Unreal!"
        ]


def clean_lyric_text(text: str) -> str:
    """Clean and normalize lyric text.

    Args:
        text: Raw lyric text

    Returns:
        Cleaned lyric text
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove leading/trailing whitespace
    text = text.strip()
    # Ensure proper sentence endings
    text = re.sub(r'([.!?])\s*([A-Z])', r'\1 \2', text)
    return text


def format_bar_output(bars: List[str]) -> str:
    """Format a list of bars into a single output string.

    Args:
        bars: List of bar strings

    Returns:
        Formatted output with bars on separate lines
    """
    return "\n".join(bars)


def parse_generation_params(params: Dict) -> Dict:
    """Parse and validate generation parameters.

    Args:
        params: Dictionary of generation parameters

    Returns:
        Validated and normalized parameters

    Raises:
        ValueError: If parameters are invalid
    """
    from src.utils import validate_range

    validated = {}

    # Validate flex level
    if 'flex_level' in params:
        validated['flex_level'] = validate_range(
            params['flex_level'], 1, 10, "flex_level"
        )

    # Validate nonsense juice
    if 'nonsense' in params:
        validated['nonsense'] = validate_range(
            params['nonsense'], 0, 10, "nonsense"
        )

    # Pass through other params
    for key in ['persona', 'theme', 'mode']:
        if key in params:
            validated[key] = params[key]

    return validated
