"""
Nombre del archivo: models.py
Autores: Montserrat Lopez, Victor Bassas,  Andres  Henao
Descripción: Archivo que contiene código útil para tranformar datos para
            proyecto de curso Data Scientist de la UOC
Creado: 28/10/2024
Versión: 1.0
Correos: cutmountain@uoc.edu, vbassasb@uoc.edu, ahenaoa@uoc.edu
"""

import pickle
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report, confusion_matrix
from imblearn.over_sampling import SMOTE


class ModelEvaluation:
    def __init__(self, cash_df):
        self.cash_df = cash_df
        self.X_train, self.X_test, self.y_train, self.y_test = self.train_test_split()
        self.logistic_model = None
        self.gb_model = None

    def train_test_split(self):
        """
        Splits the data into train and test sets.
        """
        X = self.cash_df.drop(columns=['status'])
        y = self.cash_df['status']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        return X_train, X_test, y_train, y_test

    def train_and_evaluate_models(self):
        """
        Trains both models and evaluates them on the test set.
        """
        # Handle Imbalance with SMOTE
        smote = SMOTE(random_state=42)
        X_train_balanced, y_train_balanced = smote.fit_resample(self.X_train, self.y_train)

        # Logistic Regression
        self.logistic_model = LogisticRegression(class_weight='balanced', random_state=42)
        self.logistic_model.fit(X_train_balanced, y_train_balanced)

        # Gradient Boosting
        self.gb_model = GradientBoostingClassifier(random_state=42)
        self.gb_model.fit(X_train_balanced, y_train_balanced)

        # Evaluate both models
        print("### Logistic Regression Results ###")
        self.evaluate_model(self.logistic_model, self.X_test, self.y_test)

        print("\n### Gradient Boosting Results ###")
        self.evaluate_model(self.gb_model, self.X_test, self.y_test)

    def evaluate_model(self, model, X_test, y_test):
        """
        Prints classification report and confusion matrix for a given model.
        """
        y_pred = model.predict(X_test)
        print("Classification Report:")
        print(classification_report(y_test, y_pred, target_names=['money_back', 'rejected']))
        print("\nConfusion Matrix:")
        print(confusion_matrix(y_test, y_pred))

    def plot_evaluations(self):
        """
        Generates and displays various evaluation plots.
        """
        feature_names = self.X_train.columns

        # Logistic Regression Feature Importance
        print("Logistic Regression Feature Importance:")
        self.plot_logistic_regression_importance(self.logistic_model, feature_names)

        # Gradient Boosting Feature Importance
        print("Gradient Boosting Feature Importance:")
        self.plot_gradient_boosting_importance(self.gb_model, feature_names)

        # Confusion Matrices
        print("Logistic Regression Confusion Matrix:")
        self.plot_confusion_matrix(self.y_test, self.logistic_model.predict(self.X_test), "Logistic Regression Confusion Matrix")

        print("Gradient Boosting Confusion Matrix:")
        self.plot_confusion_matrix(self.y_test, self.gb_model.predict(self.X_test), "Gradient Boosting Confusion Matrix")

        # Predicted Probabilities
        print("Logistic Regression Predicted Probabilities:")
        self.plot_predictions(self.y_test, self.logistic_model.predict_proba(self.X_test), "Logistic Regression Predicted Probabilities")

        print("Gradient Boosting Predicted Probabilities:")
        self.plot_predictions(self.y_test, self.gb_model.predict_proba(self.X_test), "Gradient Boosting Predicted Probabilities")

    def plot_logistic_regression_importance(self, model, feature_names):
        """
        Plot feature importance for Logistic Regression model.
        """
        coeffs = model.coef_[0]
        importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': coeffs})
        importance_df.sort_values(by='Importance', key=abs, ascending=False, inplace=True)

        plt.figure(figsize=(8, 5))
        sns.barplot(data=importance_df, x='Importance', y='Feature', palette='coolwarm')
        plt.title("Feature Importance - Logistic Regression")
        plt.xlabel("Coefficient Value")
        plt.ylabel("Feature")
        plt.show()

    def plot_gradient_boosting_importance(self, model, feature_names):
        """
        Plot feature importance for Gradient Boosting model.
        """
        importance = model.feature_importances_
        importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': importance})
        importance_df.sort_values(by='Importance', ascending=False, inplace=True)

        plt.figure(figsize=(8, 5))
        sns.barplot(data=importance_df, x='Importance', y='Feature', palette='viridis')
        plt.title("Feature Importance - Gradient Boosting")
        plt.xlabel("Importance Score")
        plt.ylabel("Feature")
        plt.show()

    def plot_confusion_matrix(self, y_true, y_pred, title):
        """
        Plot confusion matrix as heatmap.
        """
        cm = confusion_matrix(y_true, y_pred)
        plt.figure(figsize=(6, 4))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['money_back', 'rejected'],
                    yticklabels=['money_back', 'rejected'])
        plt.title(title)
        plt.xlabel("Predicted")
        plt.ylabel("Actual")
        plt.show()

    def plot_predictions(self, y_test, y_prob, title):
        """
        Plot the predicted probabilities.
        """
        plt.figure(figsize=(8, 5))
        sns.histplot(y_prob[:, 1], bins=30, kde=True, color='purple', label='Predicted Probability of Rejected')
        plt.axvline(0.5, color='red', linestyle='--', label='Decision Threshold')
        plt.title(title)
        plt.xlabel("Predicted Probability")
        plt.ylabel("Frequency")
        plt.legend()
        plt.show()


# Example usage:

# Assuming cash_df is the DataFrame with the necessary data
#cash_df = pd.read_csv("./data/test2_regression.csv")

# Create ModelEvaluation instance
#model_eval = ModelEvaluation(cash_df)

# Train models and evaluate them
#model_eval.train_and_evaluate_models()

# Generate evaluation plots
#model_eval.plot_evaluations()
