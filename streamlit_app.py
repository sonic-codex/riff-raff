
import streamlit as st
from generator_core import generate_bars, generate_hook
from vault_manager import save_lyrics, load_lyrics
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Riff Raff Generator", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #FF6B6B;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        text-align: center;
        color: #4A4A4A;
        margin-bottom: 2rem;
    }
    .generated-content {
        background-color: #F8F9FA;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #FF6B6B;
        margin: 1rem 0;
    }
    .download-button {
        background-color: #28A745;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        text-decoration: none;
        display: inline-block;
        margin: 0.5rem;
    }
    .history-item {
        background-color: #E9ECEF;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        border-left: 3px solid #FF6B6B;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'generation_history' not in st.session_state:
    st.session_state.generation_history = []

# Header
st.markdown('<h1 class="main-header">🎤 Riff Raff Lyric Generator</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Build-a-Bar: Surreal Swag Edition</p>', unsafe_allow_html=True)

# Sidebar for controls
with st.sidebar:
    st.header("🎛️ Controls")
    
    persona = st.selectbox(
        "Choose your Persona", 
        ["Neon Alien", "Beach Riff", "Snakeskin Tycoon", "Retro Arcade Savage"],
        help="Select your Riff Raff persona style"
    )
    
    theme = st.selectbox(
        "Theme", 
        ["Fashion", "Flexing", "Snacks", "Sci-Fi", "Random"],
        help="Choose the theme for your lyrics"
    )
    
    mode = st.radio(
        "Mode", 
        ["4-Bar Verse", "Hook Generator"],
        help="Generate a 4-bar verse or a catchy hook"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        flex_level = st.slider("💎 Flex Level", 1, 10, 7, help="How hard you're flexing")
    with col2:
        nonsense = st.slider("🌀 Nonsense Juice", 0, 10, 5, help="Level of surreal randomness")
    
    # Generate button
    if st.button("🎵 Generate", type="primary", use_container_width=True):
        st.session_state.generating = True

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("🎤 Generated Content")
    
    if st.session_state.get('generating', False):
        with st.spinner("Generating your bars..."):
            if mode == "4-Bar Verse":
                generated_text = generate_bars(persona, theme, flex_level, nonsense)
            else:
                generated_text = generate_hook(persona, theme, flex_level, nonsense)
            
            # Store in session state
            st.session_state.current_generation = {
                'text': generated_text,
                'persona': persona,
                'theme': theme,
                'mode': mode,
                'flex_level': flex_level,
                'nonsense': nonsense,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Add to history
            st.session_state.generation_history.append(st.session_state.current_generation.copy())
            st.session_state.generating = False
    
    # Display current generation
    if 'current_generation' in st.session_state:
        st.markdown('<div class="generated-content">', unsafe_allow_html=True)
        st.text_area(
            "Generated Lyrics",
            value=st.session_state.current_generation['text'],
            height=200,
            disabled=True,
            key="display_area"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Download and save buttons
        col_d1, col_d2, col_d3 = st.columns(3)
        
        with col_d1:
            # Download as text file
            st.download_button(
                label="📥 Download TXT",
                data=st.session_state.current_generation['text'],
                file_name=f"riff_raff_{persona.lower().replace(' ', '_')}_{theme.lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
        
        with col_d2:
            # Save to vault
            if st.button("💾 Save to Vault"):
                try:
                    # Load existing lyrics
                    existing_lyrics = load_lyrics()
                    if not isinstance(existing_lyrics, list):
                        existing_lyrics = []
                    
                    # Add new lyrics
                    new_lyric = {
                        'text': st.session_state.current_generation['text'],
                        'persona': persona,
                        'theme': theme,
                        'mode': mode,
                        'flex_level': flex_level,
                        'nonsense': nonsense,
                        'timestamp': datetime.now().isoformat()
                    }
                    existing_lyrics.append(new_lyric)
                    
                    # Save back to file
                    save_lyrics(existing_lyrics)
                    st.success("✅ Saved to vault!")
                except Exception as e:
                    st.error(f"❌ Error saving: {e}")
        
        with col_d3:
            # Copy to clipboard
            if st.button("📋 Copy"):
                st.write("📋 Copied to clipboard!")
                st.code(st.session_state.current_generation['text'])

with col2:
    st.header("📚 Generation History")
    
    if st.session_state.generation_history:
        for i, generation in enumerate(reversed(st.session_state.generation_history[-5:])):  # Show last 5
            with st.expander(f"{generation['timestamp']} - {generation['persona']} ({generation['theme']})"):
                st.text_area(
                    f"{generation['mode']}",
                    value=generation['text'],
                    height=100,
                    disabled=True,
                    key=f"history_{i}"
                )
                st.caption(f"Flex: {generation['flex_level']} | Nonsense: {generation['nonsense']}")
    else:
        st.info("No generation history yet. Generate some bars to see them here!")

# Vault section
st.header("🗄️ Vault")
tab1, tab2 = st.tabs(["Saved Lyrics", "Export Vault"])

with tab1:
    try:
        saved_lyrics = load_lyrics()
        if saved_lyrics and len(saved_lyrics) > 0:
            for i, lyric in enumerate(saved_lyrics):
                with st.expander(f"{lyric.get('timestamp', 'Unknown')} - {lyric.get('persona', 'Unknown')} ({lyric.get('theme', 'Unknown')})"):
                    st.text_area(
                        f"{lyric.get('mode', 'Unknown')}",
                        value=lyric.get('text', ''),
                        height=100,
                        disabled=True,
                        key=f"vault_{i}"
                    )
                    st.caption(f"Flex: {lyric.get('flex_level', 'N/A')} | Nonsense: {lyric.get('nonsense', 'N/A')}")
                    
                    # Delete button
                    if st.button(f"🗑️ Delete", key=f"delete_{i}"):
                        saved_lyrics.pop(i)
                        save_lyrics(saved_lyrics)
                        st.rerun()
        else:
            st.info("No saved lyrics in vault yet. Save some generations to see them here!")
    except Exception as e:
        st.error(f"Error loading vault: {e}")

with tab2:
    try:
        saved_lyrics = load_lyrics()
        if saved_lyrics and len(saved_lyrics) > 0:
            # Export as JSON
            json_data = json.dumps(saved_lyrics, indent=2)
            st.download_button(
                label="📥 Export Vault as JSON",
                data=json_data,
                file_name=f"riff_raff_vault_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
            
            # Export as text
            text_data = ""
            for lyric in saved_lyrics:
                text_data += f"=== {lyric.get('persona', 'Unknown')} - {lyric.get('theme', 'Unknown')} ===\n"
                text_data += f"Mode: {lyric.get('mode', 'Unknown')}\n"
                text_data += f"Flex: {lyric.get('flex_level', 'N/A')} | Nonsense: {lyric.get('nonsense', 'N/A')}\n"
                text_data += f"Timestamp: {lyric.get('timestamp', 'Unknown')}\n\n"
                text_data += lyric.get('text', '') + "\n\n"
            
            st.download_button(
                label="📥 Export Vault as TXT",
                data=text_data,
                file_name=f"riff_raff_vault_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
        else:
            st.info("No lyrics to export. Save some generations first!")
    except Exception as e:
        st.error(f"Error exporting vault: {e}")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>🎤 Built with ❤️ for the Riff Raff community | Generate surreal swag bars and hooks</p>
    </div>
    """, 
    unsafe_allow_html=True
)
