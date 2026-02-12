"""
Setup Script for E-commerce Recommendation System
Initializes data, trains model, and prepares the system
"""
import os
import sys
from data_generator import EcommerceDataGenerator
from recommender import HybridRecommender
from evaluator import ModelEvaluator
from auth import AuthManager
import pandas as pd


def setup_system():
    """Complete system setup"""
    print("="*70)
    print("E-COMMERCE RECOMMENDATION SYSTEM SETUP")
    print("="*70)
    
    # Step 1: Generate synthetic data
    print("\n[1/5] Generating synthetic e-commerce data...")
    generator = EcommerceDataGenerator(seed=42)
    
    products_df, users_df, interactions_df = generator.generate_dataset(
        num_products=500,      # Adjust as needed
        num_users=1000,        # Adjust as needed
        num_interactions=50000 # Adjust as needed
    )
    
    generator.save_dataset(products_df, users_df, interactions_df, data_dir='data')
    print("✓ Data generation completed!")
    
    # Step 2: Train recommendation model
    print("\n[2/5] Training recommendation model...")
    recommender = HybridRecommender()
    recommender.train('data/products.csv', 'data/interactions.csv')
    recommender.save_model('models')
    print("✓ Model training completed!")
    
    # Step 3: Evaluate model
    print("\n[3/5] Evaluating model performance...")
    try:
        evaluator = ModelEvaluator(recommender)
        train_data, test_data = evaluator.split_data_for_evaluation(interactions_df, test_ratio=0.2)
        
        # Retrain on train data for proper evaluation
        print("   Retraining on train split...")
        recommender_eval = HybridRecommender()
        recommender_eval.load_data('data/products.csv', 'data/interactions.csv')
        recommender_eval.interactions_df = train_data
        recommender_eval.build_user_item_matrix()
        recommender_eval.build_item_similarity()
        recommender_eval.build_user_similarity()
        recommender_eval.build_content_similarity()
        
        # Evaluate
        evaluator_new = ModelEvaluator(recommender_eval)
        comparison = evaluator_new.compare_methods(test_data, k=10)
        comparison.to_csv('models/evaluation_results.csv', index=False)
        print("✓ Model evaluation completed!")
    except Exception as e:
        print(f"⚠ Warning: Evaluation failed: {str(e)}")
        print("   Continuing with setup...")
    
    # Step 4: Setup authentication
    print("\n[4/5] Setting up authentication system...")
    auth = AuthManager()
    print("✓ Authentication setup completed!")
    
    # Step 5: Test recommendations
    print("\n[5/5] Testing recommendation system...")
    test_user_id = 1
    recommendations = recommender.get_recommendations(test_user_id, top_n=5)
    
    if recommendations:
        product_details = recommender.get_product_details(recommendations)
        print(f"\n   Sample recommendations for User {test_user_id}:")
        print(product_details[['name', 'category', 'price']].to_string(index=False))
    
    print("\n✓ System test completed!")
    
    # Summary
    print("\n" + "="*70)
    print("SETUP COMPLETED SUCCESSFULLY!")
    print("="*70)
    print("\nSystem Statistics:")
    print(f"  • Products: {len(products_df)}")
    print(f"  • Users: {len(users_df)}")
    print(f"  • Interactions: {len(interactions_df)}")
    print(f"  • Model Size: {os.path.getsize('models/recommender_model.pkl') / (1024*1024):.2f} MB")
    
    print("\nTo start the application, run:")
    print("  streamlit run app.py")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    try:
        setup_system()
    except Exception as e:
        print(f"\n❌ Setup failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
