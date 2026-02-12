"""
E-commerce Recommendation System - Streamlit App
Features: Authentication, Recommendations, Analytics, Product Discovery
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from auth import AuthManager
from recommender import HybridRecommender
from evaluator import ModelEvaluator
import os
from datetime import datetime


# Page configuration
st.set_page_config(
    page_title="E-Commerce Recommender",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .product-card {
        border: 2px solid #e0e0e0;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .product-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    .product-title {
        font-size: 18px;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 8px;
    }
    .product-price {
        font-size: 24px;
        color: #e74c3c;
        font-weight: bold;
        margin: 10px 0;
    }
    .product-rating {
        color: #f39c12;
        font-size: 16px;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        color: white;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    .metric-value {
        font-size: 36px;
        font-weight: bold;
        margin: 10px 0;
    }
    .metric-label {
        font-size: 14px;
        opacity: 0.9;
    }
    .category-badge {
        background-color: #3498db;
        color: white;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 12px;
        display: inline-block;
        margin: 5px 5px 5px 0;
    }
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)


# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_id = None
    st.session_state.username = None

if 'recommender' not in st.session_state:
    st.session_state.recommender = None

if 'auth_manager' not in st.session_state:
    st.session_state.auth_manager = AuthManager()

if 'wishlist' not in st.session_state:
    st.session_state.wishlist = []

if 'cart' not in st.session_state:
    st.session_state.cart = []

if 'view_history' not in st.session_state:
    st.session_state.view_history = []


def load_recommender():
    """Load the recommendation model"""
    if st.session_state.recommender is None:
        with st.spinner("Loading recommendation model..."):
            try:
                recommender = HybridRecommender()
                recommender.load_model('models')
                st.session_state.recommender = recommender
                return True
            except Exception as e:
                st.error(f"Error loading model: {str(e)}")
                st.info("Please make sure the model is trained. Run: python setup.py")
                return False
    return True


def login_page():
    """Login page UI"""
    # Header
    st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 40px; border-radius: 20px; text-align: center; margin-bottom: 30px;'>
            <h1 style='color: white; margin: 0;'>🛒 E-Commerce Recommender</h1>
            <p style='color: white; font-size: 18px; margin-top: 10px;'>
                Your Personalized Shopping Experience Powered by AI
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Login/Signup Tabs
        tab1, tab2 = st.tabs(["🔐 Login", "✨ Create Account"])
        
        with tab1:
            st.markdown("#### Welcome Back!")
            st.markdown("Login to access your personalized recommendations")
            
            with st.form("login_form"):
                username = st.text_input("Username", placeholder="Enter your username")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                
                remember_me = st.checkbox("Remember me")
                
                submitted = st.form_submit_button("🔑 Login", use_container_width=True, type="primary")
                
                if submitted:
                    if username and password:
                        success, user_id, message = st.session_state.auth_manager.login_user(
                            username, password
                        )
                        
                        if success:
                            st.session_state.authenticated = True
                            st.session_state.user_id = user_id
                            st.session_state.username = username
                            st.success(f"✅ {message}")
                            st.rerun()
                        else:
                            st.error(f"❌ {message}")
                    else:
                        st.warning("⚠️ Please enter both username and password")
        
        with tab2:
            st.markdown("#### Join Our Community!")
            st.markdown("Create an account to get personalized product recommendations")
            
            with st.form("signup_form", clear_on_submit=True):
                new_username = st.text_input("Username", placeholder="Choose a unique username")
                new_email = st.text_input("Email Address", placeholder="your.email@example.com")
                
                col_pass1, col_pass2 = st.columns(2)
                with col_pass1:
                    new_password = st.text_input("Password", type="password", 
                                                placeholder="Min 6 characters")
                with col_pass2:
                    confirm_password = st.text_input("Confirm Password", type="password", 
                                                    placeholder="Re-enter password")
                
                agree_terms = st.checkbox("I agree to the Terms & Conditions and Privacy Policy")
                
                submitted = st.form_submit_button("✨ Create Account", use_container_width=True, type="primary")
                
                if submitted:
                    if not agree_terms:
                        st.error("❌ Please agree to Terms & Conditions to continue")
                    elif not (new_username and new_email and new_password and confirm_password):
                        st.warning("⚠️ Please fill in all required fields")
                    elif new_password != confirm_password:
                        st.error("❌ Passwords do not match!")
                    elif len(new_password) < 6:
                        st.error("❌ Password must be at least 6 characters long")
                    elif '@' not in new_email or '.' not in new_email:
                        st.error("❌ Please enter a valid email address")
                    else:
                        success, message = st.session_state.auth_manager.register_user(
                            new_username, new_email, new_password
                        )
                        
                        if success:
                            st.success(f"✅ {message}")
                            st.info("👉 Please switch to Login tab to access your account")
                        else:
                            st.error(f"❌ {message}")


def display_product_card(product, container):
    """Display a product card"""
    with container:
        st.markdown(f"""
        <div class="product-card">
            <div class="product-title">{product['name']}</div>
            <span class="category-badge">{product['category']}</span>
            <span class="category-badge" style="background-color: #9b59b6;">{product['brand']}</span>
            <div class="product-price">${product['price']:.2f}</div>
            <div class="product-rating">
                {'⭐' * int(product['rating'])} {product['rating']:.1f} 
                <span style="color: #7f8c8d;">({product['num_reviews']} reviews)</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Use buttons without nested columns
        if st.button("❤️ Wishlist", key=f"wish_{product['product_id']}", use_container_width=True):
            if product['product_id'] not in st.session_state.wishlist:
                st.session_state.wishlist.append(product['product_id'])
                st.success("Added to wishlist!")
            else:
                st.info("Already in wishlist")
        
        if st.button("🛒 Add to Cart", key=f"cart_{product['product_id']}", use_container_width=True):
            if product['product_id'] not in st.session_state.cart:
                st.session_state.cart.append(product['product_id'])
                st.success("Added to cart!")
            else:
                st.info("Already in cart")


