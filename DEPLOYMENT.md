# ☁️ Deployment Guide - Nexa Search

Deploy your AI search engine to the cloud for free!

## 🎯 Option 1: Streamlit Community Cloud (Recommended)

**Pros:** Free, easy, automatic HTTPS, custom subdomain  
**Cons:** Public repository required (or pay for private)

### Steps:

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/nexa-search.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repository
   - Set main file: `app.py`
   - Click "Deploy"

3. **Add Secrets**
   - In Streamlit Cloud dashboard, go to app settings
   - Click "Secrets"
   - Add:
     ```toml
     GROQ_API_KEY = "gsk_your_key_here"
     
     # Optional: LangSmith
     LANGCHAIN_TRACING_V2 = "true"
     LANGCHAIN_API_KEY = "your_langsmith_key"
     LANGCHAIN_PROJECT = "nexa-search"
     ```

4. **Access Your App**
   - URL: `https://your-app-name.streamlit.app`
   - Share with anyone!

**Cost:** FREE forever

---

## 🎯 Option 2: Heroku

**Pros:** Robust, scalable, easy Git deployment  
**Cons:** No longer has free tier

### Steps:

1. **Install Heroku CLI**
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku
   
   # Windows
   # Download from: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Create Heroku App**
   ```bash
   heroku login
   heroku create nexa-search-app
   ```

3. **Add Buildpacks**
   ```bash
   heroku buildpacks:set heroku/python
   ```

4. **Create Procfile**
   ```bash
   echo "web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0" > Procfile
   ```

5. **Set Environment Variables**
   ```bash
   heroku config:set GROQ_API_KEY=your_key_here
   
   # Optional: LangSmith
   heroku config:set LANGCHAIN_TRACING_V2=true
   heroku config:set LANGCHAIN_API_KEY=your_key
   ```

6. **Deploy**
   ```bash
   git push heroku main
   ```

**Cost:** Starting at $7/month (Eco dyno)

---

## 🎯 Option 3: Railway

**Pros:** Modern, generous free tier, great DX  
**Cons:** Free tier has limits

### Steps:

1. **Connect Repository**
   - Go to [railway.app](https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `nexa-search`

2. **Configure**
   - Railway auto-detects Python
   - Set start command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

3. **Add Environment Variables**
   - Click "Variables"
   - Add:
     ```
     GROQ_API_KEY=your_key_here
     PORT=8501
     ```

4. **Deploy**
   - Railway auto-deploys on push
   - Get public URL from dashboard

**Cost:** $5/month free credit, then pay-as-you-go

---

## 🎯 Option 4: Render

**Pros:** Free tier, easy setup, great docs  
**Cons:** Free tier sleeps after inactivity

### Steps:

1. **Create render.yaml**
   ```yaml
   services:
     - type: web
       name: nexa-search
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
       envVars:
         - key: GROQ_API_KEY
           sync: false
         - key: PYTHON_VERSION
           value: 3.11.0
   ```

2. **Deploy**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect GitHub repository
   - Render auto-detects config

3. **Set Secrets**
   - In dashboard, go to "Environment"
   - Add `GROQ_API_KEY`

**Cost:** FREE (with limitations), $7/month for always-on

---

## 🎯 Option 5: Google Cloud Run

**Pros:** Serverless, scales to zero, pay-per-use  
**Cons:** Requires Docker knowledge

### Steps:

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.11-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   COPY . .
   
   EXPOSE 8080
   
   CMD streamlit run app.py --server.port=8080 --server.address=0.0.0.0
   ```

2. **Build and Deploy**
   ```bash
   # Install gcloud CLI
   # https://cloud.google.com/sdk/docs/install
   
   # Set project
   gcloud config set project YOUR_PROJECT_ID
   
   # Build
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/nexa-search
   
   # Deploy
   gcloud run deploy nexa-search \
     --image gcr.io/YOUR_PROJECT_ID/nexa-search \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars GROQ_API_KEY=your_key
   ```

**Cost:** Free tier generous, ~$0.10/month for light use

---

## 🎯 Option 6: Docker + Any VPS

**Pros:** Full control, works anywhere  
**Cons:** You manage infrastructure

### Dockerfile (included above)

### Docker Compose:
```yaml
version: '3.8'

services:
  nexa-search:
    build: .
    ports:
      - "8501:8501"
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
    restart: unless-stopped
```

### Run:
```bash
# Build
docker-compose build

# Run
docker-compose up -d

# View logs
docker-compose logs -f
```

Deploy on any VPS (DigitalOcean, Linode, AWS EC2, etc.)

**Cost:** VPS prices vary ($5-20/month typically)

---

## 🔒 Security Best Practices

### Environment Variables
- **Never** commit `.env` to Git
- Use platform secret management
- Rotate API keys regularly

### API Rate Limits
```python
# Add to agent_engine.py for production
from langchain.callbacks import get_openai_callback

# Track usage
with get_openai_callback() as cb:
    result = agent.run(query)
    print(f"Tokens used: {cb.total_tokens}")
```

### HTTPS
- All platforms above provide HTTPS automatically
- Never deploy without HTTPS in production

### Rate Limiting (Optional)
```python
# Install: pip install streamlit-authenticator
import streamlit_authenticator as stauth

# Add authentication
authenticator = stauth.Authenticate(
    credentials,
    cookie_name,
    key,
    cookie_expiry_days
)
```

---

## 📊 Monitoring

### Streamlit Cloud
- Built-in analytics
- View logs in dashboard
- Auto-updates on Git push

### Custom Monitoring
```python
# Add to app.py
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Log searches
logger.info(f"Search: {query}")
logger.info(f"Result: {result['success']}")
```

### LangSmith (Recommended)
- Full agent tracing
- Performance metrics
- Error tracking
- Free tier available

---

## 🚀 Performance Tips

1. **Caching**
   ```python
   @st.cache_data(ttl=3600)
   def cached_search(query):
       return run_search(query)
   ```

2. **Lazy Loading**
   ```python
   if 'engine' not in st.session_state:
       st.session_state.engine = get_search_engine()
   ```

3. **Connection Pooling**
   - Groq handles this automatically
   - No additional config needed

---

## 📱 Custom Domain

### Streamlit Cloud
- Pro plan: Custom domains
- Free: Use provided `.streamlit.app` subdomain

### Other Platforms
1. Buy domain (Namecheap, Google Domains, etc.)
2. Add DNS records (platform provides instructions)
3. Configure SSL (usually automatic)

---

## 🎉 Post-Deployment

1. **Test thoroughly**
   - Try various queries
   - Check error handling
   - Verify all tools work

2. **Share**
   - Tweet your project
   - Post on Reddit (r/MachineLearning, r/Python)
   - Add to your portfolio

3. **Monitor**
   - Check logs regularly
   - Watch for API limit errors
   - Track user feedback

---

## 🆘 Troubleshooting

### "Application error"
→ Check logs for specific error  
→ Verify all env vars are set  
→ Ensure requirements.txt is complete

### "Memory exceeded"
→ Reduce `top_k_results` in tools  
→ Use lighter model (Mixtral instead of Llama)  
→ Upgrade to paid tier

### Slow responses
→ Enable caching  
→ Reduce timeout values  
→ Use CDN for static assets

---

**Ready to deploy? Choose a platform and get started! 🚀**

Need help? Open an issue on GitHub.
