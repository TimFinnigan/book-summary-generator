# 📚 Book Summary Generator

An AI-powered tool that generates engaging book summaries, converts them to audio narration, and creates videos optimized for YouTube Shorts and social media.

## Features

### 1. 📝 Text Summary Generation
- Generate book summaries using OpenAI's GPT models
- **Iterative refinement**: Keep refining until you're happy with the result
- Multiple length options (short, medium, long)
- Conversational tone optimized for audio narration

### 2. 🎵 Audio Narration
- Convert text summaries to natural-sounding speech using OpenAI's TTS
- 6 different voice options (male/female, various styles)
- Choice between standard and HD quality

### 3. 🎬 Video Generation
- Combine images with audio narration
- **Default 9:16 aspect ratio** (YouTube Shorts, TikTok, Instagram Reels)
- Support for multiple aspect ratios (16:9, 1:1, 4:5)
- Smart image cropping to fit aspect ratio

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up OpenAI API Key

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys).

### 3. Create Output Directory

The application will automatically create an `output/` directory for generated files.

## Usage

### Interactive Mode (Recommended)

Run the main application for a step-by-step guided experience:

```bash
python main.py
```

This will walk you through:
1. Entering book details
2. Generating and refining the summary iteratively
3. Selecting voice for audio narration
4. Adding an image for video creation

### Quick Mode

Generate everything with default settings from the command line:

```bash
python main.py "Book Title" "Author Name" "/path/to/image.jpg"
```

Example:
```bash
python main.py "Atomic Habits" "James Clear" "./book_cover.jpg"
```

### Using Individual Modules

#### Generate Summary Only

```python
from summary_generator import SummaryGenerator

generator = SummaryGenerator()

# Generate initial summary
summary = generator.generate_summary(
    book_title="Atomic Habits",
    book_author="James Clear",
    summary_length="medium"  # or "short", "long"
)
print(summary)

# Refine the summary
refined = generator.refine_summary(
    "Make it more concise and focus on the main framework"
)
print(refined)
```

#### Generate Audio Only

```python
from audio_generator import AudioGenerator

generator = AudioGenerator()

# Available voices: alloy, echo, fable, onyx, nova, shimmer
audio_path = generator.generate_audio(
    text="Your summary text here...",
    output_filename="narration.mp3",
    voice="nova",
    model="tts-1"  # or "tts-1-hd" for higher quality
)
```

#### Generate Video Only

```python
from video_generator import VideoGenerator

generator = VideoGenerator()

video_path = generator.create_video(
    image_path="book_cover.jpg",
    audio_path="output/narration.mp3",
    output_filename="book_summary.mp4",
    aspect_ratio="9:16"  # YouTube Shorts format
)
```

## Voice Options

| Voice | Description | Best For |
|-------|-------------|----------|
| **alloy** | Neutral and balanced | General content |
| **echo** | Male, clear | Professional narration |
| **fable** | British accent | Literary content |
| **onyx** | Deep male voice | Authoritative tone |
| **nova** | Female, energetic | Engaging content (recommended) |
| **shimmer** | Female, soft | Gentle, calming narration |

## Aspect Ratios

| Ratio | Dimensions | Best For |
|-------|------------|----------|
| **9:16** | 1080x1920 | YouTube Shorts, TikTok, Instagram Reels (default) |
| 16:9 | 1920x1080 | Standard YouTube videos |
| 1:1 | 1080x1080 | Instagram square posts |
| 4:5 | 1080x1350 | Instagram portrait posts |

## Summary Length Guidelines

- **Short**: 100-150 words - Core message only
- **Medium**: 250-350 words - Main themes and key insights (recommended)
- **Long**: 500-700 words - Comprehensive coverage

## Tips for Best Results

### For Summaries:
- Provide specific context or focus areas when generating
- Use the iterative refinement feature to dial in the perfect tone
- Medium length works best for video narrations (2-3 minutes)

### For Audio:
- Use **nova** or **shimmer** for engaging, friendly narration
- Use **onyx** or **echo** for more authoritative content
- Choose HD quality (tts-1-hd) for final production

### For Video:
- Use high-quality images (book covers work great!)
- Images will be automatically cropped to fit aspect ratio
- Drag and drop image files when prompted in interactive mode

## Project Structure

```
book-summary-generator/
├── main.py                 # Main application interface
├── summary_generator.py    # Text summary generation
├── audio_generator.py      # Audio narration generation
├── video_generator.py      # Video creation
├── requirements.txt        # Python dependencies
├── .env                    # API keys (create this)
├── .gitignore             # Git ignore rules
└── output/                # Generated files (auto-created)
    ├── *.mp3              # Audio files
    └── *.mp4              # Video files
```

## Requirements

- Python 3.8+
- OpenAI API key
- Internet connection for API calls

## Cost Considerations

- **GPT-4o-mini**: ~$0.15 per 1M input tokens, ~$0.60 per 1M output tokens
- **TTS**: ~$15 per 1M characters (a 300-word summary ≈ $0.03)
- **Total per summary**: Typically under $0.10

## Troubleshooting

### API Key Issues
```
ValueError: OPENAI_API_KEY not found in environment variables
```
→ Make sure you've created a `.env` file with your API key

### Import Errors
```
ModuleNotFoundError: No module named 'openai'
```
→ Run `pip install -r requirements.txt` or `pip3 install -r requirements.txt`

### MoviePy Import Issues
```
ModuleNotFoundError: No module named 'moviepy.editor'
```
→ The project uses moviepy 1.0.3 specifically. Run:
```bash
pip3 install moviepy==1.0.3
```
Note: Newer versions of moviepy have a different module structure

### Video Generation Issues
```
FileNotFoundError: Image file not found
```
→ Check the image path and ensure the file exists. Use absolute paths or drag-and-drop in interactive mode.

## License

MIT License - feel free to use and modify for your projects!

## Contributing

Contributions welcome! Feel free to open issues or submit pull requests.

---

**Happy summarizing! 📚✨**

