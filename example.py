"""
Example usage of the Book Summary Generator
This demonstrates how to use each module individually.
"""
from summary_generator import SummaryGenerator
from audio_generator import AudioGenerator
from video_generator import VideoGenerator


def example_summary_generation():
    """Example: Generate and refine a book summary."""
    print("=" * 60)
    print("EXAMPLE 1: Summary Generation with Iteration")
    print("=" * 60)
    
    generator = SummaryGenerator()
    
    # Generate initial summary
    print("\n1️⃣ Generating initial summary...")
    summary = generator.generate_summary(
        book_title="The 7 Habits of Highly Effective People",
        book_author="Stephen Covey",
        summary_length="long"
    )
    print("\nInitial Summary:")
    print(summary)
    
    # Refine the summary
    print("\n2️⃣ Refining to be more concise...")
    refined = generator.refine_summary(
        "Make this more concise and focus specifically on the 7 habits themselves"
    )
    print("\nRefined Summary:")
    print(refined)
    
    # Further refinement
    print("\n3️⃣ Adding more engaging tone...")
    final = generator.refine_summary(
        "Make the language more engaging and conversational, as if explaining to a friend"
    )
    print("\nFinal Summary:")
    print(final)
    
    return final


def example_audio_generation(text):
    """Example: Generate audio with different voices."""
    print("\n\n" + "=" * 60)
    print("EXAMPLE 2: Audio Generation")
    print("=" * 60)
    
    generator = AudioGenerator()
    
    # List available voices
    print("\nAvailable voices:")
    for voice, description in generator.list_available_voices().items():
        print(f"  • {voice}: {description}")
    
    # Generate audio with different voices
    print("\n🎵 Generating audio with 'nova' voice (energetic female)...")
    audio_path = generator.generate_audio(
        text=text,
        output_filename="example_nova.mp3",
        voice="nova",
        model="tts-1"
    )
    print(f"✅ Audio saved to: {audio_path}")
    
    return audio_path


def example_video_generation(audio_path):
    """Example: Create video (requires an image)."""
    print("\n\n" + "=" * 60)
    print("EXAMPLE 3: Video Generation")
    print("=" * 60)
    
    generator = VideoGenerator()
    
    print("\nTo create a video, you need:")
    print("  1. An audio file (✅ we have this)")
    print("  2. An image file (you'll need to provide this)")
    print("\nExample code:")
    print("""
    generator = VideoGenerator()
    video_path = generator.create_video(
        image_path="your_book_cover.jpg",
        audio_path="output/example_nova.mp3",
        output_filename="example_video.mp4",
        aspect_ratio="9:16"  # YouTube Shorts format
    )
    """)
    
    print("\nSupported aspect ratios:")
    print("  • 9:16 - YouTube Shorts, TikTok, Instagram Reels")
    print("  • 16:9 - Standard YouTube")
    print("  • 1:1 - Instagram square")
    print("  • 4:5 - Instagram portrait")


def main():
    """Run all examples."""
    print("\n")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║       📚 BOOK SUMMARY GENERATOR - EXAMPLES 📚             ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    
    try:
        # Example 1: Summary generation with iteration
        summary = example_summary_generation()
        
        # Example 2: Audio generation
        audio_path = example_audio_generation(summary)
        
        # Example 3: Video generation (explanation only)
        example_video_generation(audio_path)
        
        print("\n\n" + "=" * 60)
        print("✅ EXAMPLES COMPLETED!")
        print("=" * 60)
        print("\nCheck the 'output/' folder for generated files.")
        print("\nTo run the full interactive app, use: python main.py")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you have:")
        print("  1. Created a .env file with OPENAI_API_KEY")
        print("  2. Installed dependencies: pip install -r requirements.txt")


if __name__ == "__main__":
    main()

