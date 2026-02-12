"""
Hybrid Recommendation Engine
Combines collaborative filtering and content-based filtering
"""
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from scipy.sparse import csr_matrix
import pickle
import os


class HybridRecommender:
    def __init__(self):
        self.user_item_matrix = None
        self.item_similarity_matrix = None
        self.user_similarity_matrix = None
        self.products_df = None
        self.interactions_df = None
        self.popular_items = None
        self.scaler = StandardScaler()
        
    def load_data(self, products_path, interactions_path):
        """Load product and interaction data"""
        self.products_df = pd.read_csv(products_path)
        self.interactions_df = pd.read_csv(interactions_path)
        print(f"Loaded {len(self.products_df)} products and {len(self.interactions_df)} interactions")
        
    def build_user_item_matrix(self):
        """Build user-item interaction matrix"""
        print("Building user-item matrix...")
        
        # Aggregate interactions by user and product
        user_item_interactions = self.interactions_df.groupby(
            ['user_id', 'product_id']
        )['interaction_strength'].sum().reset_index()
        
        # Create pivot table
        self.user_item_matrix = user_item_interactions.pivot_table(
            index='user_id',
            columns='product_id',
            values='interaction_strength',
            fill_value=0
        )
        
        print(f"User-item matrix shape: {self.user_item_matrix.shape}")
        
        # Calculate popular items for cold start
        self._calculate_popular_items()
        
    def _calculate_popular_items(self):
        """Calculate most popular items based on interactions"""
        item_popularity = self.interactions_df.groupby('product_id').agg({
            'interaction_strength': 'sum',
            'user_id': 'count'
        }).rename(columns={'user_id': 'interaction_count'})
        
        # Weighted popularity score
        item_popularity['popularity_score'] = (
            item_popularity['interaction_strength'] * 0.7 + 
            item_popularity['interaction_count'] * 0.3
        )
        
        self.popular_items = item_popularity.sort_values(
            'popularity_score', ascending=False
        ).index.tolist()
        
    def build_item_similarity(self):
        """Build item-item similarity matrix using collaborative filtering"""
        print("Building item-item similarity matrix...")
        
        # Use cosine similarity on user-item matrix (transposed)
        item_similarity = cosine_similarity(self.user_item_matrix.T)
        
        self.item_similarity_matrix = pd.DataFrame(
            item_similarity,
            index=self.user_item_matrix.columns,
            columns=self.user_item_matrix.columns
        )
        
        print(f"Item similarity matrix shape: {self.item_similarity_matrix.shape}")
        
    def build_user_similarity(self):
        """Build user-user similarity matrix"""
        print("Building user-user similarity matrix...")
        
        # Use cosine similarity on user-item matrix
        user_similarity = cosine_similarity(self.user_item_matrix)
        
        self.user_similarity_matrix = pd.DataFrame(
            user_similarity,
            index=self.user_item_matrix.index,
            columns=self.user_item_matrix.index
        )
        
        print(f"User similarity matrix shape: {self.user_similarity_matrix.shape}")
        
    def build_content_similarity(self):
        """Build content-based similarity using product features"""
        print("Building content-based similarity...")
        
        # One-hot encode categorical features
        category_encoded = pd.get_dummies(self.products_df['category'], prefix='cat')
        brand_encoded = pd.get_dummies(self.products_df['brand'], prefix='brand')
        
        # Normalize numerical features
        numerical_features = self.products_df[['price', 'rating']].copy()
        numerical_features['price'] = self.scaler.fit_transform(
            numerical_features[['price']]
        )
        
        # Combine features
        product_features = pd.concat([
            self.products_df[['product_id']],
            category_encoded,
            brand_encoded,
            numerical_features
        ], axis=1)
        
        # Calculate content similarity
        product_features_matrix = product_features.drop('product_id', axis=1).values
        content_similarity = cosine_similarity(product_features_matrix)
        
        self.content_similarity_matrix = pd.DataFrame(
            content_similarity,
            index=self.products_df['product_id'],
            columns=self.products_df['product_id']
        )
        
        print(f"Content similarity matrix shape: {self.content_similarity_matrix.shape}")
        
    def train(self, products_path, interactions_path):
        """Train the recommendation model"""
        print("="*50)
        print("Training Hybrid Recommendation System")
        print("="*50)
        
        self.load_data(products_path, interactions_path)
        self.build_user_item_matrix()
        self.build_item_similarity()
        self.build_user_similarity()
        self.build_content_similarity()
        
        print("\nTraining completed!")
        
    def get_item_based_recommendations(self, user_id, top_n=10):
        """Get recommendations using item-based collaborative filtering"""
        if user_id not in self.user_item_matrix.index:
            return []
        
        # Get user's interaction history
        user_interactions = self.user_item_matrix.loc[user_id]
        interacted_items = user_interactions[user_interactions > 0].index.tolist()
        
        if not interacted_items:
            return []
        
        # Calculate scores for all items
        item_scores = pd.Series(0.0, index=self.item_similarity_matrix.index)
        
        for item_id in interacted_items:
            if item_id in self.item_similarity_matrix.index:
                # Weight by user's interaction strength
                weight = user_interactions[item_id]
                item_scores += self.item_similarity_matrix[item_id] * weight
        
        # Remove already interacted items
        item_scores = item_scores.drop(interacted_items, errors='ignore')
        
        # Get top N
        top_items = item_scores.sort_values(ascending=False).head(top_n)
        
        return top_items.index.tolist()
    
    def get_user_based_recommendations(self, user_id, top_n=10):
        """Get recommendations using user-based collaborative filtering"""
        if user_id not in self.user_similarity_matrix.index:
            return []
        
        # Get similar users
        similar_users = self.user_similarity_matrix[user_id].sort_values(ascending=False)[1:11]
        
        # Get items liked by similar users
        user_interactions = self.user_item_matrix.loc[user_id]
        interacted_items = user_interactions[user_interactions > 0].index.tolist()
        
        item_scores = pd.Series(0.0, index=self.user_item_matrix.columns)
        
        for similar_user_id, similarity in similar_users.items():
            similar_user_items = self.user_item_matrix.loc[similar_user_id]
            item_scores += similar_user_items * similarity
        
        # Remove already interacted items
        item_scores = item_scores.drop(interacted_items, errors='ignore')
        
        # Get top N
        top_items = item_scores.sort_values(ascending=False).head(top_n)
        
        return top_items.index.tolist()
    
    def get_content_based_recommendations(self, user_id, top_n=10):
        """Get recommendations using content-based filtering"""
        if user_id not in self.user_item_matrix.index:
            return []
        
        # Get user's interaction history
        user_interactions = self.user_item_matrix.loc[user_id]
        interacted_items = user_interactions[user_interactions > 0].index.tolist()
        
        if not interacted_items:
            return []
        
        # Calculate scores based on content similarity
        item_scores = pd.Series(0.0, index=self.content_similarity_matrix.index)
        
        for item_id in interacted_items:
            if item_id in self.content_similarity_matrix.index:
                weight = user_interactions[item_id]
                item_scores += self.content_similarity_matrix[item_id] * weight
        
        # Remove already interacted items
        item_scores = item_scores.drop(interacted_items, errors='ignore')
        
        # Get top N
        top_items = item_scores.sort_values(ascending=False).head(top_n)
        
        return top_items.index.tolist()
    
    def get_hybrid_recommendations(self, user_id, top_n=10, 
                                   item_weight=0.4, user_weight=0.3, content_weight=0.3):
        """Get hybrid recommendations combining all methods"""
        # Get recommendations from each method
        item_based = self.get_item_based_recommendations(user_id, top_n * 2)
        user_based = self.get_user_based_recommendations(user_id, top_n * 2)
        content_based = self.get_content_based_recommendations(user_id, top_n * 2)
        
        # Combine recommendations with weighted voting
        item_scores = {}
        
        for i, item_id in enumerate(item_based):
            item_scores[item_id] = item_scores.get(item_id, 0) + (len(item_based) - i) * item_weight
        
        for i, item_id in enumerate(user_based):
            item_scores[item_id] = item_scores.get(item_id, 0) + (len(user_based) - i) * user_weight
        
        for i, item_id in enumerate(content_based):
            item_scores[item_id] = item_scores.get(item_id, 0) + (len(content_based) - i) * content_weight
        
        # Sort by combined score
        sorted_items = sorted(item_scores.items(), key=lambda x: x[1], reverse=True)
        
        return [item_id for item_id, score in sorted_items[:top_n]]
    
    def get_recommendations(self, user_id, top_n=10, method='hybrid'):
        """Get recommendations for a user"""
        # Check if new user (not in training data)
        if user_id not in self.user_item_matrix.index:
            return self.get_popular_recommendations(top_n)
        
        if method == 'item_based':
            recommendations = self.get_item_based_recommendations(user_id, top_n)
        elif method == 'user_based':
            recommendations = self.get_user_based_recommendations(user_id, top_n)
        elif method == 'content_based':
            recommendations = self.get_content_based_recommendations(user_id, top_n)
        else:  # hybrid
            recommendations = self.get_hybrid_recommendations(user_id, top_n)
        
        # If no recommendations, return popular items
        if not recommendations:
            return self.get_popular_recommendations(top_n)
        
        return recommendations
    
    def get_popular_recommendations(self, top_n=10):
        """Get popular items for cold start users"""
        return self.popular_items[:top_n]
    
    def get_product_details(self, product_ids):
        """Get product details for given IDs"""
        return self.products_df[self.products_df['product_id'].isin(product_ids)]
    
    def save_model(self, model_dir='models'):
        """Save trained model"""
        os.makedirs(model_dir, exist_ok=True)
        
        model_data = {
            'user_item_matrix': self.user_item_matrix,
            'item_similarity_matrix': self.item_similarity_matrix,
            'user_similarity_matrix': self.user_similarity_matrix,
            'content_similarity_matrix': self.content_similarity_matrix,
            'popular_items': self.popular_items,
            'scaler': self.scaler
        }
        
        with open(f'{model_dir}/recommender_model.pkl', 'wb') as f:
            pickle.dump(model_data, f)
        
        # Save products separately for easy access
        self.products_df.to_csv(f'{model_dir}/products.csv', index=False)
        
        print(f"Model saved to {model_dir}/")
    
    def load_model(self, model_dir='models'):
        """Load trained model"""
        with open(f'{model_dir}/recommender_model.pkl', 'rb') as f:
            model_data = pickle.load(f)
        
        self.user_item_matrix = model_data['user_item_matrix']
        self.item_similarity_matrix = model_data['item_similarity_matrix']
        self.user_similarity_matrix = model_data['user_similarity_matrix']
        self.content_similarity_matrix = model_data['content_similarity_matrix']
        self.popular_items = model_data['popular_items']
        self.scaler = model_data['scaler']
        
        # Load products
        self.products_df = pd.read_csv(f'{model_dir}/products.csv')
        
        print(f"Model loaded from {model_dir}/")


if __name__ == "__main__":
    # Train and save model
    recommender = HybridRecommender()
    recommender.train('data/products.csv', 'data/interactions.csv')
    recommender.save_model()
    
    # Test recommendations
    print("\n" + "="*50)
    print("Testing Recommendations")
    print("="*50)
    
    test_user_id = 1
    recommendations = recommender.get_recommendations(test_user_id, top_n=10)
    product_details = recommender.get_product_details(recommendations)
    
    print(f"\nTop 10 recommendations for User {test_user_id}:")
    print(product_details[['product_id', 'name', 'category', 'price', 'rating']])
