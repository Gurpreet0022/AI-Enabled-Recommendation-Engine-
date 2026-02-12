# E-Commerce Recommendation System

A comprehensive, production-ready e-commerce recommendation system built with Python and Streamlit. Features hybrid collaborative filtering, user authentication, and real-time personalized product recommendations.

## 🌟 Features

### Core Functionality
- **Hybrid Recommendation Engine**: Combines item-based, user-based, content-based, and hybrid filtering
- **Smart Cold Start Handling**: New users receive popular product recommendations
- **Multi-Category Support**: Electronics, Fashion, Beauty, and Home products
- **Real-Time Recommendations**: Instant personalized suggestions based on user behavior

### User Interface
- **Authentication System**: Secure login/signup with password hashing
- **Personalized Dashboard**: Custom recommendations based on user history
- **Interactive Product Cards**: Rich product information with ratings and reviews
- **Advanced Filtering**: Filter by category, price range, and ratings
- **User Statistics**: Visual analytics of shopping behavior

### Model Performance
- **Comprehensive Evaluation**: Precision, Recall, F1-Score, and NDCG metrics
- **Method Comparison**: Compare different recommendation approaches
- **Performance Visualization**: Interactive charts and graphs
- **Catalog Coverage Analysis**: Track recommendation diversity

## 📋 Requirements

```
Python 3.8+
streamlit==1.31.0
pandas==2.1.4
numpy==1.24.3
scikit-learn==1.3.2
scipy==1.11.4
plotly==5.18.0
bcrypt==4.1.2
Pillow==10.2.0
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or download the project
cd ecommerce_recommendation_system

# Install dependencies
pip install -r requirements.txt
```

### 2. Setup and Training

```bash
# Run setup script (generates data and trains model)
python setup.py
```

This will:
- Generate synthetic product catalog (500 products)
- Create user interaction data (50,000 interactions)
- Train the hybrid recommendation model
- Evaluate model performance

### 3. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### 4. Create Account

Create a new account with:
- Username of your choice
- Valid email address
- Password (minimum 6 characters)

## 📁 Project Structure

```
ecommerce_recommendation_system/
├── app.py                    # Main Streamlit application
├── recommender.py            # Hybrid recommendation engine
├── data_generator.py         # Synthetic data generation
├── evaluator.py              # Model evaluation metrics
├── auth.py                   # Authentication system
├── setup.py                  # Setup and initialization
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── data/                     # Generated data files
│   ├── products.csv
│   ├── interactions.csv
│   ├── users.csv
│   └── auth_users.csv
└── models/                   # Trained models
    ├── recommender_model.pkl
    ├── products.csv
    └── evaluation_results.csv
```

## 🎯 Recommendation Methods

### 1. Item-Based Collaborative Filtering
- Recommends items similar to what the user has interacted with
- Uses cosine similarity between item vectors
- Best for users with consistent preferences

### 2. User-Based Collaborative Filtering
- Finds similar users and recommends their preferred items
- Leverages community behavior patterns
- Effective for discovering new interests

### 3. Content-Based Filtering
- Recommends items with similar features (category, brand, price)
- Uses product metadata for matching
- Works well for niche preferences

### 4. Hybrid Approach (Default)
- Combines all three methods with weighted voting
- Weights: Item-based (40%), User-based (30%), Content-based (30%)
- Provides balanced, diverse recommendations

## 📊 Model Performance

The system achieves the following performance metrics (K=10):

| Method | Precision | Recall | F1-Score | NDCG |
|--------|-----------|--------|----------|------|
| Hybrid | ~0.04-0.06 | ~0.08-0.12 | ~0.05-0.08 | ~0.06-0.10 |

*Note: Actual metrics depend on data characteristics and will be displayed in the app.*

## 🔧 Customization

### Adjust Data Size

Edit `setup.py`:

```python
products_df, users_df, interactions_df = generator.generate_dataset(
    num_products=1000,      # Increase for more products
    num_users=2000,         # Increase for more users
    num_interactions=100000 # Increase for more interactions
)
```

### Modify Recommendation Weights

Edit `recommender.py` in the `get_hybrid_recommendations` method:

```python
def get_hybrid_recommendations(self, user_id, top_n=10, 
                               item_weight=0.4,      # Adjust weights
                               user_weight=0.3,      # as needed
                               content_weight=0.3):
```

### Add New Product Categories

Edit `data_generator.py`:

```python
self.categories = {
    'Electronics': [...],
    'Fashion': [...],
    'YourCategory': ['Product1', 'Product2', ...]  # Add here
}
```

## 🌐 Deployment Options

### Local Deployment
```bash
streamlit run app.py
```

### Streamlit Cloud
1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Deploy!

### Heroku Deployment

1. Create `Procfile`:
```
web: sh setup.sh && streamlit run app.py
```

2. Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/
echo "\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
\n\
" > ~/.streamlit/config.toml
```

3. Deploy:
```bash
heroku create your-app-name
git push heroku main
```

## 🔒 Security Notes

- Passwords are hashed using bcrypt
- Session state manages authentication
- No sensitive data in version control
- For production: Use environment variables for secrets

## 🛠 Troubleshooting

### Model not loading
```bash
# Retrain the model
python setup.py
```

### Memory issues
Reduce data size in `setup.py`:
```python
num_products=200,
num_users=500,
num_interactions=10000
```

### Authentication errors
Delete and recreate auth file:
```bash
rm data/auth_users.csv
python setup.py
```

### Port already in use
```bash
# Use different port
streamlit run app.py --server.port=8502
```

## 📈 Performance Optimization

1. **Increase Sample Size**: More data = better recommendations
2. **Adjust Similarity Thresholds**: Fine-tune collaborative filtering
3. **Feature Engineering**: Add more product attributes
4. **Matrix Factorization**: Implement SVD for large-scale data
5. **Caching**: Add Redis for faster lookups in production

## 🤝 Contributing

Suggestions for improvements:
1. Add real product images
2. Implement deep learning models
3. Add A/B testing framework
4. Include purchase tracking
5. Add recommendation explanations

## 📝 License

MIT License - Feel free to use for personal or commercial projects.

## 🙏 Acknowledgments

- Built with Streamlit
- Uses scikit-learn for ML algorithms
- Plotly for visualizations
- bcrypt for secure authentication

## 📧 Support

For issues or questions:
1. Check troubleshooting section
2. Review code comments
3. Open an issue on GitHub

---

**Happy Recommending! 🎉**
