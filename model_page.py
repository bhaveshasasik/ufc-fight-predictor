import pandas as pd
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

class UFCModelPredictor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.models = {
            "Logistic Regression": LogisticRegression(),
            "K-Nearest Neighbors": KNeighborsClassifier(),
            "Support Vector Machine": SVC(),
            "Decision Tree": DecisionTreeClassifier(),
            "Random Forest": RandomForestClassifier(n_estimators=100),
            "Gradient Boosting": GradientBoostingClassifier()
        }
        self.results = {}
        self.best_model = None
        self.fighters = None
        self.X_train = self.X_test = self.y_train = self.y_test = None
        self.scaler = StandardScaler()

    def load_and_prepare_data(self):
        ufc_df = pd.read_csv(self.file_path)
        ufc_df.dropna(inplace=True)
        categorical_cols = ufc_df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            ufc_df[col] = LabelEncoder().fit_transform(ufc_df[col])

        self.fighters = ufc_df[['wins_r', 'losses_r', 'draws_r', 'height_cm_r', 'weight_in_kg_r', 'reach_in_cm_r', 'stance_r', 
                                'significant_strikes_landed_per_minute_r', 'significant_striking_accuracy_r', 
                                'significant_strikes_absorbed_per_minute_r', 'significant_strike_defence_r', 
                                'average_takedowns_landed_per_15_minutes_r', 'takedown_accuracy_r', 'takedown_defense_r', 
                                'average_submissions_attempted_per_15_minutes_r', 'wins_b', 'losses_b', 'draws_b', 
                                'height_cm_b', 'weight_in_kg_b', 'reach_in_cm_b', 'stance_b', 
                                'significant_strikes_landed_per_minute_b', 'significant_striking_accuracy_b', 
                                'significant_strikes_absorbed_per_minute_b', 'significant_strike_defence_b', 
                                'average_takedowns_landed_per_15_minutes_b', 'takedown_accuracy_b', 'takedown_defense_b', 
                                'average_submissions_attempted_per_15_minutes_b']]

        X = ufc_df.drop('Winner', axis=1)
        y = ufc_df['Winner']

        X_scaled = self.scaler.fit_transform(X)

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    def test_models(self, silent=False):
        
        self.results = {}
        for name, model in self.models.items():
            accuracy = self.evaluate_model(model)
            self.results[name] = accuracy
            if not silent:
                st.write(f'{name} Accuracy: {accuracy:.4f}')


        self.best_model = max(self.results, key=self.results.get)
        
    def evaluate_model(self, model):
        model.fit(self.X_train, self.y_train)
        predictions = model.predict(self.X_test)
        return accuracy_score(self.y_test, predictions)
    
    def predict_winner(self, fighter_r, fighter_b):
        fighter_r_columns = ['wins_r', 'losses_r', 'draws_r', 'height_cm_r', 'weight_in_kg_r', 'reach_in_cm_r', 'stance_r', 
                             'significant_strikes_landed_per_minute_r', 'significant_striking_accuracy_r', 
                             'significant_strikes_absorbed_per_minute_r', 'significant_strike_defence_r', 
                             'average_takedowns_landed_per_15_minutes_r', 'takedown_accuracy_r', 'takedown_defense_r', 
                             'average_submissions_attempted_per_15_minutes_r']
    
        fighter_b_columns = ['wins_b', 'losses_b', 'draws_b', 'height_cm_b', 'weight_in_kg_b', 'reach_in_cm_b', 'stance_b', 
                             'significant_strikes_landed_per_minute_b', 'significant_striking_accuracy_b', 
                             'significant_strikes_absorbed_per_minute_b', 'significant_strike_defence_b', 
                             'average_takedowns_landed_per_15_minutes_b', 'takedown_accuracy_b', 'takedown_defense_b', 
                             'average_submissions_attempted_per_15_minutes_b']

        combined_features = fighter_r + fighter_b

        # Correct the condition check: len(fighter_r_columns) + len(fighter_b_columns)
        if len(combined_features) != len(fighter_r_columns) + len(fighter_b_columns):
            raise ValueError(f"Expected {len(fighter_r_columns) + len(fighter_b_columns)} features, got {len(combined_features)}")

        data = [combined_features]
        data_scaled = self.scaler.transform(data)
        model = self.models[self.best_model]
        prediction = model.predict(data_scaled)
        return 'Red Fighter' if prediction == 1 else 'Blue Fighter'
