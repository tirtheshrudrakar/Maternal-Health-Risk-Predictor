## Maternal Health Risk Predictor is a simple, practical machine learning project that predicts whether a pregnant patient is at low, medium, or high health risk using routine clinical data.

# What the Project Does (In Simple Terms)

It takes common medical inputs (like age, blood pressure, glucose levels, etc.), cleans and prepares the data, trains a supervised ML model, evaluates its performance, and then allows predictions for new patients through a small prediction script.

Reads maternal health data from CSV files

Cleans and prepares the data

Fixes missing or inconsistent values

Scales numeric features if needed

Encodes categorical values

Trains machine learning models

Starts with interpretable models (Logistic Regression)

Improves accuracy using Random Forest / XGBoost

Evaluates model performance

Accuracy, precision, recall, F1-score, ROC/AUC

Predicts risk

For a single patient or a batch of patients

# What’s Inside the Repository

Data folder – raw and processed datasets

Notebooks – exploration and experiments

Models folder – trained ML models

Scripts – preprocessing, training, evaluation, and prediction

Config file – controls parameters for reproducibility

Everything is structured so that someone else can run it without confusion.

# Tech stack


Machine learning and data science : NumPy , Pandas , Scikit-learn

Data preprocessing (scaling, encoding)

Model training (Logistic Regression, Random Forest)

Model evaluation (accuracy, F1-score, ROC-AUC)

Modeling Techniques : Logistic Regression , Random Forest Classifier 

Pickle : Saving and loading trained models, scalers, and encoders

Web Application and UI : Streamlit –

Visualization : Plotly , Matplotlib 

## Author

**Tirthesh Rudrakar**  
B.Tech – Artificial Intelligence & Data Science  

GitHub: https://github.com/tirtheshrudrakar
LinkedIn: https://www.linkedin.com/in/tirthesh-rudrakar/ 
