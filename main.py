"""
Book Summary Generator - Main Application
Combines text summary generation, audio narration, and video creation.
"""
import sys
import os
from pathlib import Path
from summary_generator import SummaryGenerator
from audio_generator import AudioGenerator
from video_generator import VideoGenerator


class BookSummaryApp:
    """Main application for generating book summaries with audio and video."""
    
    def __init__(self):
        """Initialize all generators."""
        self.summary_gen = SummaryGenerator()
        self.audio_gen = AudioGenerator()
        self.video_gen = VideoGenerator()
        self.current_summary = None
    
    def run(self):
        """Run the interactive application."""
        print("=" * 60)
        print("     📚 BOOK SUMMARY GENERATOR 📚")
        print("=" * 60)
        print("\nGenerate engaging book summaries with audio narration and video!")
        print()
        
        try:
            # Step 1: Generate text summary
            self.current_summary = self._generate_summary_workflow()
            
            if not self.current_summary:
                print("\nExiting without generating summary.")
                return
            
            # Step 2: Generate audio narration
            audio_path = self._generate_audio_workflow()
            
            if not audio_path:
                print("\nExiting without generating audio.")
                return
            
            # Step 3: Generate video
            video_path = self._generate_video_workflow(audio_path)
            
            if video_path:
                print("\n" + "=" * 60)
                print("✅ SUCCESS! All components generated:")
                print(f"   📝 Summary: {len(self.current_summary.split())} words")
                print(f"   🎵 Audio: {audio_path}")
                print(f"   🎬 Video: {video_path}")
                print("=" * 60)
            
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    def _generate_summary_workflow(self):
        """Handle the summary generation workflow with iterations."""
        print("\n" + "─" * 60)
        print("STEP 1: Generate Book Summary")
        print("─" * 60)
        
        # Get book information
        book_title = input("\nEnter book title: ").strip()
        if not book_title:
            return None
        
        book_author = input("Enter author name (optional, press Enter to skip): ").strip()
        
        print("\nSummary length options:")
        print("  1. Short (150-200 words)")
        print("  2. Medium (300-400 words)")
        print("  3. Long (600-800 words) - recommended for comprehensive detail")
        length_choice = input("Choose length (1-3, default: 3): ").strip() or "3"
        
        length_map = {"1": "short", "2": "medium", "3": "long"}
        summary_length = length_map.get(length_choice, "long")
        
        additional_context = input("\nAny specific focus areas? (optional, press Enter to skip): ").strip()
        
        print("\n⏳ Generating summary...")
        summary = self.summary_gen.generate_summary(
            book_title=book_title,
            book_author=book_author if book_author else None,
            additional_context=additional_context if additional_context else None,
            summary_length=summary_length
        )
        
        print("\n" + "=" * 60)
        print("GENERATED SUMMARY:")
        print("=" * 60)
        print(summary)
        print("=" * 60)
        
        # Iteration loop
        while True:
            print("\nOptions:")
            print("  1. Accept this summary and continue")
            print("  2. Refine the summary")
            print("  3. Start over with a new summary")
            print("  4. Exit")
            
            choice = input("\nYour choice (1-4): ").strip()
            
            if choice == "1":
                return summary
            elif choice == "2":
                refinement = input("\nWhat would you like to change? ").strip()
                if refinement:
                    print("\n⏳ Refining summary...")
                    summary = self.summary_gen.refine_summary(refinement)
                    print("\n" + "=" * 60)
                    print("REFINED SUMMARY:")
                    print("=" * 60)
                    print(summary)
                    print("=" * 60)
            elif choice == "3":
                self.summary_gen.reset()
                return self._generate_summary_workflow()
            elif choice == "4":
                return None
            else:
                print("Invalid choice. Please try again.")
    
    def _generate_audio_workflow(self):
        """Handle the audio generation workflow."""
        print("\n" + "─" * 60)
        print("STEP 2: Generate Audio Narration")
        print("─" * 60)
        
        print("\nAvailable voices:")
        for i, (voice, description) in enumerate(self.audio_gen.list_available_voices().items(), 1):
            print(f"  {i}. {voice}: {description}")
        
        voice_choice = input("\nChoose voice (1-6, default: 5 for 'nova'): ").strip() or "5"
        voice_map = {
            "1": "alloy", "2": "echo", "3": "fable",
            "4": "onyx", "5": "nova", "6": "shimmer"
        }
        voice = voice_map.get(voice_choice, "nova")
        
        print("\nQuality options:")
        print("  1. Standard (tts-1) - faster")
        print("  2. High Quality (tts-1-hd) - better sound")
        quality_choice = input("Choose quality (1-2, default: 1): ").strip() or "1"
        model = "tts-1" if quality_choice == "1" else "tts-1-hd"
        
        filename = input("\nAudio filename (default: narration.mp3): ").strip() or "narration.mp3"
        
        print(f"\n⏳ Generating audio with '{voice}' voice...")
        audio_path = self.audio_gen.generate_audio(
            text=self.current_summary,
            output_filename=filename,
            voice=voice,
            model=model
        )
        
        print(f"✅ Audio generated successfully!")
        return audio_path
    
    def _generate_video_workflow(self, audio_path):
        """Handle the video generation workflow."""
        print("\n" + "─" * 60)
        print("STEP 3: Generate Video")
        print("─" * 60)
        
        image_path = input("\nEnter path to image file (or drag and drop): ").strip()
        
        # Remove quotes if user dragged and dropped
        image_path = image_path.strip('"').strip("'")
        
        if not os.path.exists(image_path):
            print(f"❌ Image file not found: {image_path}")
            skip = input("Skip video generation? (y/n): ").strip().lower()
            if skip == 'y':
                return None
            return self._generate_video_workflow(audio_path)
        
        print("\nAspect ratio options:")
        print("  1. 9:16 (YouTube Shorts / TikTok / Instagram Reels) - default")
        print("  2. 16:9 (Standard YouTube)")
        print("  3. 1:1 (Instagram square)")
        print("  4. 4:5 (Instagram portrait)")
        
        aspect_choice = input("Choose aspect ratio (1-4, default: 1): ").strip() or "1"
        aspect_map = {"1": "9:16", "2": "16:9", "3": "1:1", "4": "4:5"}
        aspect_ratio = aspect_map.get(aspect_choice, "9:16")
        
        filename = input("\nVideo filename (default: book_summary.mp4): ").strip() or "book_summary.mp4"
        
        print(f"\n⏳ Creating video with {aspect_ratio} aspect ratio...")
        video_path = self.video_gen.create_video(
            image_path=image_path,
            audio_path=audio_path,
            output_filename=filename,
            aspect_ratio=aspect_ratio
        )
        
        print(f"✅ Video generated successfully!")
        return video_path


