"""
Module for generating videos by combining images with audio narration.
Optimized for YouTube Shorts (9:16 aspect ratio).
"""
import os
from pathlib import Path
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip
from PIL import Image


class VideoGenerator:
    """Handles video generation by combining images with audio."""
    
    def __init__(self, output_dir="output"):
        """
        Initialize the video generator.
        
        Args:
            output_dir: Directory to save generated video files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def create_video(self, image_path, audio_path, output_filename="book_summary.mp4",
                    aspect_ratio="9:16", fps=24):
        """
        Create a video by combining an image with audio.
        
        Args:
            image_path: Path to the image file
            audio_path: Path to the audio file
            output_filename: Name of the output video file
            aspect_ratio: Video aspect ratio. Options: "9:16" (YouTube Shorts), 
                         "16:9" (standard), "1:1" (square)
            fps: Frames per second for the video
        
        Returns:
            Path to the generated video file
        """
        # Validate inputs
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        # Ensure output filename has .mp4 extension
        if not output_filename.endswith('.mp4'):
            output_filename += '.mp4'
        
        output_path = self.output_dir / output_filename
        
        print(f"Creating video with {aspect_ratio} aspect ratio...")
        
        # Load audio to get duration
        audio_clip = AudioFileClip(audio_path)
        duration = audio_clip.duration
        
        # Get target dimensions based on aspect ratio
        target_width, target_height = self._get_dimensions(aspect_ratio)
        
        # Process image to fit aspect ratio
        processed_image_path = self._process_image(image_path, target_width, target_height)
        
        # Create image clip with duration matching audio
        image_clip = ImageClip(processed_image_path, duration=duration)
        
        # Combine image and audio
        video_clip = image_clip.set_audio(audio_clip)
        
        # Write the video file
        print(f"Rendering video... (this may take a moment)")
        video_clip.write_videofile(
            str(output_path),
            fps=fps,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True,
            logger=None  # Reduce verbosity
        )
        
        # Clean up
        video_clip.close()
        audio_clip.close()
        
        # Remove temporary processed image if it was created
        if processed_image_path != image_path:
            try:
                os.remove(processed_image_path)
            except:
                pass
        
        print(f"Video saved to: {output_path}")
        return str(output_path)
    
    def _get_dimensions(self, aspect_ratio):
        """Get target dimensions for the given aspect ratio."""
        dimensions = {
            "9:16": (1080, 1920),  # YouTube Shorts / TikTok / Instagram Reels
            "16:9": (1920, 1080),  # Standard YouTube
            "1:1": (1080, 1080),   # Instagram square
            "4:5": (1080, 1350),   # Instagram portrait
        }
        
        if aspect_ratio not in dimensions:
            raise ValueError(f"Invalid aspect ratio. Choose from: {', '.join(dimensions.keys())}")
        
        return dimensions[aspect_ratio]
    
    def _process_image(self, image_path, target_width, target_height):
        """
        Process image to fit the target dimensions.
        Uses smart cropping to maintain aspect ratio.
        """
        img = Image.open(image_path)
        img_width, img_height = img.size
        
        # Calculate aspect ratios
        target_ratio = target_width / target_height
        img_ratio = img_width / img_height
        
        # Determine if we need to crop or pad
        if abs(img_ratio - target_ratio) < 0.01:
            # Aspect ratios are close enough, just resize
            img_resized = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
        elif img_ratio > target_ratio:
            # Image is wider, crop width
            new_width = int(img_height * target_ratio)
            left = (img_width - new_width) // 2
            img_cropped = img.crop((left, 0, left + new_width, img_height))
            img_resized = img_cropped.resize((target_width, target_height), Image.Resampling.LANCZOS)
        else:
            # Image is taller, crop height
            new_height = int(img_width / target_ratio)
            top = (img_height - new_height) // 2
            img_cropped = img.crop((0, top, img_width, top + new_height))
            img_resized = img_cropped.resize((target_width, target_height), Image.Resampling.LANCZOS)
        
        # Save processed image temporarily
        temp_image_path = str(self.output_dir / "temp_processed_image.jpg")
        img_resized.save(temp_image_path, quality=95)
        
        return temp_image_path


if __name__ == "__main__":
    # Example usage
    generator = VideoGenerator()
    
    print("Video Generator - Example Usage")
    print("\nSupported aspect ratios:")
    print("  - 9:16 (YouTube Shorts, TikTok, Instagram Reels)")
    print("  - 16:9 (Standard YouTube)")
    print("  - 1:1 (Instagram square)")
    print("  - 4:5 (Instagram portrait)")
    print("\nTo use: Provide an image path and audio path to create_video()")

