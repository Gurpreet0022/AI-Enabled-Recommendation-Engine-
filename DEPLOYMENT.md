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

### Option 3: Docker Deployment

#### Prerequisites
- Docker installed
- 4GB+ RAM recommended

#### Steps

1. **Create Dockerfile**

Already created in project. Contents:

```dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Run setup on container creation
RUN python setup.py

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

2. **Build and Run**

```bash
# Build image
docker build -t ecommerce-recommender:latest .

# Run container
docker run -p 8501:8501 ecommerce-recommender:latest

# Run with volume (persistent data)
docker run -p 8501:8501 -v $(pwd)/data:/app/data ecommerce-recommender:latest
```

3. **Docker Compose** (Optional)

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
      - ./models:/app/models
    environment:
      - STREAMLIT_SERVER_PORT=8501
    restart: unless-stopped
```

Run with:
```bash
docker-compose up -d
```

---

### Option 4: Heroku Deployment

#### Prerequisites
- Heroku account (free tier available)
- Heroku CLI installed

#### Steps

1. **Create Heroku Files**

Create `Procfile`:
```
web: sh setup.sh && streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

Create `setup.sh`:
```bash
#!/bin/bash

mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"your-email@example.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml

# Run setup if models don't exist
if [ ! -f "models/recommender_model.pkl" ]; then
    python setup.py
fi
```

2. **Deploy**

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Push to Heroku
git push heroku main

# Scale dynos
heroku ps:scale web=1

# Open app
heroku open
```

---

### Option 5: AWS EC2 Deployment

#### Prerequisites
- AWS account
- EC2 instance (t2.medium or larger recommended)

#### Steps

1. **Launch EC2 Instance**
   - AMI: Ubuntu 22.04 LTS
   - Instance Type: t2.medium
   - Security Group: Allow ports 22 (SSH) and 8501 (Streamlit)

2. **SSH into Instance**
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

3. **Setup Environment**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3-pip python3-venv -y

# Clone repository
git clone https://github.com/yourusername/ecommerce-recommender.git
cd ecommerce-recommender

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run setup
python setup.py
```

4. **Run with Systemd (Background Service)**

Create `/etc/systemd/system/streamlit.service`:
```ini
[Unit]
Description=Streamlit E-Commerce Recommender
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/ecommerce-recommender
Environment="PATH=/home/ubuntu/ecommerce-recommender/venv/bin"
ExecStart=/home/ubuntu/ecommerce-recommender/venv/bin/streamlit run app.py --server.port=8501 --server.address=0.0.0.0

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable streamlit
sudo systemctl start streamlit
sudo systemctl status streamlit
```

5. **Access Application**
   - Open browser to `http://your-ec2-ip:8501`

---

### Option 6: Google Cloud Run (Serverless)

#### Prerequisites
- Google Cloud account
- gcloud CLI installed

#### Steps

1. **Enable APIs**
```bash
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

2. **Build and Deploy**
```bash
# Set project
gcloud config set project your-project-id

# Build container
gcloud builds submit --tag gcr.io/your-project-id/ecommerce-recommender

# Deploy to Cloud Run
gcloud run deploy ecommerce-recommender \
  --image gcr.io/your-project-id/ecommerce-recommender \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2
```

---

## 🔧 Configuration for Production

### Environment Variables

Create `.env` file:
```bash
# Application settings
APP_ENV=production
DEBUG=false

# Model settings
NUM_RECOMMENDATIONS=12
MIN_INTERACTIONS=2

# Security
SECRET_KEY=your-secret-key-here
SESSION_TIMEOUT=3600

# Database (if using external DB)
DATABASE_URL=postgresql://user:pass@host:5432/dbname
```

### Performance Optimization

1. **Enable Caching**

Add to app.py:
```python
@st.cache_resource
def load_recommender():
    recommender = HybridRecommender()
    recommender.load_model('models')
    return recommender
```

2. **Use Production Server**

For production, use gunicorn instead of Streamlit's dev server:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8501 app:main
```

3. **Add Monitoring**

Install monitoring:
```bash
pip install prometheus-client
```

4. **Setup HTTPS**

Use Nginx as reverse proxy with Let's Encrypt SSL:
```bash
sudo apt install nginx certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

---

## 📊 Scaling Considerations

### For High Traffic (1000+ users)

1. **Use Redis for Caching**
```bash
pip install redis
```

2. **Implement Load Balancing**
   - Use multiple instances behind a load balancer
   - AWS ELB, Google Cloud Load Balancer, or Nginx

3. **Database Migration**
   - Move from CSV to PostgreSQL/MySQL
   - Use connection pooling

4. **CDN for Static Assets**
   - CloudFlare, AWS CloudFront

### For Large Datasets (1M+ products)

1. **Use Matrix Factorization**
   - Implement SVD/ALS algorithms
   - Use Surprise library or custom implementation

2. **Implement Batch Processing**
   - Precompute recommendations
   - Update periodically (hourly/daily)

3. **Use Vector Databases**
   - Pinecone, Weaviate, or Milvus
   - For fast similarity search

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

### Backup Strategy

```bash
# Backup data and models daily
0 0 * * * /usr/bin/tar -czf backup-$(date +\%Y\%m\%d).tar.gz data/ models/
```

---

## 🎉 Success Checklist

- [ ] Application accessible from external IP
- [ ] Users can register and login
- [ ] Recommendations loading correctly
- [ ] Model performance metrics visible
- [ ] No errors in logs
- [ ] HTTPS enabled (production)
- [ ] Monitoring setup
- [ ] Backup configured

---

**Need Help?** Check the main README.md or open an issue!
