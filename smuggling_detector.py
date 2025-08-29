# smuggling_detector.py - Machine Learning Model for Smuggling Detection
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_recall_fscore_support
from sklearn.pipeline import Pipeline
import pickle
import re
import logging
from typing import List, Tuple, Dict, Any
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SmugglingDetector:
    """
    Machine Learning model to detect smuggling incidents from maritime event notes
    """
    
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.pipeline = None
        self.smuggling_keywords = [
            'smuggling', 'smuggle', 'smuggled', 'contraband', 'illegal cargo',
            'drug trafficking', 'drugs', 'narcotics', 'cocaine', 'heroin', 'marijuana',
            'weapons trafficking', 'arms smuggling', 'gun running', 'weapons',
            'human trafficking', 'human smuggling', 'migrants', 'undocumented',
            'cigarette smuggling', 'tobacco', 'alcohol smuggling', 'liquor',
            'fuel smuggling', 'diesel', 'petrol', 'oil smuggling',
            'wildlife smuggling', 'ivory', 'rhino horn', 'endangered species',
            'counterfeit', 'fake goods', 'pirated', 'stolen goods',
            'money laundering', 'cash smuggling', 'currency',
            'hidden compartment', 'concealed', 'secret cargo',
            'border crossing', 'illegal entry', 'unauthorized',
            'intercepted', 'seized', 'confiscated', 'arrested',
            'suspicious vessel', 'suspicious cargo', 'unusual activity'
        ]
        
    def load_data(self, csv_file: str = '2024-01-01-2024-12-31.csv') -> pd.DataFrame:
        """
        Load and prepare data for smuggling detection
        """
        logging.info("Loading data for smuggling detection...")
        
        # Load the CSV file
        df = pd.read_csv(csv_file, usecols=['Event_Date', 'Event_Type', 'Sub_Event_Type', 
                                           'Country', 'Location', 'Latitude', 'Longitude', 
                                           'Notes', 'Custom'])
        
        # Clean the Notes column
        df['Notes'] = df['Notes'].fillna('')
        df['Notes'] = df['Notes'].astype(str)
        
        logging.info(f"Loaded {len(df):,} events for analysis")
        return df
    
    def create_training_labels(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create training labels based on smuggling keywords in Notes
        """
        logging.info("Creating training labels for smuggling detection...")
        
        # Create binary labels based on smuggling keywords
        def is_smuggling(note: str) -> bool:
            note_lower = note.lower()
            return any(keyword in note_lower for keyword in self.smuggling_keywords)
        
        df['is_smuggling'] = df['Notes'].apply(is_smuggling)
        
        # Add some additional context-based rules
        smuggling_indicators = [
            'intercepted', 'seized', 'confiscated', 'arrested', 'detained',
            'suspicious', 'illegal', 'unauthorized', 'hidden', 'concealed'
        ]
        
        def has_smuggling_context(note: str) -> bool:
            note_lower = note.lower()
            return any(indicator in note_lower for indicator in smuggling_indicators)
        
        # Combine keyword detection with context
        df['smuggling_context'] = df['Notes'].apply(has_smuggling_context)
        
        # Final label: either explicit smuggling keywords or strong context
        df['smuggling_label'] = (df['is_smuggling'] | 
                                (df['smuggling_context'] & df['Notes'].str.len() > 50))
        
        smuggling_count = df['smuggling_label'].sum()
        logging.info(f"Identified {smuggling_count:,} potential smuggling incidents out of {len(df):,} total events")
        logging.info(f"Smuggling rate: {smuggling_count/len(df)*100:.2f}%")
        
        return df
    
    def preprocess_text(self, text: str) -> str:
        """
        Preprocess text for better model performance
        """
        if pd.isna(text) or text == '':
            return ''
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep important punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\-]', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def create_features(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """
        Create features and labels for training
        """
        logging.info("Creating features for machine learning model...")
        
        # Preprocess all notes
        df['processed_notes'] = df['Notes'].apply(self.preprocess_text)
        
        # Remove rows with empty notes
        df_filtered = df[df['processed_notes'].str.len() > 0].copy()
        
        # Create features
        X = df_filtered['processed_notes'].values
        y = df_filtered['smuggling_label'].values
        
        logging.info(f"Created features for {len(X):,} samples")
        logging.info(f"Positive samples (smuggling): {y.sum():,}")
        logging.info(f"Negative samples (non-smuggling): {(y == 0).sum():,}")
        
        return X, y
    
    def train_model(self, X: np.ndarray, y: np.ndarray) -> Dict[str, Any]:
        """
        Train multiple models and select the best one
        """
        logging.info("Training machine learning models...")
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Define models to try
        models = {
            'logistic_regression': Pipeline([
                ('tfidf', TfidfVectorizer(max_features=5000, ngram_range=(1, 2))),
                ('classifier', LogisticRegression(random_state=42, max_iter=1000))
            ]),
            'random_forest': Pipeline([
                ('tfidf', TfidfVectorizer(max_features=5000, ngram_range=(1, 2))),
                ('classifier', RandomForestClassifier(random_state=42, n_estimators=100))
            ]),
            'naive_bayes': Pipeline([
                ('tfidf', TfidfVectorizer(max_features=5000, ngram_range=(1, 2))),
                ('classifier', MultinomialNB())
            ])
        }
        
        # Train and evaluate each model
        results = {}
        best_model = None
        best_score = 0
        
        for name, model in models.items():
            logging.info(f"Training {name}...")
            
            # Train the model
            model.fit(X_train, y_train)
            
            # Make predictions
            y_pred = model.predict(X_test)
            
            # Calculate metrics
            accuracy = accuracy_score(y_test, y_pred)
            precision, recall, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='binary')
            
            # Cross-validation score
            cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='f1')
            cv_mean = cv_scores.mean()
            cv_std = cv_scores.std()
            
            results[name] = {
                'model': model,
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1_score': f1,
                'cv_mean': cv_mean,
                'cv_std': cv_std,
                'predictions': y_pred,
                'test_labels': y_test
            }
            
            logging.info(f"{name} - Accuracy: {accuracy:.3f}, F1: {f1:.3f}, CV F1: {cv_mean:.3f} ± {cv_std:.3f}")
            
            # Select best model based on F1 score
            if f1 > best_score:
                best_score = f1
                best_model = name
        
        # Store the best model
        self.model = results[best_model]['model']
        self.vectorizer = self.model.named_steps['tfidf']
        
        logging.info(f"Best model: {best_model} with F1 score: {best_score:.3f}")
        
        return results
    
    def evaluate_model(self, results: Dict[str, Any]) -> None:
        """
        Evaluate and display model performance
        """
        logging.info("Evaluating model performance...")
        
        for name, result in results.items():
            print(f"\n{'='*50}")
            print(f"Model: {name.upper()}")
            print(f"{'='*50}")
            print(f"Accuracy:  {result['accuracy']:.3f}")
            print(f"Precision: {result['precision']:.3f}")
            print(f"Recall:    {result['recall']:.3f}")
            print(f"F1 Score:  {result['f1_score']:.3f}")
            print(f"CV F1:     {result['cv_mean']:.3f} ± {result['cv_std']:.3f}")
            
            # Confusion matrix
            cm = confusion_matrix(result['test_labels'], result['predictions'])
            print(f"\nConfusion Matrix:")
            print(f"True Negatives:  {cm[0,0]}")
            print(f"False Positives: {cm[0,1]}")
            print(f"False Negatives: {cm[1,0]}")
            print(f"True Positives:  {cm[1,1]}")
            
            # Classification report
            print(f"\nClassification Report:")
            print(classification_report(result['test_labels'], result['predictions']))
    
    def predict_smuggling(self, notes: List[str]) -> List[bool]:
        """
        Predict smuggling for new notes
        """
        if self.model is None:
            raise ValueError("Model not trained. Please train the model first.")
        
        # Preprocess notes
        processed_notes = [self.preprocess_text(note) for note in notes]
        
        # Make predictions
        predictions = self.model.predict(processed_notes)
        probabilities = self.model.predict_proba(processed_notes)
        
        return predictions.tolist(), probabilities.tolist()
    
    def get_feature_importance(self, top_n: int = 20) -> pd.DataFrame:
        """
        Get the most important features for smuggling detection
        """
        if self.model is None:
            raise ValueError("Model not trained. Please train the model first.")
        
        # Get feature names
        feature_names = self.vectorizer.get_feature_names_out()
        
        # Get feature importance (for Random Forest)
        if hasattr(self.model.named_steps['classifier'], 'feature_importances_'):
            importances = self.model.named_steps['classifier'].feature_importances_
        else:
            # For other models, use coefficients
            importances = np.abs(self.model.named_steps['classifier'].coef_[0])
        
        # Create DataFrame
        feature_importance_df = pd.DataFrame({
            'feature': feature_names,
            'importance': importances
        }).sort_values('importance', ascending=False).head(top_n)
        
        return feature_importance_df
    
    def save_model(self, filepath: str = 'smuggling_detector_model.pkl') -> None:
        """
        Save the trained model
        """
        if self.model is None:
            raise ValueError("No model to save. Please train the model first.")
        
        model_data = {
            'model': self.model,
            'smuggling_keywords': self.smuggling_keywords,
            'vectorizer': self.vectorizer
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        
        logging.info(f"Model saved to {filepath}")
    
    def load_model(self, filepath: str = 'smuggling_detector_model.pkl') -> None:
        """
        Load a trained model
        """
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)
        
        self.model = model_data['model']
        self.vectorizer = model_data['vectorizer']
        self.smuggling_keywords = model_data['smuggling_keywords']
        
        logging.info(f"Model loaded from {filepath}")
    
    def analyze_maritime_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Analyze maritime data and add smuggling predictions
        """
        logging.info("Analyzing maritime data for smuggling detection...")
        
        # Create a copy to avoid modifying original
        df_analysis = df.copy()
        
        # Add smuggling predictions
        predictions, probabilities = self.predict_smuggling(df_analysis['Notes'].tolist())
        df_analysis['smuggling_predicted'] = predictions
        df_analysis['smuggling_probability'] = [prob[1] for prob in probabilities]
        
        # Filter for high-confidence smuggling predictions
        high_confidence_smuggling = df_analysis[
            (df_analysis['smuggling_predicted'] == True) & 
            (df_analysis['smuggling_probability'] > 0.7)
        ]
        
        logging.info(f"Found {len(high_confidence_smuggling):,} high-confidence smuggling incidents")
        
        return df_analysis, high_confidence_smuggling

def main():
    """
    Main function to train and evaluate the smuggling detection model
    """
    print("🚢 Maritime Smuggling Detection Model")
    print("=" * 50)
    
    # Initialize detector
    detector = SmugglingDetector()
    
    # Load data
    df = detector.load_data()
    
    # Create training labels
    df_labeled = detector.create_training_labels(df)
    
    # Create features
    X, y = detector.create_features(df_labeled)
    
    # Train models
    results = detector.train_model(X, y)
    
    # Evaluate models
    detector.evaluate_model(results)
    
    # Show feature importance
    print(f"\n{'='*50}")
    print("TOP FEATURES FOR SMUGGLING DETECTION")
    print(f"{'='*50}")
    feature_importance = detector.get_feature_importance(top_n=15)
    print(feature_importance.to_string(index=False))
    
    # Save the best model
    detector.save_model()
    
    # Analyze maritime data
    print(f"\n{'='*50}")
    print("ANALYZING MARITIME DATA")
    print(f"{'='*50}")
    
    # Load cleaned maritime data
    try:
        from data_cleaner import clean_maritime_data
        maritime_data = clean_maritime_data()
        maritime_df = maritime_data['df_events']
        
        # Analyze maritime data
        analyzed_df, high_confidence_smuggling = detector.analyze_maritime_data(maritime_df)
        
        print(f"Maritime events analyzed: {len(maritime_df):,}")
        print(f"Smuggling incidents detected: {analyzed_df['smuggling_predicted'].sum():,}")
        print(f"High-confidence smuggling: {len(high_confidence_smuggling):,}")
        
        if len(high_confidence_smuggling) > 0:
            print(f"\nTop 5 High-Confidence Smuggling Incidents:")
            for idx, row in high_confidence_smuggling.head().iterrows():
                print(f"\nCountry: {row['Country']}")
                print(f"Location: {row['Location']}")
                print(f"Event Type: {row['Event_Type']}")
                print(f"Confidence: {row['smuggling_probability']:.3f}")
                print(f"Notes: {row['Notes'][:200]}...")
        
    except ImportError:
        print("Could not import data_cleaner. Skipping maritime data analysis.")
    
    print(f"\n{'='*50}")
    print("MODEL TRAINING COMPLETE!")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()