def quick_generate(book_title, book_author=None, image_path=None):
    """
    Quick generation mode - generates everything with default settings.
    
    Args:
        book_title: Title of the book
        book_author: Author of the book (optional)
        image_path: Path to image for video (optional)
    """
    print(f"📚 Quick generating summary for: {book_title}")
    
    app = BookSummaryApp()
    
    # Generate summary
    print("\n⏳ Generating summary...")
    summary = app.summary_gen.generate_summary(
        book_title=book_title,
        book_author=book_author,
        summary_length="long"
    )
    print(f"✅ Summary generated ({len(summary.split())} words)")
    
    # Generate audio
    print("\n⏳ Generating audio...")
    audio_path = app.audio_gen.generate_audio(
        text=summary,
        output_filename=f"{book_title.replace(' ', '_')}_narration.mp3",
        voice="nova"
    )
    print(f"✅ Audio generated: {audio_path}")
    
    # Generate video if image provided
    if image_path and os.path.exists(image_path):
        print("\n⏳ Creating video...")
        video_path = app.video_gen.create_video(
            image_path=image_path,
            audio_path=audio_path,
            output_filename=f"{book_title.replace(' ', '_')}_video.mp4",
            aspect_ratio="9:16"
        )
        print(f"✅ Video generated: {video_path}")
    
    print("\n✅ All done!")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Quick mode from command line
        book_title = sys.argv[1]
        book_author = sys.argv[2] if len(sys.argv) > 2 else None
        image_path = sys.argv[3] if len(sys.argv) > 3 else None
        quick_generate(book_title, book_author, image_path)
    else:
        # Interactive mode
        app = BookSummaryApp()
        app.run()