def recommendations_page():
    """Main recommendations page"""
    if not load_recommender():
        return
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"### 👤 Welcome, {st.session_state.username}!")
        
        st.markdown("---")
        
        # Recommendation settings
        st.markdown("### ⚙️ Settings")
        num_recommendations = st.slider(
            "Number of recommendations",
            min_value=5,
            max_value=20,
            value=12,
            step=1
        )
        
        recommendation_method = st.selectbox(
            "Recommendation Method",
            ["hybrid", "item_based", "user_based", "content_based"],
            format_func=lambda x: x.replace('_', ' ').title()
        )
        
        st.markdown("---")
        
        # Quick stats
        st.markdown("### 📊 Quick Stats")
        st.metric("Wishlist Items", len(st.session_state.wishlist))
        st.metric("Cart Items", len(st.session_state.cart))
        st.metric("Products Viewed", len(st.session_state.view_history))
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_id = None
            st.session_state.username = None
            st.session_state.wishlist = []
            st.session_state.cart = []
            st.session_state.view_history = []
            st.rerun()
    
    # Main content
    tabs = st.tabs(["🏠 For You", "🛒 Cart", "❤️ Wishlist", "📊 Analytics", "🔍 Explore"])
    
    # Tab 1: Recommendations
    with tabs[0]:
        st.markdown("## 🎯 Recommended For You")
        st.markdown("Based on your preferences and shopping history")
        
        try:
            recommendations = st.session_state.recommender.get_recommendations(
                st.session_state.user_id,
                top_n=num_recommendations,
                method=recommendation_method
            )
            
            if recommendations:
                product_details = st.session_state.recommender.get_product_details(recommendations)
                
                # Display products
                cols_per_row = 3
                for i in range(0, len(product_details), cols_per_row):
                    cols = st.columns(cols_per_row)
                    for j, col in enumerate(cols):
                        if i + j < len(product_details):
                            product = product_details.iloc[i + j]
                            display_product_card(product, col)
            else:
                st.info("No recommendations available. Start shopping to get personalized suggestions!")
        
        except Exception as e:
            st.error(f"Error getting recommendations: {str(e)}")
            st.info("This may be a new user. Try exploring products to build your profile!")
    
    # Tab 2: Cart
    with tabs[1]:
        st.markdown("## 🛒 Your Shopping Cart")
        
        if st.session_state.cart:
            cart_products = st.session_state.recommender.get_product_details(st.session_state.cart)
            
            total_price = cart_products['price'].sum()
            
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f"### {len(cart_products)} items in cart")
            with col2:
                st.markdown(f"### Total: ${total_price:.2f}")
            
            st.markdown("---")
            
            for _, product in cart_products.iterrows():
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"**{product['name']}**")
                    st.markdown(f"{product['category']} - {product['brand']}")
                
                with col2:
                    st.markdown(f"**${product['price']:.2f}**")
                
                with col3:
                    if st.button("🗑️ Remove", key=f"remove_cart_{product['product_id']}"):
                        st.session_state.cart.remove(product['product_id'])
                        st.rerun()
                
                st.markdown("---")
            
            if st.button("🛍️ Proceed to Checkout", type="primary", use_container_width=True):
                st.success("Checkout functionality coming soon!")
        else:
            st.info("Your cart is empty. Start shopping!")
    
    # Tab 3: Wishlist
    with tabs[2]:
        st.markdown("## ❤️ Your Wishlist")
        
        if st.session_state.wishlist:
            wishlist_products = st.session_state.recommender.get_product_details(st.session_state.wishlist)
            
            st.markdown(f"### {len(wishlist_products)} items")
            
            cols_per_row = 3
            for i in range(0, len(wishlist_products), cols_per_row):
                cols = st.columns(cols_per_row)
                for j, col in enumerate(cols):
                    if i + j < len(wishlist_products):
                        product = wishlist_products.iloc[i + j]
                        with col:
                            st.markdown(f"""
                            <div class="product-card">
                                <div class="product-title">{product['name']}</div>
                                <span class="category-badge">{product['category']}</span>
                                <div class="product-price">${product['price']:.2f}</div>
                                <div class="product-rating">
                                    {'⭐' * int(product['rating'])} {product['rating']:.1f}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Use buttons without nested columns
                            if st.button("🛒 Add to Cart", key=f"add_from_wish_{product['product_id']}", use_container_width=True):
                                if product['product_id'] not in st.session_state.cart:
                                    st.session_state.cart.append(product['product_id'])
                                    st.success("Added to cart!")
                            
                            if st.button("🗑️ Remove from Wishlist", key=f"remove_wish_{product['product_id']}", use_container_width=True):
                                st.session_state.wishlist.remove(product['product_id'])
                                st.rerun()
        else:
            st.info("Your wishlist is empty. Add items you love!")
    
    # Tab 4: Analytics
    with tabs[3]:
        st.markdown("## 📊 Your Shopping Analytics")
        
        if st.session_state.wishlist or st.session_state.cart or st.session_state.view_history:
            all_viewed = list(set(st.session_state.wishlist + st.session_state.cart + st.session_state.view_history))
            viewed_products = st.session_state.recommender.get_product_details(all_viewed)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{len(all_viewed)}</div>
                    <div class="metric-label">Products Viewed</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                avg_price = viewed_products['price'].mean()
                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                    <div class="metric-value">${avg_price:.0f}</div>
                    <div class="metric-label">Avg. Product Price</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                total_value = (viewed_products['price'].sum() if len(st.session_state.cart) > 0 
                             else viewed_products['price'].sum())
                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                    <div class="metric-value">${total_value:.0f}</div>
                    <div class="metric-label">Total Value</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                avg_rating = viewed_products['rating'].mean()
                st.markdown(f"""
                <div class="metric-card" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">
                    <div class="metric-value">{avg_rating:.1f} ⭐</div>
                    <div class="metric-label">Avg. Rating</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Category Distribution")
                category_counts = viewed_products['category'].value_counts()
                fig = px.pie(
                    values=category_counts.values,
                    names=category_counts.index,
                    title="Your Favorite Categories",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("### Price Distribution")
                fig = px.histogram(
                    viewed_products,
                    x='price',
                    nbins=20,
                    title="Price Range of Your Interests",
                    color_discrete_sequence=['#667eea']
                )
                st.plotly_chart(fig, use_container_width=True)
            
            if len(viewed_products['brand'].unique()) > 1:
                st.markdown("### Brand Preferences")
                brand_counts = viewed_products['brand'].value_counts().head(10)
                fig = px.bar(
                    x=brand_counts.values,
                    y=brand_counts.index,
                    orientation='h',
                    title="Your Favorite Brands",
                    color=brand_counts.values,
                    color_continuous_scale='Viridis'
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📈 Start shopping to see your analytics!")
    
    # Tab 5: Explore
    with tabs[4]:
        st.markdown("## 🔍 Explore All Products")
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown("### Filters")
            
            search_query = st.text_input("🔍 Search", placeholder="Search products...")
            
            search_category = st.selectbox(
                "Category",
                options=['All'] + list(st.session_state.recommender.products_df['category'].unique())
            )
            
            search_brand = st.multiselect(
                "Brands",
                options=st.session_state.recommender.products_df['brand'].unique()
            )
            
            price_range_explore = st.slider(
                "Price ($)",
                0, 2000, (0, 2000)
            )
            
            min_rating = st.slider(
                "Min Rating",
                0.0, 5.0, 0.0, 0.5
            )
            
            sort_by = st.selectbox(
                "Sort By",
                ["Price: Low to High", "Price: High to Low", "Rating", "Reviews"]
            )
        
        with col2:
            # Filter products
            filtered = st.session_state.recommender.products_df.copy()
            
            if search_query:
                filtered = filtered[
                    filtered['name'].str.contains(search_query, case=False) |
                    filtered['description'].str.contains(search_query, case=False)
                ]
            
            if search_category != 'All':
                filtered = filtered[filtered['category'] == search_category]
            
            if search_brand:
                filtered = filtered[filtered['brand'].isin(search_brand)]
            
            filtered = filtered[
                (filtered['price'] >= price_range_explore[0]) &
                (filtered['price'] <= price_range_explore[1]) &
                (filtered['rating'] >= min_rating)
            ]
            
            # Sort
            if sort_by == "Price: Low to High":
                filtered = filtered.sort_values('price')
            elif sort_by == "Price: High to Low":
                filtered = filtered.sort_values('price', ascending=False)
            elif sort_by == "Rating":
                filtered = filtered.sort_values('rating', ascending=False)
            else:
                filtered = filtered.sort_values('num_reviews', ascending=False)
            
            st.markdown(f"### Found {len(filtered)} products")
            
            if len(filtered) == 0:
                st.warning("No products found. Try adjusting filters.")
            else:
                # Pagination
                products_per_page = 12
                num_pages = (len(filtered) - 1) // products_per_page + 1
                page = st.number_input("Page", 1, num_pages, 1)
                
                start_idx = (page - 1) * products_per_page
                end_idx = min(start_idx + products_per_page, len(filtered))
                
                page_products = filtered.iloc[start_idx:end_idx]
                
                cols_per_row = 3
                for i in range(0, len(page_products), cols_per_row):
                    cols = st.columns(cols_per_row)
                    for j, col in enumerate(cols):
                        if i + j < len(page_products):
                            product = page_products.iloc[i + j]
                            display_product_card(product, col)


def model_performance_page():
    """Model performance page"""
    st.title("📊 Model Performance & Analytics")
    
    if not load_recommender():
        return
    
    tabs = st.tabs(["📈 Performance Metrics", "🔍 Model Details"])
    
    with tabs[0]:
        st.markdown("### Recommendation System Performance")
        
        if os.path.exists('models/evaluation_results.csv'):
            eval_df = pd.read_csv('models/evaluation_results.csv')
            
            st.markdown("#### Performance Comparison")
            
            fig = go.Figure()
            metrics = ['Precision', 'Recall', 'F1-Score', 'NDCG']
            
            for metric in metrics:
                if metric in eval_df.columns:
                    fig.add_trace(go.Bar(
                        name=metric,
                        x=eval_df['Method'],
                        y=eval_df[metric],
                        text=eval_df[metric].round(4),
                        textposition='auto',
                    ))
            
            fig.update_layout(
                barmode='group',
                title="Model Performance Metrics (K=10)",
                xaxis_title="Method",
                yaxis_title="Score",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("#### Detailed Metrics")
            st.dataframe(eval_df, use_container_width=True)
        else:
            st.info("Run evaluation to see metrics")
            
            if st.button("Run Evaluation"):
                with st.spinner("Evaluating..."):
                    try:
                        evaluator = ModelEvaluator(st.session_state.recommender)
                        interactions_df = pd.read_csv('data/interactions.csv')
                        train_data, test_data = evaluator.split_data_for_evaluation(interactions_df)
                        
                        comparison = evaluator.compare_methods(test_data, k=10)
                        comparison.to_csv('models/evaluation_results.csv', index=False)
                        
                        st.success("Evaluation completed!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    
    with tabs[1]:
        st.markdown("### Model Information")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(st.session_state.recommender.products_df)}</div>
                <div class="metric-label">Total Products</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                <div class="metric-value">{len(st.session_state.recommender.user_item_matrix)}</div>
                <div class="metric-label">Total Users</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            density = (st.session_state.recommender.user_item_matrix > 0).sum().sum() / \
                     (st.session_state.recommender.user_item_matrix.shape[0] * 
                      st.session_state.recommender.user_item_matrix.shape[1])
            st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                <div class="metric-value">{density:.2%}</div>
                <div class="metric-label">Matrix Density</div>
            </div>
            """, unsafe_allow_html=True)


def main():
    """Main application"""
    if not st.session_state.authenticated:
        login_page()
    else:
        page = st.sidebar.radio(
            "Navigation",
            ["🏠 Home", "📊 Model Performance"],
            label_visibility="collapsed"
        )
        
        if page == "🏠 Home":
            recommendations_page()
        else:
            model_performance_page()


if __name__ == "__main__":
    main()