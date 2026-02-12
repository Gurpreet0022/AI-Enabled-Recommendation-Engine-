"""
Model Evaluator for Recommendation System
Computes precision, recall, F1-score, and other metrics
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


class ModelEvaluator:
    def __init__(self, recommender):
        self.recommender = recommender
        self.metrics = {}
        
    def precision_at_k(self, recommended, relevant, k):
        """Calculate Precision@K"""
        recommended_k = recommended[:k]
        relevant_recommended = set(recommended_k) & set(relevant)
        
        if len(recommended_k) == 0:
            return 0.0
        
        return len(relevant_recommended) / len(recommended_k)
    
    def recall_at_k(self, recommended, relevant, k):
        """Calculate Recall@K"""
        recommended_k = recommended[:k]
        relevant_recommended = set(recommended_k) & set(relevant)
        
        if len(relevant) == 0:
            return 0.0
        
        return len(relevant_recommended) / len(relevant)
    
    def f1_at_k(self, precision, recall):
        """Calculate F1-Score"""
        if precision + recall == 0:
            return 0.0
        
        return 2 * (precision * recall) / (precision + recall)
    
    def ndcg_at_k(self, recommended, relevant, k):
        """Calculate Normalized Discounted Cumulative Gain@K"""
        recommended_k = recommended[:k]
        
        dcg = 0.0
        for i, item in enumerate(recommended_k):
            if item in relevant:
                dcg += 1.0 / np.log2(i + 2)
        
        # Ideal DCG
        idcg = sum([1.0 / np.log2(i + 2) for i in range(min(len(relevant), k))])
        
        if idcg == 0:
            return 0.0
        
        return dcg / idcg
    
    def evaluate_recommendations(self, test_data, k_values=[5, 10, 20], method='hybrid'):
        """Evaluate recommendation system"""
        print("="*50)
        print(f"Evaluating {method.upper()} Recommendations")
        print("="*50)
        
        results = {k: {'precision': [], 'recall': [], 'f1': [], 'ndcg': []} 
                  for k in k_values}
        
        # Get unique users in test data
        test_users = test_data['user_id'].unique()
        evaluated_users = 0
        
        for user_id in test_users:
            # Get relevant items for this user (items they interacted with in test set)
            relevant_items = test_data[test_data['user_id'] == user_id]['product_id'].tolist()
            
            if not relevant_items:
                continue
            
            # Get recommendations
            try:
                recommendations = self.recommender.get_recommendations(
                    user_id, 
                    top_n=max(k_values),
                    method=method
                )
                
                if not recommendations:
                    continue
                
                # Calculate metrics for each k
                for k in k_values:
                    precision = self.precision_at_k(recommendations, relevant_items, k)
                    recall = self.recall_at_k(recommendations, relevant_items, k)
                    f1 = self.f1_at_k(precision, recall)
                    ndcg = self.ndcg_at_k(recommendations, relevant_items, k)
                    
                    results[k]['precision'].append(precision)
                    results[k]['recall'].append(recall)
                    results[k]['f1'].append(f1)
                    results[k]['ndcg'].append(ndcg)
                
                evaluated_users += 1
                
                if evaluated_users % 100 == 0:
                    print(f"Evaluated {evaluated_users} users...")
                    
            except Exception as e:
                continue
        
        # Calculate average metrics
        print(f"\nTotal users evaluated: {evaluated_users}")
        print("\nResults:")
        print("-"*50)
        
        evaluation_summary = []
        
        for k in k_values:
            avg_metrics = {
                'K': k,
                'Precision': np.mean(results[k]['precision']),
                'Recall': np.mean(results[k]['recall']),
                'F1-Score': np.mean(results[k]['f1']),
                'NDCG': np.mean(results[k]['ndcg'])
            }
            
            evaluation_summary.append(avg_metrics)
            
            print(f"\nK = {k}:")
            print(f"  Precision@{k}: {avg_metrics['Precision']:.4f}")
            print(f"  Recall@{k}:    {avg_metrics['Recall']:.4f}")
            print(f"  F1-Score@{k}:  {avg_metrics['F1-Score']:.4f}")
            print(f"  NDCG@{k}:      {avg_metrics['NDCG']:.4f}")
        
        self.metrics[method] = evaluation_summary
        
        return pd.DataFrame(evaluation_summary)
    
    def split_data_for_evaluation(self, interactions_df, test_ratio=0.2):
        """Split interactions into train and test sets"""
        print("Splitting data for evaluation...")
        
        train_data = []
        test_data = []
        
        # Split per user
        for user_id in interactions_df['user_id'].unique():
            user_interactions = interactions_df[interactions_df['user_id'] == user_id]
            
            if len(user_interactions) < 3:  # Need minimum interactions
                train_data.append(user_interactions)
                continue
            
            # Sort by timestamp if available
            if 'timestamp' in user_interactions.columns:
                user_interactions = user_interactions.sort_values('timestamp')
            
            # Split
            n_test = max(1, int(len(user_interactions) * test_ratio))
            test_data.append(user_interactions.iloc[-n_test:])
            train_data.append(user_interactions.iloc[:-n_test])
        
        train_df = pd.concat(train_data, ignore_index=True)
        test_df = pd.concat(test_data, ignore_index=True)
        
        print(f"Train set: {len(train_df)} interactions")
        print(f"Test set: {len(test_df)} interactions")
        
        return train_df, test_df
    
    def compare_methods(self, test_data, k=10):
        """Compare different recommendation methods"""
        print("\n" + "="*50)
        print("Comparing Recommendation Methods")
        print("="*50)
        
        methods = ['item_based', 'user_based', 'content_based', 'hybrid']
        comparison_results = []
        
        for method in methods:
            print(f"\nEvaluating {method}...")
            results = self.evaluate_recommendations(test_data, k_values=[k], method=method)
            comparison_results.append({
                'Method': method.replace('_', ' ').title(),
                'Precision': results.iloc[0]['Precision'],
                'Recall': results.iloc[0]['Recall'],
                'F1-Score': results.iloc[0]['F1-Score'],
                'NDCG': results.iloc[0]['NDCG']
            })
        
        comparison_df = pd.DataFrame(comparison_results)
        
        print("\n" + "="*50)
        print("Method Comparison Summary")
        print("="*50)
        print(comparison_df.to_string(index=False))
        
        return comparison_df
    
    def get_coverage(self, test_users, top_n=10, method='hybrid'):
        """Calculate catalog coverage"""
        all_recommended = set()
        total_products = len(self.recommender.products_df)
        
        for user_id in test_users:
            recommendations = self.recommender.get_recommendations(
                user_id, 
                top_n=top_n,
                method=method
            )
            all_recommended.update(recommendations)
        
        coverage = len(all_recommended) / total_products
        
        print(f"\nCatalog Coverage: {coverage:.4f}")
        print(f"Unique items recommended: {len(all_recommended)} out of {total_products}")
        
        return coverage


if __name__ == "__main__":
    from recommender import HybridRecommender
    
    # Load model
    recommender = HybridRecommender()
    recommender.load_model()
    
    # Load interactions
    interactions_df = pd.read_csv('data/interactions.csv')
    
    # Split data
    evaluator = ModelEvaluator(recommender)
    train_data, test_data = evaluator.split_data_for_evaluation(interactions_df)
    
    # Retrain on train data only
    print("\nRetraining model on train data...")
    recommender.train_on_split(train_data)
    
    # Evaluate
    comparison = evaluator.compare_methods(test_data, k=10)
