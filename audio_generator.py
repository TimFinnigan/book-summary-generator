"""
Module for generating audio narration from text using OpenAI's Text-to-Speech API.
"""
import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class AudioGenerator:
    """Handles audio generation using OpenAI's TTS API."""
    
    def __init__(self, output_dir="output"):
        """
        Initialize the audio generator.
        
        Args:
            output_dir: Directory to save generated audio files
        """
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        self.client = OpenAI(api_key=api_key)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_audio(self, text, output_filename="narration.mp3", 
                      voice="alloy", model="tts-1"):
        """
        Generate audio narration from text.
        
        Args:
            text: Text to convert to speech
            output_filename: Name of the output audio file
            voice: Voice to use. Options: alloy, echo, fable, onyx, nova, shimmer
            model: TTS model to use. Options: tts-1 (faster), tts-1-hd (higher quality)
        
        Returns:
            Path to the generated audio file
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        
        # Available voices with descriptions for reference
        voices_info = {
            "alloy": "Neutral and balanced",
            "echo": "Male, clear",
            "fable": "British accent",
            "onyx": "Deep male voice",
            "nova": "Female, energetic",
            "shimmer": "Female, soft"
        }
        
        if voice not in voices_info:
            raise ValueError(f"Invalid voice. Choose from: {', '.join(voices_info.keys())}")
        
        # Ensure output filename has .mp3 extension
        if not output_filename.endswith('.mp3'):
            output_filename += '.mp3'
        
        output_path = self.output_dir / output_filename
        
        print(f"Generating audio with voice '{voice}' ({voices_info[voice]})...")
        
        response = self.client.audio.speech.create(
            model=model,
            voice=voice,
            input=text
        )
        
        # Save the audio file
        response.stream_to_file(str(output_path))
        
        print(f"Audio saved to: {output_path}")
        return str(output_path)
    
    def list_available_voices(self):
        """Return information about available voices."""
        return {
            "alloy": "Neutral and balanced - great for general content",
            "echo": "Male voice, clear and articulate",
            "fable": "British accent - sophisticated tone",
            "onyx": "Deep male voice - authoritative",
            "nova": "Female voice, energetic and engaging",
            "shimmer": "Female voice, soft and gentle"
        }


if __name__ == "__main__":
    # Example usage
    generator = AudioGenerator()
    
    # List available voices
    print("Available voices:")
    for voice, description in generator.list_available_voices().items():
        print(f"  - {voice}: {description}")
    print()
    
    # Generate sample audio
    sample_text = """
    Atomic Habits by James Clear is a groundbreaking guide to building good habits 
    and breaking bad ones. The book introduces a powerful framework based on four laws: 
    make it obvious, make it attractive, make it easy, and make it satisfying. 
    Clear emphasizes that tiny changes can lead to remarkable results when compounded over time.
    """
    
    audio_path = generator.generate_audio(
        text=sample_text,
        output_filename="sample_narration.mp3",
        voice="nova",
        model="tts-1"
    )
    print(f"\nGenerated audio file: {audio_path}")

