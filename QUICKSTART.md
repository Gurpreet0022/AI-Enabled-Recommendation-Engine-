# 🚀 QUICK START GUIDE

## E-Commerce Recommendation System

### ⚡ Super Quick Start (1 Minute)

**Option 1: Linux/Mac**
```bash
cd ecommerce_recommendation_system
chmod +x start.sh
./start.sh
```

**Option 2: Windows**
```cmd
cd ecommerce_recommendation_system
start.bat
```

**Option 3: Manual**
```bash
pip install -r requirements.txt
python setup.py
streamlit run app.py
```

That's it! The app will open at `http://localhost:8501`

---

## 🔐 Getting Started

### Create Your Account
1. Open the app at `http://localhost:8501`
2. Click on "Create Account" tab
3. Enter your details:
   - Username (unique)
   - Email address
   - Password (min 6 characters)
4. Click "Create Account"
5. Switch to "Login" tab and sign in

---

## 📱 What Can You Do?

### 1️⃣ Get Personalized Recommendations
- Login to see products recommended for you
- Based on your interaction history
- Updates in real-time

### 2️⃣ Browse Products
- 500+ products across 4 categories
- Filter by category, price, rating
- Search and explore

### 3️⃣ View Statistics
- Your shopping behavior
- Category preferences
- Price distribution
- Interaction analytics

### 4️⃣ Compare Models
- See how different algorithms perform
- Precision, Recall, F1-Score metrics
- Interactive charts

---

## 🎯 Key Features

✅ **Hybrid Recommendations**: 3 algorithms combined  
✅ **Cold Start Handling**: Works for new users  
✅ **Secure Authentication**: Password hashing  
✅ **Real-Time Updates**: Instant recommendations  
✅ **Multi-Category**: Electronics, Fashion, Beauty, Home  
✅ **Advanced Filtering**: Multiple filter options  
✅ **Analytics Dashboard**: Performance metrics  
✅ **Responsive Design**: Works on all devices  

---

## 🛠️ Customization

### Change Number of Products
Edit `setup.py`:
```python
num_products=1000  # Change from 500
```

### Adjust Recommendations
In app, use the sidebar slider:
- 5-20 recommendations

### Switch Algorithm
Select from dropdown:
- Hybrid (recommended)
- Item-based
- User-based
- Content-based

---

## 📊 Sample Data

- **Products**: 500 items
- **Users**: 1000 profiles
- **Interactions**: 50,000 events
- **Categories**: 4 main categories
- **Brands**: 20+ brands

---

## 🛠 Troubleshooting

### Port Already Used
```bash
# Kill process
lsof -ti:8501 | xargs kill -9

# Or use different port
streamlit run app.py --server.port=8502
```

### Module Not Found
```bash
pip install -r requirements.txt
```

### Model Not Loading
```bash
python setup.py
```

### Memory Issues
Reduce data size in `setup.py`:
```python
num_interactions=10000  # Reduce from 50000
```

---

## 📚 Learn More

- **README.md**: Full documentation
- **Code comments**: Throughout all files

---

## 🎓 Project Structure

```
ecommerce_recommendation_system/
├── app.py              # Main app
├── recommender.py      # Recommendation engine
├── data_generator.py   # Data creation
├── evaluator.py        # Model evaluation
├── auth.py            # Authentication
├── setup.py           # Setup script
└── data/              # Generated data
    └── models/        # Trained models
```

---

## 💡 Tips

1. **First Time**: Run setup.py to initialize
2. **New Users**: See popular items first
3. **Existing Users**: Get personalized recs
4. **Filter Products**: Use sidebar options
5. **View Analytics**: Check Model Performance tab

---

## ⚙️ System Requirements

- Python 3.8+
- 2GB RAM minimum
- 500MB disk space
- Modern web browser

---

## 🎉 You're Ready!

Start the app and explore the recommendation system!

```bash
streamlit run app.py
```

Visit: `http://localhost:8501`

---

**Need Help?** Check README.md or review code comments!

**Enjoy! 🛒✨**
