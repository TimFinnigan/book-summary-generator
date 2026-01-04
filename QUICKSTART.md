# 🚀 Quick Start Guide

Get up and running with the Book Summary Generator in 5 minutes!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `openai` - For GPT and TTS APIs
- `python-dotenv` - For environment variable management
- `moviepy` - For video generation
- `Pillow` - For image processing

## Step 2: Get Your OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy your API key

## Step 3: Create .env File

Create a file named `.env` in the project root:

```bash
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

Replace `your_api_key_here` with your actual API key.

## Step 4: Test the Setup

Run the example script to verify everything works:

```bash
python example.py
```

This will:
- ✅ Generate a sample book summary
- ✅ Create audio narration
- ✅ Show how to create videos

## Step 5: Create Your First Summary

### Option A: Interactive Mode (Easiest)

```bash
python main.py
```

Follow the prompts to:
1. Enter book title and author
2. Generate and refine summary
3. Select voice for narration
4. Add image for video

### Option B: Quick Mode

```bash
python main.py "Book Title" "Author Name" "path/to/image.jpg"
```

Example:
```bash
python main.py "Atomic Habits" "James Clear" "./cover.jpg"
```

## Common Issues

### "OPENAI_API_KEY not found"
→ Make sure your `.env` file is in the project root directory

### "ModuleNotFoundError"
→ Run `pip3 install -r requirements.txt` (note: use `pip3` on macOS)

### MoviePy import issues
→ This project requires moviepy 1.0.3 specifically:
```bash
pip3 install moviepy==1.0.3
```

### "Image file not found"
→ Use absolute path or drag-and-drop the file when prompted

## What's Next?

- Check out `README.md` for detailed documentation
- Run `python example.py` to see code examples
- Explore individual modules in the Python files

## Cost Estimate

Generating one complete book summary (text + audio + video):
- Text generation: ~$0.01
- Audio generation: ~$0.03
- Total: **~$0.04 per summary**

---

**Need help?** Open an issue on GitHub or check the README.md for more details.

