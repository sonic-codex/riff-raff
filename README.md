# Riff Raff Generator 🎤

This is a surreal freestyle hook and bar generator in the spirit of RiFF RAFF & Lil Debbie.
Built with Python + Streamlit for use in GitHub Codespaces or locally.

## ✨ Features

- **4 Personas**: Neon Alien, Beach Riff, Snakeskin Tycoon, Retro Arcade Savage
- **5 Themes**: Fashion, Flexing, Snacks, Sci-Fi, Random
- **2 Modes**: 4-Bar Verse Generator & Hook Generator
- **Customizable**: Adjustable "Flex Level" & "Nonsense Juice"
- **Smart Generation**: Persona-specific vocabulary and theme influence
- **Vault System**: Save, load, and export your generated lyrics
- **Download Options**: Export as TXT or JSON files
- **Generation History**: Track your recent creations
- **Modern UI**: Beautiful Streamlit interface with custom styling

## 🚀 Quick Start

### Option 1: Using the startup script (Recommended)
```bash
./start.sh
```

### Option 2: Manual setup
```bash
# Create and activate a Python virtual environment
python3 -m venv env
source env/bin/activate

# Install project dependencies
pip install -r requirements.txt

# Run the application
streamlit run streamlit_app.py
```

## 🎛️ How to Use

1. **Choose your Persona**: Select from 4 unique Riff Raff personas
2. **Pick a Theme**: Choose from 5 different thematic styles
3. **Select Mode**: Generate either 4-bar verses or catchy hooks
4. **Adjust Settings**: 
   - 💎 **Flex Level**: How hard you're flexing (1-10)
   - 🌀 **Nonsense Juice**: Level of surreal randomness (0-10)
5. **Generate**: Click the generate button to create your bars
6. **Save & Export**: Download as text files or save to your vault

## 🗄️ Vault System

- **Save Lyrics**: Store your favorite generations in the vault
- **View History**: Browse your saved lyrics with metadata
- **Export Options**: Download your entire vault as JSON or TXT
- **Delete Entries**: Remove unwanted lyrics from your vault

## 🎨 Personas & Themes

### Personas
- **Neon Alien**: Space-age vocabulary with futuristic themes
- **Beach Riff**: Surf and beach culture with laid-back vibes
- **Snakeskin Tycoon**: Luxury and wealth-focused content
- **Retro Arcade Savage**: Gaming and arcade-inspired lyrics

### Themes
- **Fashion**: Designer brands, runway, and style
- **Flexing**: Wealth, luxury, and status
- **Snacks**: Candy, treats, and food references
- **Sci-Fi**: Technology, space, and futuristic elements
- **Random**: Wild and unpredictable combinations

## 📁 Project Structure

```
riff-raff/
├── streamlit_app.py          # Main Streamlit application
├── generator_core.py         # Core generation logic
├── vault_manager.py          # Save/load functionality
├── requirements.txt          # Python dependencies
├── streamlit.toml           # Streamlit configuration
├── start.sh                 # Quick startup script
├── personas/                # Persona definitions
│   ├── base.json
│   ├── neon_alien.json
│   ├── beach_riff.json
│   └── snakeskin_tycoon.json
└── data/                    # Data storage
    └── saved_lyrics.json
```

## 🛠️ Development

The generator uses a sophisticated system that:
- Loads persona-specific vocabulary and styles
- Applies theme-specific word selection
- Combines base and persona vocabularies
- Uses weighted randomization for natural variation
- Applies flex level and nonsense juice effects

## 🌐 Deployment

The app is ready for deployment on:
- **Streamlit Cloud**: Direct deployment from GitHub
- **GitHub Codespaces**: Run in browser with full IDE
- **Local Development**: Run on your machine
- **Docker**: Containerized deployment (coming soon)

## 📝 License

This project is open source and available under the MIT License.

---

🎤 **Ready to generate some surreal swag bars?** Start the app and let the Riff Raff magic flow! 🚀
