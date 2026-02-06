# 🚀 Nexa Search - Setup Guide

Complete setup instructions for getting Nexa Search running locally.

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.8 or higher** installed
  - Check: `python --version` or `python3 --version`
  - Download from: https://www.python.org/downloads/

- **pip** (Python package manager)
  - Usually comes with Python
  - Check: `pip --version`

- **Git** (optional, for cloning)
  - Download from: https://git-scm.com/

## 🔑 Step 1: Get Your Groq API Key

1. Visit [https://console.groq.com](https://console.groq.com)
2. Sign up for a free account (GitHub or Google sign-in available)
3. Navigate to **API Keys** section
4. Click **"Create API Key"**
5. Copy the key (starts with `gsk_...`)

**Important:** Store this key safely! You won't be able to see it again.

## 📥 Step 2: Download Nexa Search

### Option A: Using Git (Recommended)

```bash
git clone https://github.com/yourusername/nexa-search.git
cd nexa-search
```

### Option B: Download ZIP

1. Download the ZIP from GitHub
2. Extract to a folder
3. Open terminal/command prompt in that folder

## 🔧 Step 3: Install Dependencies

### On macOS/Linux:

```bash
# Create virtual environment (recommended)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### On Windows:

```cmd
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

**Note:** If you see "command not found" for `python3`, try `python` instead.

## 🔐 Step 4: Configure API Key

### Method 1: Using .env file (Recommended)

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your favorite text editor
# Replace 'your_groq_api_key_here' with your actual key
```

Example `.env` file:
```env
GROQ_API_KEY=gsk_abc123xyz789...
```

### Method 2: Environment Variable

**macOS/Linux:**
```bash
export GROQ_API_KEY="gsk_abc123xyz789..."
```

**Windows (Command Prompt):**
```cmd
set GROQ_API_KEY=gsk_abc123xyz789...
```

**Windows (PowerShell):**
```powershell
$env:GROQ_API_KEY="gsk_abc123xyz789..."
```

## ▶️ Step 5: Run Nexa Search

```bash
streamlit run app.py
```

You should see:
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

The app will automatically open in your default browser!

## ✅ Step 6: Test Your Setup

Try these example searches:

1. **"What is quantum computing?"**
2. **"Latest AI research papers"**
3. **"Who won the Nobel Prize in Physics in 2024?"**

If you see AI-generated answers with sources cited, congratulations! 🎉

## 🐛 Troubleshooting

### Issue: "GROQ_API_KEY not found"

**Solution:**
- Ensure `.env` file is in the same folder as `app.py`
- Check the key is correctly formatted: `GROQ_API_KEY=your_key` (no quotes, no spaces)
- Try method 2 (environment variable) instead

### Issue: "No module named 'streamlit'"

**Solution:**
```bash
# Make sure virtual environment is activated
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate

# Reinstall packages
pip install -r requirements.txt
```

### Issue: "Port 8501 is already in use"

**Solution:**
```bash
# Kill existing Streamlit process
# macOS/Linux:
pkill -f streamlit

# Windows:
taskkill /F /IM streamlit.exe

# Or use a different port:
streamlit run app.py --server.port 8502
```

### Issue: Search returns errors

**Solution:**
- Check internet connection
- Verify API key is valid at https://console.groq.com
- Check if you've exceeded free tier rate limits (wait a minute and try again)

### Issue: "ModuleNotFoundError: No module named 'langchain_groq'"

**Solution:**
```bash
# Update pip first
pip install --upgrade pip

# Reinstall requirements
pip install -r requirements.txt --upgrade
```

## 🎯 Optional: Enable LangSmith Tracing

Want to see how the AI agent thinks? Enable LangSmith!

1. Sign up at [https://smith.langchain.com](https://smith.langchain.com)
2. Get your API key from settings
3. Add to `.env`:

```env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_key_here
LANGCHAIN_PROJECT=nexa-search
```

Now you can see agent reasoning steps in the LangSmith dashboard!

## 📚 Next Steps

- **Customize the UI:** Edit CSS in `app.py`
- **Add more tools:** Modify `agent_engine.py`
- **Experiment with models:** Try different Groq models
- **Share feedback:** Open an issue on GitHub

## 💡 Pro Tips

1. **Virtual Environment:** Always activate it before running
   ```bash
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   ```

2. **Keep dependencies updated:**
   ```bash
   pip install -r requirements.txt --upgrade
   ```

3. **Multiple terminal windows:** Keep one for running the app, one for development

4. **Environment variables persist:** Using `.env` file means you don't need to set them every time

## 🆘 Still Having Issues?

- Check the main [README.md](README.md) for more documentation
- Open an issue: [GitHub Issues](https://github.com/yourusername/nexa-search/issues)
- Make sure you're using Python 3.8+: `python --version`

---

**Happy Searching! 🔍✨**
