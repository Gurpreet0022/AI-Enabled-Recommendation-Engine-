"""
Authentication Module for E-commerce Recommendation System
Handles user registration, login, and session management
"""
import pandas as pd
import bcrypt
import os
import json
from datetime import datetime


class AuthManager:
    def __init__(self, users_file='data/auth_users.csv'):
        self.users_file = users_file
        self.users_df = self._load_users()
        
    def _load_users(self):
        """Load users from file"""
        if os.path.exists(self.users_file):
            return pd.read_csv(self.users_file)
        else:
            # Create new users file
            users_df = pd.DataFrame(columns=[
                'username', 'email', 'password_hash', 'user_id', 
                'created_at', 'last_login'
            ])
            return users_df
    
    def _save_users(self):
        """Save users to file"""
        os.makedirs(os.path.dirname(self.users_file), exist_ok=True)
        self.users_df.to_csv(self.users_file, index=False)
    
    def _hash_password(self, password):
        """Hash password using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def _verify_password(self, password, password_hash):
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    
    def register_user(self, username, email, password):
        """Register a new user"""
        # Check if username or email already exists
        if username in self.users_df['username'].values:
            return False, "Username already exists"
        
        if email in self.users_df['email'].values:
            return False, "Email already registered"
        
        # Validate password strength
        if len(password) < 6:
            return False, "Password must be at least 6 characters"
        
        # Generate user_id
        if len(self.users_df) == 0:
            user_id = 1
        else:
            user_id = self.users_df['user_id'].max() + 1
        
        # Hash password
        password_hash = self._hash_password(password)
        
        # Add user
        new_user = pd.DataFrame([{
            'username': username,
            'email': email,
            'password_hash': password_hash,
            'user_id': user_id,
            'created_at': datetime.now().isoformat(),
            'last_login': None
        }])
        
        self.users_df = pd.concat([self.users_df, new_user], ignore_index=True)
        self._save_users()
        
        return True, f"Account created successfully! Welcome, {username}!"
    
    def login_user(self, username, password):
        """Authenticate user"""
        user = self.users_df[self.users_df['username'] == username]
        
        if user.empty:
            return False, None, "Username not found"
        
        user = user.iloc[0]
        
        if self._verify_password(password, user['password_hash']):
            # Update last login
            self.users_df.loc[
                self.users_df['username'] == username, 
                'last_login'
            ] = datetime.now().isoformat()
            self._save_users()
            
            return True, int(user['user_id']), "Login successful!"
        else:
            return False, None, "Incorrect password"
    
    def get_user_info(self, user_id):
        """Get user information"""
        user = self.users_df[self.users_df['user_id'] == user_id]
        
        if user.empty:
            return None
        
        return user.iloc[0].to_dict()
    
    def update_password(self, username, old_password, new_password):
        """Update user password"""
        user = self.users_df[self.users_df['username'] == username]
        
        if user.empty:
            return False, "User not found"
        
        user = user.iloc[0]
        
        if not self._verify_password(old_password, user['password_hash']):
            return False, "Incorrect current password"
        
        if len(new_password) < 6:
            return False, "New password must be at least 6 characters"
        
        # Update password
        new_hash = self._hash_password(new_password)
        self.users_df.loc[
            self.users_df['username'] == username,
            'password_hash'
        ] = new_hash
        self._save_users()
        
        return True, "Password updated successfully!"


if __name__ == "__main__":
    auth = AuthManager()
    print("Authentication system initialized")
    print(f"Total users: {len(auth.users_df)}")
