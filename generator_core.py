
import random
import json
import os

def load_persona(persona_name):
    """Load persona-specific vocabulary and styles"""
    persona_file = f"personas/{persona_name.lower().replace(' ', '_')}.json"
    base_file = "personas/base.json"
    
    # Load base persona
    with open(base_file, 'r') as f:
        base_data = json.load(f)
    
    # Load specific persona if it exists
    if os.path.exists(persona_file):
        with open(persona_file, 'r') as f:
            persona_data = json.load(f)
        # Merge base and persona-specific vocab
        vocab = base_data['vocab'] + persona_data['vocab']
        styles = base_data['styles'] + persona_data['styles']
    else:
        vocab = base_data['vocab']
        styles = base_data['styles']
    
    return vocab, styles

def get_theme_words(theme):
    """Get theme-specific vocabulary"""
    theme_vocab = {
        "Fashion": ["drip", "flex", "swag", "style", "designer", "couture", "runway", "trend"],
        "Flexing": ["ice", "diamonds", "gold", "luxury", "wealth", "money", "boss", "king"],
        "Snacks": ["gummy bears", "skittles", "candy", "sweets", "treats", "snacks", "food", "munchies"],
        "Sci-Fi": ["laser", "spaceship", "galaxy", "matrix", "cyber", "future", "tech", "alien"],
        "Random": ["random", "wild", "crazy", "insane", "bonkers", "wacky", "nuts", "mad"]
    }
    return theme_vocab.get(theme, theme_vocab["Random"])

def generate_bars(persona, theme, flex, chaos):
    """Generate 4-bar verse with persona and theme influence"""
    vocab, styles = load_persona(persona)
    theme_words = get_theme_words(theme)
    
    # Combine vocab with theme words
    all_vocab = vocab + theme_words
    
    bars = []
    for i in range(4):
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
        theme_objects = {
            "Fashion": ["on the runway", "in the club", "at the show", "in the scene", "on the street"],
            "Flexing": ["in my mansion", "on my wrist", "in my bank", "at the top", "in the game"],
            "Snacks": ["in my mouth", "in my bag", "on my plate", "in my stash", "in my pocket"],
            "Sci-Fi": ["in the matrix", "in space", "in the future", "in cyberspace", "in the galaxy"],
            "Random": ["in the club", "in my trunk", "from the ceiling", "on my wrist", "in the matrix"]
        }
        
        obj = random.choice(theme_objects.get(theme, theme_objects["Random"]))
        
        # Create the bar
        swag = f"My {subject} {verb}s {obj}."
        
        # Add flex level effects
        if flex > 7:
            flex_phrases = ["Yuh!", "Flexed too hard!", "Chromed out DNA!", "Too much sauce!", "Drippin'!"]
            swag += f" {random.choice(flex_phrases)}"
        
        # Add chaos/nonsense effects
        if chaos > 7:
            chaos_phrases = ["What!", "Insane!", "Bonkers!", "Wild!", "Crazy!"]
            swag += f" {random.choice(chaos_phrases)}"
        
        bars.append(swag)
    
    return "\n".join(bars)

def generate_hook(persona, theme, flex, chaos):
    """Generate hook with persona and theme influence"""
    vocab, styles = load_persona(persona)
    theme_words = get_theme_words(theme)
    
    # Persona-specific hook bases
    persona_hooks = {
        "Neon Alien": ["Came through drippin'", "High-waist flex", "Mood ring activated", "Pulled up neon", "Beam me up"],
        "Beach Riff": ["Surf's up", "Beach vibes", "Wave check", "Sand in my shoes", "Ocean breeze"],
        "Snakeskin Tycoon": ["Money moves", "Boss status", "Empire building", "Gold standard", "Luxury life"],
        "Retro Arcade Savage": ["Game over", "High score", "Level up", "Power move", "Arcade king"]
    }
    
    # Theme-specific responses
    theme_responses = {
        "Fashion": ["Michelle Obama", "Skittles and drama", "tuned like Nirvana", "snakes in pajamas", "designer flow"],
        "Flexing": ["money moves", "boss status", "king energy", "flex game", "wealth mode"],
        "Snacks": ["candy crush", "sweet dreams", "sugar rush", "treat yourself", "snack attack"],
        "Sci-Fi": ["matrix mode", "cyber flex", "future vibes", "alien tech", "space age"],
        "Random": ["Michelle Obama", "Skittles and drama", "tuned like Nirvana", "snakes in pajamas"]
    }
    
    # Select hook base and response
    hook_bases = persona_hooks.get(persona, ["Came through drippin'", "High-waist flex", "Mood ring activated", "Pulled up neon"])
    responses = theme_responses.get(theme, theme_responses["Random"])
    
    base = random.choice(hook_bases)
    response = random.choice(responses)
    
    hook = []
    for _ in range(2):
        hook.append(f"{base}... {response}")
    
    # Add flex/chaos effects
    result = "\n".join(hook)
    if flex > 8:
        result += "\nYuh! Flexed too hard!"
    if chaos > 8:
        result += "\nWhat! Insane!"
    
    return result
