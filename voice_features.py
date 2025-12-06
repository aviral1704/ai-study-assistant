"""
Voice Interaction Features
- Text-to-Speech for reading summaries
- Speech-to-Text for asking questions
- Audio explanations
"""

import os
from pathlib import Path

try:
    from gtts import gTTS
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False

try:
    import speech_recognition as sr
    STT_AVAILABLE = True
except ImportError:
    STT_AVAILABLE = False


class VoiceAssistant:
    """Voice interaction for hands-free learning."""
    
    def __init__(self):
        self.audio_dir = Path(".audio_cache")
        self.audio_dir.mkdir(exist_ok=True)
        self.recognizer = sr.Recognizer() if STT_AVAILABLE else None
    
    def text_to_speech(self, text: str, filename: str = "output.mp3", lang: str = "en") -> str:
        """Convert text to speech and save as audio file."""
        if not TTS_AVAILABLE:
            return None
        
        try:
            # Create audio file
            audio_path = self.audio_dir / filename
            tts = gTTS(text=text, lang=lang, slow=False)
            tts.save(str(audio_path))
            return str(audio_path)
        except Exception as e:
            print(f"TTS Error: {e}")
            return None
    
    def speech_to_text(self, audio_source=None) -> str:
        """Convert speech to text."""
        if not STT_AVAILABLE:
            return "Speech recognition not available"
        
        try:
            with sr.Microphone() as source:
                print("🎤 Listening... Speak now!")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
                print("🤔 Processing...")
                text = self.recognizer.recognize_google(audio)
                return text
        except sr.WaitTimeoutError:
            return "No speech detected. Please try again."
        except sr.UnknownValueError:
            return "Could not understand audio. Please speak clearly."
        except sr.RequestError as e:
            return f"Speech recognition error: {e}"
        except Exception as e:
            return f"Error: {e}"
    
    def read_summary(self, summary: str) -> str:
        """Read a summary aloud."""
        # Split into chunks if too long
        max_length = 5000
        if len(summary) > max_length:
            chunks = [summary[i:i+max_length] for i in range(0, len(summary), max_length)]
            audio_files = []
            for i, chunk in enumerate(chunks):
                audio_file = self.text_to_speech(chunk, f"summary_part_{i}.mp3")
                if audio_file:
                    audio_files.append(audio_file)
            return audio_files
        else:
            return [self.text_to_speech(summary, "summary.mp3")]
    
    def create_audio_flashcard(self, concept: str, definition: str) -> str:
        """Create audio flashcard."""
        text = f"Concept: {concept}. Definition: {definition}"
        return self.text_to_speech(text, f"flashcard_{concept[:20]}.mp3")


def get_voice_commands() -> dict:
    """Get available voice commands."""
    return {
        "summarize": "Get document summary",
        "explain": "Explain a concept",
        "question": "Ask a question",
        "quiz": "Start a quiz",
        "read": "Read current content",
        "next": "Next section",
        "previous": "Previous section",
        "repeat": "Repeat last response",
        "help": "Show help"
    }
