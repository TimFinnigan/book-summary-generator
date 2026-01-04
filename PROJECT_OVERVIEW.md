# 📊 Project Overview

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    MAIN APPLICATION                      │
│                      (main.py)                          │
│                                                         │
│  Interactive CLI for complete workflow                  │
└────────────┬───────────────┬────────────────┬──────────┘
             │               │                │
             ▼               ▼                ▼
    ┌────────────┐  ┌───────────────┐  ┌──────────────┐
    │  SUMMARY   │  │     AUDIO     │  │    VIDEO     │
    │ GENERATOR  │  │  GENERATOR    │  │  GENERATOR   │
    │            │  │               │  │              │
    │ OpenAI GPT │  │  OpenAI TTS   │  │   MoviePy    │
    └────────────┘  └───────────────┘  └──────────────┘
         │                 │                  │
         ▼                 ▼                  ▼
    Text Summary      Audio MP3          Video MP4
```

## Three Core Modules

### 1️⃣ Summary Generator (`summary_generator.py`)
**Purpose**: Generate and iteratively refine book summaries

**Key Features**:
- Uses OpenAI GPT-4o-mini by default
- Maintains conversation history for iterations
- Three length options (short/medium/long)
- Context-aware refinement

**Main Methods**:
```python
generate_summary(book_title, book_author, ...)  # Initial generation
refine_summary(refinement_request)              # Iterative refinement
reset()                                         # Clear history
```

**Use Case**: "Make it shorter" → "Focus more on themes" → Perfect!

---

### 2️⃣ Audio Generator (`audio_generator.py`)
**Purpose**: Convert text to natural-sounding speech

**Key Features**:
- 6 voice options (alloy, echo, fable, onyx, nova, shimmer)
- 2 quality levels (standard/HD)
- Automatic MP3 output

**Main Methods**:
```python
generate_audio(text, voice, model)      # Generate narration
list_available_voices()                 # Show voice options
```

**Best Practices**:
- Use "nova" for engaging content
- Use "onyx" for authoritative tone
- Choose HD for final production

---

### 3️⃣ Video Generator (`video_generator.py`)
**Purpose**: Combine images with audio into videos

**Key Features**:
- Smart image cropping for aspect ratios
- 4 aspect ratio presets (9:16, 16:9, 1:1, 4:5)
- Automatic duration matching with audio

**Main Methods**:
```python
create_video(image_path, audio_path, aspect_ratio)  # Generate video
_process_image(image_path, width, height)           # Smart cropping
```

**Optimizations**:
- 9:16 default (YouTube Shorts)
- Center-crop algorithm
- High-quality encoding (H.264 + AAC)

---

## Main Application (`main.py`)

### BookSummaryApp Class
Orchestrates the complete workflow with two modes:

#### Interactive Mode
```bash
python main.py
```
- Step-by-step guided process
- Iterative refinement loop
- Voice and quality selection
- Drag-and-drop image support

#### Quick Mode
```bash
python main.py "Book Title" "Author" "image.jpg"
```
- One command, everything generated
- Uses sensible defaults
- Great for batch processing

---

## Workflow Diagram

```
START
  │
  ├─► Enter Book Details
  │   (title, author, length, context)
  │
  ├─► Generate Summary
  │   │
  │   ├─► Review Summary
  │   │
  │   ├─► Satisfied? ──► YES ──┐
  │   │                        │
  │   └─► NO ──► Refine ───────┘
  │
  ├─► Select Voice & Quality
  │
  ├─► Generate Audio (MP3)
  │
  ├─► Select Image & Aspect Ratio
  │
  ├─► Generate Video (MP4)
  │
  └─► COMPLETE! 🎉
```

---

## File Structure

```
book-summary-generator/
│
├── 📄 Core Modules
│   ├── summary_generator.py     # Text generation + iteration
│   ├── audio_generator.py       # Text-to-speech
│   └── video_generator.py       # Image + audio → video
│
├── 🎯 Main Application
│   ├── main.py                  # Interactive & quick mode
│   └── example.py               # Usage examples
│
├── 📚 Documentation
│   ├── README.md                # Full documentation
│   ├── QUICKSTART.md            # 5-minute setup guide
│   └── PROJECT_OVERVIEW.md      # This file
│
├── ⚙️ Configuration
│   ├── requirements.txt         # Python dependencies
│   ├── .env                     # API keys (create this)
│   └── .gitignore              # Git ignore rules
│
└── 📁 output/                   # Generated files (auto-created)
    ├── *.mp3                    # Audio narrations
    └── *.mp4                    # Final videos
```

---

## Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Text Generation** | OpenAI GPT-4o-mini | Fast, cost-effective summaries |
| **Text-to-Speech** | OpenAI TTS | Natural-sounding narration |
| **Video Processing** | MoviePy | Combine image + audio |
| **Image Processing** | Pillow (PIL) | Smart cropping & resizing |
| **Environment** | python-dotenv | Secure API key management |

---

## API Usage & Costs

### Per Summary Generation:

| Component | API | Cost |
|-----------|-----|------|
| Text (medium) | GPT-4o-mini | ~$0.01 |
| Audio (300 words) | TTS | ~$0.03 |
| **Total** | | **~$0.04** |

### Monthly Estimates:
- 10 summaries/month: ~$0.40
- 100 summaries/month: ~$4.00
- 1000 summaries/month: ~$40.00

*Costs based on OpenAI pricing as of January 2026*

---

## Key Design Decisions

### ✅ Why OpenAI?
- Best-in-class language models
- Natural TTS voices
- Simple, reliable API
- Cost-effective for this use case

### ✅ Why Iterative Refinement?
- Perfection requires iteration
- User maintains creative control
- Conversational workflow
- Better results than one-shot generation

### ✅ Why 9:16 Default?
- Optimized for YouTube Shorts
- Mobile-first consumption
- Vertical format dominates social media
- Easy to crop to other ratios

### ✅ Why Python?
- Excellent AI/ML libraries
- OpenAI's official SDK
- Easy video processing (MoviePy)
- Accessible to developers

---

## Extensibility

### Easy to Add:
- ✨ New aspect ratios (modify `video_generator.py`)
- ✨ Additional AI models (modify `summary_generator.py`)
- ✨ Batch processing (extend `main.py`)
- ✨ Custom prompts (modify system messages)
- ✨ Text overlays on videos (extend `VideoGenerator`)

### Potential Enhancements:
- 🎨 Add subtitles/captions to videos
- 🌐 Support multiple languages
- 📊 Generate analytics/metrics
- 💾 Database for managing summaries
- 🔄 Batch process multiple books
- 🎭 Custom voice cloning integration

---

## Development Principles

1. **Modularity**: Each component works independently
2. **User-Friendly**: Interactive CLI with clear prompts
3. **Flexible**: Use modules separately or together
4. **Production-Ready**: Error handling, validation, documentation
5. **Cost-Conscious**: Uses efficient models and caching

---

## Getting Started

1. **Quick Setup**: See `QUICKSTART.md`
2. **Full Docs**: See `README.md`
3. **Code Examples**: Run `example.py`
4. **Create Summary**: Run `main.py`

---

## Support & Contribution

- 🐛 **Bug Reports**: Open an issue
- 💡 **Feature Requests**: Open an issue
- 🤝 **Contributions**: Pull requests welcome
- 📧 **Questions**: Check README.md first

---

**Happy summarizing! 📚✨**

