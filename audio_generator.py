"""
Module for generating audio narration from text using OpenAI's Text-to-Speech API.
Handles long text by splitting into chunks and combining audio segments.
"""
import os
import re
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
from moviepy.editor import AudioFileClip, concatenate_audioclips

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
    
    def _split_text_into_chunks(self, text, max_chars=4000):
        """
        Split text into chunks at sentence boundaries to stay under character limit.
        OpenAI TTS has a 4096 character limit.
        
        Args:
            text: Text to split
            max_chars: Maximum characters per chunk (default 4000 for safety)
        
        Returns:
            List of text chunks
        """
        # If text is short enough, return as single chunk
        if len(text) <= max_chars:
            return [text]
        
        # Split into sentences (basic sentence splitting)
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            # If a single sentence is too long, we need to split it further
            if len(sentence) > max_chars:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = ""
                # Split long sentence by phrases at commas, semicolons, etc.
                phrases = re.split(r'([,;:])\s+', sentence)
                temp_chunk = ""
                for phrase in phrases:
                    if len(temp_chunk) + len(phrase) <= max_chars:
                        temp_chunk += phrase
                    else:
                        if temp_chunk:
                            chunks.append(temp_chunk.strip())
                        temp_chunk = phrase
                if temp_chunk:
                    chunks.append(temp_chunk.strip())
            # Normal case: add sentence to current chunk
            elif len(current_chunk) + len(sentence) + 1 <= max_chars:
                current_chunk += " " + sentence if current_chunk else sentence
            else:
                chunks.append(current_chunk.strip())
                current_chunk = sentence
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def generate_audio(self, text, output_filename="narration.mp3", 
                      voice="alloy", model="tts-1"):
        """
        Generate audio narration from text.
        Automatically handles long text by splitting into chunks and combining.
        
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
        
        # Split text into chunks if needed
        chunks = self._split_text_into_chunks(text)
        
        if len(chunks) == 1:
            # Simple case: text fits in one request
            print(f"Generating audio with voice '{voice}' ({voices_info[voice]})...")
            response = self.client.audio.speech.create(
                model=model,
                voice=voice,
                input=text
            )
            response.stream_to_file(str(output_path))
            print(f"Audio saved to: {output_path}")
        else:
            # Complex case: need to generate multiple chunks and combine
            print(f"Text is long ({len(text)} chars), splitting into {len(chunks)} chunks...")
            print(f"Generating audio with voice '{voice}' ({voices_info[voice]})...")
            
            # Generate audio for each chunk
            temp_files = []
            for i, chunk in enumerate(chunks, 1):
                print(f"  Processing chunk {i}/{len(chunks)}...")
                temp_filename = f"temp_chunk_{i}_{output_filename}"
                temp_path = self.output_dir / temp_filename
                
                response = self.client.audio.speech.create(
                    model=model,
                    voice=voice,
                    input=chunk
                )
                response.stream_to_file(str(temp_path))
                temp_files.append(str(temp_path))
            
            # Combine all audio chunks
            print(f"  Combining {len(chunks)} audio segments...")
            audio_clips = [AudioFileClip(f) for f in temp_files]
            final_audio = concatenate_audioclips(audio_clips)
            final_audio.write_audiofile(str(output_path), codec='mp3', logger=None)
            
            # Clean up
            final_audio.close()
            for clip in audio_clips:
                clip.close()
            
            # Remove temporary files
            for temp_file in temp_files:
                try:
                    os.remove(temp_file)
                except:
                    pass
            
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

