"""
ML model training script for legal document classification.
Uses scikit-learn pipeline with TF-IDF vectorization and Naive Bayes classifier.
"""

import pandas as pd
import pickle
import os
import json
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split, cross_val_score
import numpy as np

class LegalDocumentClassifier:
    """
    Legal document classification model using TF-IDF and Naive Bayes.
    """
    
    def __init__(self):
        self.pipeline = None
        self.model_info = {}
        
    def create_pipeline(self):
        """
        Create the ML pipeline with TF-IDF vectorization and Naive Bayes classifier.
        """
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(
                max_features=1000,
                stop_words=None,  # No stop words for Russian legal text
                ngram_range=(1, 2),  # Use unigrams and bigrams
                min_df=1,
                max_df=0.95
            )),
            ('classifier', MultinomialNB(alpha=1.0))
        ])
        
    def train(self, X_train, y_train):
        """
        Train the model on the provided data.
        """
        print("Training the legal document classifier...")
        
        if self.pipeline is None:
            self.create_pipeline()
        
        # Train the pipeline
        self.pipeline.fit(X_train, y_train)
        
        # Store training information
        self.model_info = {
            'training_date': datetime.now().isoformat(),
            'n_samples': len(X_train),
            'n_features': self.pipeline.named_steps['tfidf'].get_feature_names_out().shape[0],
            'classes': self.pipeline.classes_.tolist()
        }
        
        print("Model training completed!")
        
    def evaluate(self, X_test, y_test):
        """
        Evaluate the model on test data.
        """
        print("\nEvaluating model performance...")
        
        # Make predictions
        y_pred = self.pipeline.predict(X_test)
        y_proba = self.pipeline.predict_proba(X_test)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        
        # Store evaluation results
        evaluation_results = {
            'accuracy': accuracy,
            'classification_report': classification_report(y_test, y_pred, output_dict=True)
        }
        
        # Print results
        print(f"Accuracy: {accuracy:.3f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        print("\nConfusion Matrix:")
        print(cm)
        
        return evaluation_results
    
    def predict(self, texts):
        """
        Make predictions on new texts.
        """
        if self.pipeline is None:
            raise ValueError("Model not trained yet!")
        
        predictions = self.pipeline.predict(texts)
        probabilities = self.pipeline.predict_proba(texts)
        
        return predictions, probabilities
    
    def save_model(self, model_path='../src/model.pkl', info_path='../src/model_info.json'):
        """
        Save the trained model and metadata.
        """
        if self.pipeline is None:
            raise ValueError("No model to save!")
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
        # Save the model
        with open(model_path, 'wb') as f:
            pickle.dump(self.pipeline, f)
        
        # Save model information
        with open(info_path, 'w', encoding='utf-8') as f:
            json.dump(self.model_info, f, ensure_ascii=False, indent=2)
        
        print(f"Model saved to {model_path}")
        print(f"Model info saved to {info_path}")
    
    def load_model(self, model_path='../src/model.pkl'):
        """
        Load a trained model.
        """
        with open(model_path, 'rb') as f:
            self.pipeline = pickle.load(f)
        print(f"Model loaded from {model_path}")

def train_model():
    """
    Main function to train the legal document classifier.
    """
    print("=== Legal Document Classifier Training ===")
    
    # Load training data
    try:
        df = pd.read_csv('../data/training_data.csv')
        print(f"Loaded {len(df)} training samples")
    except FileNotFoundError:
        print("Training data not found. Please run prepare_data.py first.")
        return None
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        df['text'], df['category'], 
        test_size=0.2, 
        random_state=42,
        stratify=df['category']
    )
    
    print(f"Training set: {len(X_train)} samples")
    print(f"Test set: {len(X_test)} samples")
    
    # Create and train model
    classifier = LegalDocumentClassifier()
    classifier.train(X_train, y_train)
    
    # Evaluate model
    evaluation_results = classifier.evaluate(X_test, y_test)
    
    # Save model
    classifier.save_model()
    
    # Test with some examples
    print("\n=== Testing with examples ===")
    test_examples = [
        "Office space rental agreement",
        "Lawsuit for debt collection",
        "Complaint about poor service quality",
        "Income certificate request"
    ]
    
    predictions, probabilities = classifier.predict(test_examples)
    
    for i, (text, pred, prob) in enumerate(zip(test_examples, predictions, probabilities)):
        confidence = max(prob)
        print(f"Example {i+1}: '{text}' -> {pred} (confidence: {confidence:.3f})")
    
    return classifier

if __name__ == "__main__":
    train_model() 