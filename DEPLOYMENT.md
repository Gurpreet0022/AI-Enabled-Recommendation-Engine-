# Deployment Guide - E-Commerce Recommendation System

## 🚀 Deployment Options

### Option 1: Local Deployment (Development)

#### Prerequisites
- Python 3.8+
- pip package manager
- 2GB+ RAM recommended

#### Steps
```bash
# 1. Navigate to project directory
cd ecommerce_recommendation_system

# 2. Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run setup (first time only)
python setup.py

# 5. Start the application
streamlit run app.py
```

Access at: `http://localhost:8501`

---

### Option 2: Streamlit Cloud (Free Hosting)

#### Prerequisites
- GitHub account
- Streamlit Cloud account (free at share.streamlit.io)

#### Steps

1. **Prepare Repository**
```bash
# Create GitHub repository
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/ecommerce-recommender.git
git push -u origin main
```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repository
   - Set main file: `app.py`
   - Click "Deploy"

3. **First-Time Setup**
   - After deployment, the app will fail initially (no data)
   - SSH into the Streamlit Cloud environment or:
   - Add setup as a pre-deployment step in `packages.txt`:
     ```
     python-setuptools
     ```
   - And create `.streamlit/secrets.toml` with:
     ```toml
     [setup]
     run_setup = true
     ```
   - Modify `app.py` to run setup on first load

4. **Auto-Setup Integration**

Add this to the top of `app.py`:

```python
import os

# Auto-setup for first deployment
if not os.path.exists('models/recommender_model.pkl'):
    with st.spinner("First-time setup... This may take a few minutes."):
        import setup
        setup.setup_system()
    st.success("Setup complete! Please refresh the page.")
    st.stop()
```

---




---

## 🐛 Troubleshooting

### Common Issues

1. **Port Already in Use**
```bash
# Kill process on port 8501
lsof -ti:8501 | xargs kill -9
# Or use different port
streamlit run app.py --server.port=8502
```

2. **Memory Issues**
```bash
# Reduce data size in setup.py
num_products=200
num_interactions=10000
```

3. **Model Loading Fails**
```bash
# Retrain model
rm -rf models/
python setup.py
```

4. **Authentication Errors**
```bash
# Reset auth database
rm data/auth_users.csv
python -c "from auth import AuthManager; AuthManager().create_demo_users()"
```

---

## 📈 Monitoring and Maintenance

### Health Checks

Add health check endpoint:
```python
@app.route('/health')
def health():
    return {'status': 'healthy'}
```

### Logging

Configure logging:
```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

---

## 🎉 Success Checklist

- [ ] Application accessible from external IP
- [ ] Users can register and login
- [ ] Recommendations loading correctly
- [ ] Model performance metrics visible
- [ ] No errors in logs
- [ ] HTTPS enabled (production)

---

**Need Help?** Check the main README.md or open an issue!
