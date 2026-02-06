# ⚡ Quick Start - Nexa Search

Get up and running in 3 minutes!

## 🎯 For Beginners

### Step 1: Install Python
If you don't have Python installed:
- **Windows/Mac:** Download from [python.org](https://www.python.org/downloads/)
- **Linux:** `sudo apt install python3 python3-pip` (Ubuntu/Debian)

### Step 2: Get Groq API Key (Free!)
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up (free, takes 30 seconds)
3. Create API key
4. Copy it (starts with `gsk_...`)

### Step 3: Run Nexa Search

**On Mac/Linux:**
```bash
# 1. Download and enter folder
git clone https://github.com/yourusername/nexa-search.git
cd nexa-search

# 2. Install
pip3 install -r requirements.txt

# 3. Set your API key
echo 'GROQ_API_KEY=gsk_your_key_here' > .env

# 4. Run!
streamlit run app.py
```

**On Windows:**
```cmd
# 1. Download and enter folder
git clone https://github.com/yourusername/nexa-search.git
cd nexa-search

# 2. Install
pip install -r requirements.txt

# 3. Create .env file
copy .env.example .env
# Then edit .env and add your key

# 4. Run!
streamlit run app.py
```

**Or just double-click `run.bat` (Windows) or `run.sh` (Mac/Linux)!**

## 🎯 For Developers

```bash
# Clone
git clone https://github.com/yourusername/nexa-search.git && cd nexa-search

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env and add GROQ_API_KEY

# Run
streamlit run app.py
```

## 🚀 Using the App

1. **Enter your question** in the search box
2. **Press Enter** or click outside the box
3. **Wait 3-5 seconds** for AI to search and synthesize
4. **Get your answer** with sources cited!

### Example Queries:
- "What are the latest developments in AI?"
- "Explain quantum computing simply"
- "Recent research on climate change"
- "Who won the 2024 Nobel Prize in Physics?"

## 🎨 Optional: Enable Debugging

Want to see how the AI thinks?

1. Sign up at [smith.langchain.com](https://smith.langchain.com)
2. Get API key
3. Add to `.env`:
   ```env
   LANGCHAIN_TRACING_V2=true
   LANGCHAIN_API_KEY=your_langsmith_key
   ```

Now see agent reasoning in LangSmith dashboard!

## 📱 Access from Other Devices

When running, you'll see:
```
Network URL: http://192.168.x.x:8501
```

Open this URL on your phone/tablet on the same WiFi!

## ❓ Common Issues

**"GROQ_API_KEY not found"**
→ Check `.env` file exists and has your key

**"No module named streamlit"**
→ Run `pip install -r requirements.txt`

**"Port 8501 already in use"**
→ Run `streamlit run app.py --server.port 8502`

## 📚 Next Steps

- **Customize:** Edit `app.py` to change colors/styling
- **Extend:** Add new search tools in `agent_engine.py`
- **Deploy:** Host on Streamlit Cloud (free!)

## 💡 Pro Tip

Bookmark `http://localhost:8501` for quick access!

---

**Need help?** Check [SETUP.md](SETUP.md) for detailed instructions.
