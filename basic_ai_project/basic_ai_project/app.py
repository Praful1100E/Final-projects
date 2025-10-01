from flask import Flask, request, render_template, jsonify
import joblib
import numpy as np
import os
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

app = Flask(__name__)

# Load the trained model and target names
try:
    model = joblib.load('model.pkl')
    target_names = joblib.load('target_names.pkl')
    print("✅ Model loaded successfully!")
except FileNotFoundError:
    print("❌ Model files not found. Please run main.py first to train the model.")
    model = None
    target_names = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return render_template('result.html', 
                             prediction="Error: Model not loaded. Please train the model first.",
                             error=True)
    
    try:
        # Get form data
        sepal_length = float(request.form['sepal_length'])
        sepal_width = float(request.form['sepal_width'])
        petal_length = float(request.form['petal_length'])
        petal_width = float(request.form['petal_width'])

        # Validate input ranges (basic validation)
        if not (4.0 <= sepal_length <= 8.0):
            raise ValueError("Sepal length should be between 4.0 and 8.0 cm")
        if not (2.0 <= sepal_width <= 4.5):
            raise ValueError("Sepal width should be between 2.0 and 4.5 cm")
        if not (1.0 <= petal_length <= 7.0):
            raise ValueError("Petal length should be between 1.0 and 7.0 cm")
        if not (0.1 <= petal_width <= 2.5):
            raise ValueError("Petal width should be between 0.1 and 2.5 cm")

        # Prepare input for prediction
        features = np.array([[sepal_length, sepal_width, petal_length, petal_width]])

        # Make prediction
        prediction = model.predict(features)
        predicted_class = target_names[prediction[0]]

        # Get prediction probabilities if available
        try:
            probabilities = model.predict_proba(features)[0]
            confidence = max(probabilities) * 100
        except:
            confidence = None

        return render_template('result.html', 
                             prediction=predicted_class,
                             confidence=confidence,
                             input_values={
                                 'sepal_length': sepal_length,
                                 'sepal_width': sepal_width,
                                 'petal_length': petal_length,
                                 'petal_width': petal_width
                             })

    except ValueError as e:
        return render_template('result.html', 
                             prediction=f"Input Error: {str(e)}", 
                             error=True)
    except Exception as e:
        return render_template('result.html', 
                             prediction=f"Prediction Error: {str(e)}", 
                             error=True)

@app.route('/api/test', methods=['GET'])
def api_test():
    """API endpoint to test the model with sample data"""
    if model is None:
        return jsonify({"error": "Model not loaded"}), 500
    
    # Test samples
    test_samples = {
        'setosa': [5.1, 3.5, 1.4, 0.2],
        'versicolor': [7.0, 3.2, 4.7, 1.4],
        'virginica': [6.3, 3.3, 6.0, 2.5]
    }
    
    results = {}
    for species, features in test_samples.items():
        prediction = model.predict([features])
        predicted_class = target_names[prediction[0]]
        results[species] = {
            'input': features,
            'predicted': predicted_class,
            'correct': predicted_class.lower() == species
        }
    
    return jsonify(results)

@app.route('/api/accuracy', methods=['GET'])
def api_accuracy():
    """API endpoint to get model accuracy"""
    if model is None:
        return jsonify({"error": "Model not loaded"}), 500
    
    try:
        # Load iris dataset for testing
        iris = load_iris()
        X = iris.data
        y = iris.target
        
        # Split data (same as training)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        
        # Get predictions
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        return jsonify({
            "accuracy": round(accuracy * 100, 2),
            "test_samples": int(len(X_test)),
            "correct_predictions": int(sum(y_pred == y_test)),
            "model_type": "Decision Tree Classifier"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    status = {
        "status": "healthy",
        "model_loaded": model is not None,
        "target_names_loaded": target_names is not None
    }
    return jsonify(status)

if __name__ == '__main__':
    print("🌸 Starting Iris Flower Classifier Web App...")
    print("📊 Features: Modern UI, Interactive Testing, Model Validation")
    print("🚀 Access the app at: http://localhost:5000")
    print("🔗 API endpoints available:")
    print("   - /api/test (GET) - Test with sample data")
    print("   - /api/accuracy (GET) - Get model accuracy")
    print("   - /health (GET) - Health check")
    app.run(debug=True, host='0.0.0.0', port=5000)
