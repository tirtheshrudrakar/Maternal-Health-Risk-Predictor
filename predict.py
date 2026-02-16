import pickle
import numpy as np

class MaternalHealthPredictor:
    """Maternal Health Risk Predictor"""

    def __init__(self, model_path='models/best_model.pkl', 
                 scaler_path='models/scaler.pkl',
                 mapping_path='models/risk_mapping.pkl'):
        """Load saved models"""
        with open(model_path, 'rb') as f:
            self.model = pickle.load(f)
        with open(scaler_path, 'rb') as f:
            self.scaler = pickle.load(f)
        with open(mapping_path, 'rb') as f:
            self.risk_mapping = pickle.load(f)

        self.reverse_mapping = {v: k for k, v in self.risk_mapping.items()}    
        self.class_names = [self.reverse_mapping[i] for i in sorted(self.reverse_mapping)]

    def _confidence_range(self, prob):
        """Convert probability to confidence range"""
        prob = prob * 100

        if prob >= 95:
            return "95-98%"
        elif prob >= 80:
            return "80-90%"
        elif prob >= 70:
            return "70-80%"
        elif prob >= 55:
            return "55-70%"
        else:
            return "50-55%"

    def predict(self, age, systolic_bp, diastolic_bp, bs, body_temp, heart_rate):
        """Predict maternal health risk"""

        # Create feature array
        features = np.array([[age, systolic_bp, diastolic_bp, bs, body_temp, heart_rate]])

        # Scale
        features_scaled = self.scaler.transform(features)

        # Predict (ML output)
        prediction = self.model.predict(features_scaled)[0]
        probabilities = self.model.predict_proba(features_scaled)[0]

        # Decode ML prediction
        risk_level = self.reverse_mapping[prediction]

        # 🚨 ABSOLUTE HIGH-RISK OVERRIDES (DOCTOR RULES)
        # Once HIGH RISK → ALWAYS HIGH RISK
        if (
            systolic_bp >= 140 or
            diastolic_bp >= 90 or
            bs >= 11.1 or
            body_temp >= 100.4 or
            heart_rate >= 110 or
            age < 18 or age > 35
        ):
            risk_level = "high risk"

        # ⚠️ BORDERLINE CONDITIONS → MID RISK (only if not already high)
        elif (
            systolic_bp >= 120 or
            diastolic_bp >= 80 or
            bs >= 7.0 or
            body_temp >= 99.0 or
            heart_rate >= 90
        ):
            if risk_level == "low risk":
                risk_level = "mid risk"

        # Confidence range (based on ML probability)
        confidence = self._confidence_range(probabilities[prediction])

        return {
            'risk_level': risk_level,
            'confidence': confidence,
            'probabilities': {
                name: f"{prob*100:.2f}%"
                for name, prob in zip(self.class_names, probabilities)
            }
        }


# Example usage
if __name__ == "__main__":
    predictor = MaternalHealthPredictor()

    print("="*60)
    print("MATERNAL HEALTH RISK PREDICTOR")
    print("="*60)

    print("\nEnter patient details:")
    age = float(input("Age (years): "))
    systolic = float(input("Systolic BP (mmHg): "))
    diastolic = float(input("Diastolic BP (mmHg): "))
    bs = float(input("Blood Sugar (mmol/L): "))
    temp = float(input("Body Temperature (°F): "))
    hr = float(input("Heart Rate (bpm): "))

    result = predictor.predict(age, systolic, diastolic, bs, temp, hr)

    print("\n" + "="*60)
    print("PREDICTION RESULTS")
    print("="*60)
    print(f"Risk Level: {result['risk_level'].upper()}")
    print(f"Confidence: {result['confidence']}")
    print("\nProbabilities:")
    for risk, prob in result['probabilities'].items():
        print(f"  {risk}: {prob}")
    print("="*60)
