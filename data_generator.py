"""
Data Generator for E-commerce Recommendation System
Generates synthetic product and interaction data
"""
import pandas as pd
import numpy as np
import pickle
import os

class EcommerceDataGenerator:
    def __init__(self, seed=42):
        np.random.seed(seed)
        self.categories = {
            'Electronics': ['Smartphone', 'Laptop', 'Tablet', 'Smartwatch', 'Headphones', 
                          'Camera', 'Speaker', 'Monitor', 'Keyboard', 'Mouse'],
            'Fashion': ['T-Shirt', 'Jeans', 'Dress', 'Jacket', 'Shoes', 
                       'Sneakers', 'Watch', 'Sunglasses', 'Belt', 'Bag'],
            'Beauty': ['Moisturizer', 'Serum', 'Cleanser', 'Sunscreen', 'Face Mask',
                      'Lipstick', 'Foundation', 'Eye Shadow', 'Perfume', 'Body Lotion'],
            'Home': ['Coffee Maker', 'Blender', 'Vacuum', 'Air Purifier', 'Lamp',
                    'Pillow', 'Blanket', 'Curtains', 'Rug', 'Mirror']
        }
        
        self.brands = {
            'Electronics': ['TechPro', 'DigiMax', 'SmartLife', 'ElectroHub', 'GadgetZone'],
            'Fashion': ['StyleHub', 'UrbanWear', 'TrendSet', 'FashionFit', 'ChicStyle'],
            'Beauty': ['GlowLab', 'PureBeauty', 'RadiantSkin', 'BeautyEssence', 'LuxeGlow'],
            'Home': ['HomeComfort', 'LivingSpace', 'CozyNest', 'ModernHome', 'SmartLiving']
        }
        
    def generate_products(self, num_products=500):
        """Generate synthetic product catalog"""
        products = []
        product_id = 1
        
        for category, product_types in self.categories.items():
            products_per_type = num_products // (len(self.categories) * len(product_types))
            
            for product_type in product_types:
                for i in range(products_per_type):
                    brand = np.random.choice(self.brands[category])
                    
                    # Generate price based on category
                    if category == 'Electronics':
                        base_price = np.random.uniform(50, 2000)
                    elif category == 'Fashion':
                        base_price = np.random.uniform(20, 300)
                    elif category == 'Beauty':
                        base_price = np.random.uniform(10, 150)
                    else:  # Home
                        base_price = np.random.uniform(30, 500)
                    
                    price = round(base_price, 2)
                    rating = round(np.random.uniform(3.0, 5.0), 1)
                    num_reviews = np.random.randint(0, 1000)
                    
                    products.append({
                        'product_id': product_id,
                        'name': f"{brand} {product_type}",
                        'category': category,
                        'sub_category': product_type,
                        'brand': brand,
                        'price': price,
                        'rating': rating,
                        'num_reviews': num_reviews,
                        'description': f"High-quality {product_type.lower()} from {brand}"
                    })
                    product_id += 1
        
        return pd.DataFrame(products)
    
    def generate_users(self, num_users=1000):
        """Generate synthetic user data"""
        users = []
        
        for user_id in range(1, num_users + 1):
            # User preferences (which categories they prefer)
            preferred_categories = np.random.choice(
                list(self.categories.keys()), 
                size=np.random.randint(1, 3),
                replace=False
            ).tolist()
            
            users.append({
                'user_id': user_id,
                'preferred_categories': preferred_categories,
                'avg_purchase_value': round(np.random.uniform(50, 500), 2),
                'activity_level': np.random.choice(['low', 'medium', 'high'], p=[0.3, 0.5, 0.2])
            })
        
        return pd.DataFrame(users)
    
    def generate_interactions(self, products_df, users_df, num_interactions=50000):
        """Generate synthetic user-product interactions"""
        interactions = []
        event_types = ['view', 'addtocart', 'transaction']
        event_strength = {'view': 1, 'addtocart': 2, 'transaction': 3}
        
        product_ids = products_df['product_id'].tolist()
        user_ids = users_df['user_id'].tolist()
        
        # Create interactions based on user preferences
        for _ in range(num_interactions):
            user_id = np.random.choice(user_ids)
            user_prefs = users_df[users_df['user_id'] == user_id]['preferred_categories'].iloc[0]
            
            # 70% chance to interact with preferred category
            if np.random.random() < 0.7 and user_prefs:
                category = np.random.choice(user_prefs)
                product_id = np.random.choice(
                    products_df[products_df['category'] == category]['product_id'].tolist()
                )
            else:
                product_id = np.random.choice(product_ids)
            
            # Event type probabilities: view (60%), addtocart (30%), transaction (10%)
            event = np.random.choice(event_types, p=[0.6, 0.3, 0.1])
            
            interactions.append({
                'user_id': user_id,
                'product_id': product_id,
                'event': event,
                'interaction_strength': event_strength[event],
                'timestamp': pd.Timestamp.now() - pd.Timedelta(days=np.random.randint(0, 90))
            })
        
        return pd.DataFrame(interactions)
    
    def generate_dataset(self, num_products=500, num_users=1000, num_interactions=50000):
        """Generate complete dataset"""
        print("Generating products...")
        products_df = self.generate_products(num_products)
        
        print("Generating users...")
        users_df = self.generate_users(num_users)
        
        print("Generating interactions...")
        interactions_df = self.generate_interactions(products_df, users_df, num_interactions)
        
        return products_df, users_df, interactions_df
    
    def save_dataset(self, products_df, users_df, interactions_df, data_dir='data'):
        """Save dataset to files"""
        os.makedirs(data_dir, exist_ok=True)
        
        products_df.to_csv(f'{data_dir}/products.csv', index=False)
        users_df.to_csv(f'{data_dir}/users.csv', index=False)
        interactions_df.to_csv(f'{data_dir}/interactions.csv', index=False)
        
        print(f"Dataset saved to {data_dir}/")
        print(f"  - Products: {len(products_df)}")
        print(f"  - Users: {len(users_df)}")
        print(f"  - Interactions: {len(interactions_df)}")


if __name__ == "__main__":
    generator = EcommerceDataGenerator()
    products_df, users_df, interactions_df = generator.generate_dataset(
        num_products=500,
        num_users=1000,
        num_interactions=50000
    )
    generator.save_dataset(products_df, users_df, interactions_df)
