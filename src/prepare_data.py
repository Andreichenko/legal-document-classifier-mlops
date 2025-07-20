"""
Data preparation script for legal document classification.
Creates synthetic training data for the ML model.
"""

import pandas as pd
import os
from sklearn.model_selection import train_test_split

def create_synthetic_data():
    """
    Create synthetic training data for legal document classification.
    In a real scenario, this would come from a database or file system.
    """
    
    # Synthetic legal document data
    data = {
        'text': [
            # Contracts
            'Supply agreement between ABC Corp and XYZ Ltd for goods delivery',
            'Service agreement for software development services',
            'Employment contract for full-time position',
            'Office space rental agreement',
            'Software license agreement for product usage',
            'Construction contract for building works',
            'Confidentiality agreement between parties',
            'Real estate purchase and sale agreement',
            'Agency agreement for product promotion',
            'Property insurance contract',
            
            # Lawsuits
            'Lawsuit for debt collection under contract',
            'Civil lawsuit for material damage compensation',
            'Administrative lawsuit challenging tax authority decision',
            'Divorce petition filing',
            'Consumer rights protection lawsuit',
            'Labor lawsuit for job reinstatement',
            'Lawsuit to invalidate transaction',
            'Child support collection lawsuit',
            'Administrative lawsuit to recognize decision as illegal',
            'Lawsuit for division of jointly acquired property',
            
            # Complaints
            'Complaint against tax authority official actions',
            'Complaint to prosecutor office for labor rights violation',
            'Complaint against first instance court decision',
            'Complaint to consumer protection agency for poor service',
            'Complaint against local government inaction',
            'Complaint to labor inspection for labor law violation',
            'Complaint against police officer actions',
            'Complaint to medical organization for service quality',
            'Complaint against administrative commission decision',
            'Complaint to bank for unauthorized account withdrawal',
            
            # Requests
            'Income certificate request for loan application',
            'Document request for tender participation',
            'Bank account status information request',
            'Criminal record certificate request for employment',
            'Document request for inheritance registration',
            'Tax debt information request',
            'Residence registration certificate request',
            'Document request for license acquisition',
            'Pension account status information request',
            'Family composition certificate request for benefits'
        ],
        'category': [
            # Contracts
            'contract', 'contract', 'contract', 'contract', 'contract',
            'contract', 'contract', 'contract', 'contract', 'contract',
            
            # Lawsuits
            'lawsuit', 'lawsuit', 'lawsuit', 'lawsuit', 'lawsuit',
            'lawsuit', 'lawsuit', 'lawsuit', 'lawsuit', 'lawsuit',
            
            # Complaints
            'complaint', 'complaint', 'complaint', 'complaint', 'complaint',
            'complaint', 'complaint', 'complaint', 'complaint', 'complaint',
            
            # Requests
            'request', 'request', 'request', 'request', 'request',
            'request', 'request', 'request', 'request', 'request'
        ]
    }
    
    return pd.DataFrame(data)

def prepare_data():
    """
    Prepare and save training data for the ML model.
    """
    print("Creating synthetic training data...")
    
    # Create synthetic data
    df = create_synthetic_data()
    
    # Ensure data directory exists
    os.makedirs('../data', exist_ok=True)
    
    # Save full dataset
    df.to_csv('../data/training_data.csv', index=False)
    print(f"Saved {len(df)} training samples to ../data/training_data.csv")
    
    # Display data distribution
    print("\nData distribution:")
    print(df['category'].value_counts())
    
    # Split data for training and testing
    X_train, X_test, y_train, y_test = train_test_split(
        df['text'], df['category'], 
        test_size=0.2, 
        random_state=42,
        stratify=df['category']
    )
    
    # Save split datasets
    train_df = pd.DataFrame({'text': X_train, 'category': y_train})
    test_df = pd.DataFrame({'text': X_test, 'category': y_test})
    
    train_df.to_csv('../data/train.csv', index=False)
    test_df.to_csv('../data/test.csv', index=False)
    
    print(f"\nTraining set: {len(train_df)} samples")
    print(f"Test set: {len(test_df)} samples")
    
    return df

if __name__ == "__main__":
    prepare_data() 