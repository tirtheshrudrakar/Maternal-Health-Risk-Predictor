import streamlit as st
from predict import MaternalHealthPredictor
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


st.markdown("<div class='ti'>CLINE<div class='t2'>X</div>I</div>", unsafe_allow_html=True)


st.set_page_config(
    
    page_title="Clinexi",

    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
    <style>
           
    @import url('https://fonts.googleapis.com/css2?family=Audiowide&display=swap');
   [data-testid="stApp"] {
    background: linear-gradient(to bottom, #414ba9, #af66ff);
    }
    .main {
        padding: 2rem;
    }
    .audiowide-regular {
      font-family: "Audiowide", sans-serif;
      font-weight: 400;
      font-style: normal;
    }
            .t2{
            color: #C399FF;
            display: inline;
    }

    .stButton>button {
        width: 100%;
        background-color: #C399FF;
        color: black;
        font-size: 18px;
        font-weight: bold;
        padding: 0.75rem;
        border-radius: 10px;
            
    }
    .ti{
        color: white;
        text-align: left;
        font-family: "Audiowide", sans-serif;
        font-size: 3rem;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #A569BD;
        color: white;
    }
    .stTextInput>div>div>input {
        font-size: 16px;
        padding: 10px;
    }
    .text{
        color: black;
}
    .t1{
            color: #C399FF;
            display: inline;
    }
    .risk-high {
        background-color: #FF5F40;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #FF4B4B;
    }
    .risk-mid {
        background-color: #FFF4E5;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #FFA500;
    }
    .risk-low {
        background-color: #E5FFE5;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #00C851;
    }
    .st-emotion-cache-1s4g1qq {
        background-color: #C399FF;
            color: black;
    }
    </style>
""", unsafe_allow_html=True)

# Load predictor (cached for performance)
@st.cache_resource
def load_predictor():
    """Initialize the predictor once"""
    return MaternalHealthPredictor()

# Initialize predictor
predictor = load_predictor()

# Title and description
st.markdown("<h1> Maternal <div class='t1'>Health </div> Risk Predictor</h1>", unsafe_allow_html=True)
st.markdown("""
This AI-powered tool predicts maternal health risk levels based on key health parameters.
**Note:** This is a predictive tool and NOT a medical diagnosis. Always consult healthcare professionals.
""")

# Sidebar - Information
with st.sidebar:
    st.header(" About")
    st.info("""
    This tool uses Machine Learning to predict maternal health risk levels:
    - **Low Risk**: Normal parameters
    - **Mid Risk**: Some attention needed
    - **High Risk**: Immediate medical attention required
    """)

    st.markdown("---")
    st.header("Unit Converter")
    
    converter_type = st.selectbox(
        "Convert:",
        ["Blood Sugar (mg/dL to mmol/L)", 
         "Temperature (°C to °F)"]
    )
    
    if converter_type == "Blood Sugar (mg/dL to mmol/L)":
        mgdl = st.number_input("Enter Blood Sugar in mg/dL:", min_value=0.0, step=1.0)
        if mgdl > 0:
            mmol = mgdl / 18
            st.success(f"**{mgdl} mg/dL = {mmol:.1f} mmol/L**")
    
    else:  
        celsius = st.number_input("Enter Temperature in °C:", min_value=0.0, step=0.1)
        if celsius > 0:
            fahrenheit = (celsius * 9/5) + 32
            st.success(f"**{celsius}°C = {fahrenheit:.1f}°F**")    
    
    st.header(" Model Info")
    st.success(f"""
    - **Model Type**: Random Forest
    - **Accuracy**: 95%+
    - **Features**: 6 health parameters
    """)
    
    st.header("⚕️ When to Use")
    st.warning("""
    Use this tool during:
    - Regular prenatal checkups
    - Self-monitoring at home
    - Before doctor appointments
    """)
    
    st.header(" Reference Ranges")
    st.info("""
    **Normal Ranges:**
    - Age: 18-45 years
    - Systolic BP: 90-120 mmHg
    - Diastolic BP: 60-80 mmHg
    - Blood Sugar: 6-7.8 mmol/L
    - Body Temp: 97-99 °F
    - Heart Rate: 60-100 bpm
    """)

# Main content
st.header(" Enter Patient Information")

# Create two columns for inputs
col1, col2 = st.columns(2)

with col1:
    st.subheader("Basic Information")
    
    age = st.text_input(
        "Age (years)",
        placeholder="Enter age (e.g., 25)",
        help="Patient's age in years"
    )
    
    systolic_bp = st.text_input(
        "Systolic Blood Pressure (mmHg)",
        placeholder="Enter systolic BP (e.g., 120)",
        help="Upper number in blood pressure reading"
    )
   
    
    diastolic_bp = st.text_input(
        "Diastolic Blood Pressure (mmHg)",
        placeholder="Enter diastolic BP (e.g., 80)",
        help="Lower number in blood pressure reading"
    )
    
with col2:
    st.subheader("Health Parameters")
    
    blood_sugar = st.text_input(
        "Blood Sugar Level (mmol/L)",
        placeholder="Enter blood sugar (e.g., 7.0)",
        help="Blood glucose level in mmol/L"
    )
   
    body_temp = st.text_input(
        "Body Temperature (°F)",
        placeholder="Enter temperature (e.g., 98.0)",
        help="Body temperature in Fahrenheit"
    )
   
    
    heart_rate = st.text_input(
        "Heart Rate (bpm)",
        placeholder="Enter heart rate (e.g., 75)",
        help="Heartbeats per minute"
    )
  

st.markdown("---")


button_col1, button_col2  = st.columns(2)

with button_col1:
    predict_button = st.button("Predict Risk Level", use_container_width=True)

with button_col2:
    dashboard_button = st.button("View Dashboard", use_container_width=True)



def create_health_dashboard(age_val, systolic_val, diastolic_val, bs_val, temp_val, hr_val):
    """Create comprehensive health parameter dashboard"""
    
    st.markdown("---")
    st.header("Health Parameters Dashboard")
    

    reference_ranges = {
        'Age': {'min': 18, 'max': 45, 'optimal_min': 20, 'optimal_max': 35},
        'Systolic BP': {'min': 90, 'max': 120, 'optimal_min': 100, 'optimal_max': 115},
        'Diastolic BP': {'min': 60, 'max': 80, 'optimal_min': 65, 'optimal_max': 75},
        'Blood Sugar': {'min': 6.0, 'max': 7.8, 'optimal_min': 6.2, 'optimal_max': 7.2},
        'Body Temp': {'min': 97.0, 'max': 99.0, 'optimal_min': 97.5, 'optimal_max': 98.6},
        'Heart Rate': {'min': 60, 'max': 100, 'optimal_min': 70, 'optimal_max': 85}
    }
    
  
    current_values = {
        'Age': age_val,
        'Systolic BP': systolic_val,
        'Diastolic BP': diastolic_val,
        'Blood Sugar': bs_val,
        'Body Temp': temp_val,
        'Heart Rate': hr_val
    }
    
   

    st.subheader("Parameter Comparison with Normal Ranges")
    
    comparison_data = []
    for param, value in current_values.items():
        ranges = reference_ranges[param]
        comparison_data.append({
            'Parameter': param,
            'Your Value': value,
            'Normal Min': ranges['min'],
            'Normal Max': ranges['max'],
            'Optimal Min': ranges['optimal_min'],
            'Optimal Max': ranges['optimal_max']
        })
    
    comp_df = pd.DataFrame(comparison_data)
    
    fig = go.Figure()
    
  
    fig.add_trace(go.Bar(
        name='Normal Min',
        x=comp_df['Parameter'],
        y=comp_df['Normal Min'],
        marker_color='lightblue',
        opacity=0.6
    ))
    
    fig.add_trace(go.Bar(
        name='Normal Max',
        x=comp_df['Parameter'],
        y=comp_df['Normal Max'],
        marker_color='lightgreen',
        opacity=0.6
    ))
    
 
    fig.add_trace(go.Scatter(
        name='Your Values',
        x=comp_df['Parameter'],
        y=comp_df['Your Value'],
        mode='lines+markers',
        marker=dict(size=12, color='red'),
        line=dict(width=3, color='red')
    ))
    
    fig.update_layout(
        title="Your Values vs Normal Ranges",
        xaxis_title="Parameter",
        yaxis_title="Value",
        barmode='group',
        height=500,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
   
    

    st.subheader("Health Status Summary")
    
    status_data = []
    for param, value in current_values.items():
        ranges = reference_ranges[param]
        
        if ranges['optimal_min'] <= value <= ranges['optimal_max']:
            status = " Optimal"
            color = "Good"
        elif ranges['min'] <= value <= ranges['max']:
            status = " Acceptable"
            color = "Moderate"
        else:
            status = " Alert"
            color = "Risk"
        
        status_data.append({
            'Status': color,
            'Parameter': param,
            'Your Value': value,
            'Normal Range': f"{ranges['min']} - {ranges['max']}",
            'Optimal Range': f"{ranges['optimal_min']} - {ranges['optimal_max']}",
            'Assessment': status
        })
    
    status_df = pd.DataFrame(status_data)
    st.dataframe(status_df, use_container_width=True, hide_index=True)

    normalized_values = []
    for param, value in current_values.items():
        ranges = reference_ranges[param]
        
        if ranges['optimal_min'] <= value <= ranges['optimal_max']:
            normalized = 100
        elif ranges['min'] <= value <= ranges['max']:
            normalized = 70
        else:
            normalized = 30
        normalized_values.append(normalized)

    st.subheader(" Health Insights")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Parameters in Optimal Range",
            value=f"{sum(1 for param, value in current_values.items() if reference_ranges[param]['optimal_min'] <= value <= reference_ranges[param]['optimal_max'])}/6",
            delta="Good" if sum(1 for param, value in current_values.items() if reference_ranges[param]['optimal_min'] <= value <= reference_ranges[param]['optimal_max']) >= 4 else "Needs Attention"
        )
    
    with col2:
        st.metric(
            label="Parameters Needing Attention",
            value=f"{sum(1 for param, value in current_values.items() if not (reference_ranges[param]['min'] <= value <= reference_ranges[param]['max']))}/6",
            delta="Monitor" if sum(1 for param, value in current_values.items() if not (reference_ranges[param]['min'] <= value <= reference_ranges[param]['max'])) > 0 else "All Good"
        )
    
    with col3:
        overall_score = sum(normalized_values) / len(normalized_values)
        st.metric(
            label="Overall Health Score",
            value=f"{overall_score:.0f}/100",
            delta="Excellent" if overall_score >= 90 else "Good" if overall_score >= 70 else "Fair"
        )


if predict_button:
    
   
    try:
       
        age_val = float(age)
        systolic_val = float(systolic_bp)
        diastolic_val = float(diastolic_bp)
        bs_val = float(blood_sugar)
        temp_val = float(body_temp)
        hr_val = float(heart_rate)
        
       
        errors = []
        
        if not (10 <= age_val <= 70):
            errors.append("Age must be between 10 and 70 years")
        if not (70 <= systolic_val <= 200):
            errors.append("Systolic BP must be between 70 and 200 mmHg")
        if not (40 <= diastolic_val <= 120):
            errors.append("Diastolic BP must be between 40 and 120 mmHg")
        if not (5.0 <= bs_val <= 20.0):
            errors.append("Blood Sugar must be between 5.0 and 20.0 mmol/L")
        if not (96.0 <= temp_val <= 104.0):
            errors.append("Body Temperature must be between 96.0 and 104.0 °F")
        if not (60 <= hr_val <= 120):
            errors.append("Heart Rate must be between 60 and 120 bpm")
        
        if errors:
            st.error(" **Validation Errors:**")
            for error in errors:
                st.error(f"• {error}")
        else:
           
            result = predictor.predict(
                age=age_val,
                systolic_bp=systolic_val,
                diastolic_bp=diastolic_val,
                bs=bs_val,
                body_temp=temp_val,
                heart_rate=hr_val
            )
            
         
            risk_level = result['risk_level']
            confidence_str = result['confidence']  
            probabilities_dict = result['probabilities']  
            
           
            confidence = confidence_str

      
            prob_values = {k: float(v.rstrip('%')) for k, v in probabilities_dict.items()}
            
        
            st.markdown("---")
            st.header(" Prediction Results")
            
   
            res_col1, res_col2, res_col3 = st.columns(3)
            
            with res_col1:
                st.metric("Risk Level", risk_level.upper())
            
            with res_col2:
                st.metric("Confidence", confidence)

            
            with res_col3:
                if 'high' in risk_level.lower():
                    st.metric("Priority", " URGENT")
                elif 'mid' in risk_level.lower():
                    st.metric("Priority", " MODERATE")
                else:
                    st.metric("Priority", " NORMAL")
            
      
            if 'high' in risk_level.lower():
                st.markdown("""
                <div class='risk-high'>
                    <div class='text'>
                            <h3> HIGH RISK DETECTED</h3>
                    <p><strong>Immediate Action Required:</strong></p>
                    <ul>
                        <li>Contact your healthcare provider immediately</li>
                        <li>Do not delay medical consultation</li>
                        <li>Monitor symptoms closely</li>
                        <li>Emergency helpline: 102 (India)</li>
                    </ul>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            elif 'mid' in risk_level.lower():
                st.markdown("""
                <div class='risk-mid'>
                <div class ='text'>
                    <h3> MEDIUM RISK DETECTED</h3>
                    <p><strong>Recommended Actions:</strong></p>
                    <ul>
                        <li>Schedule a doctor's appointment soon</li>
                        <li>Monitor blood pressure daily</li>
                        <li>Maintain a healthy diet and exercise routine</li>
                        <li>Keep track of any symptoms</li>
                    </ul>
                  </div>          
                </div>
                """, unsafe_allow_html=True)
            
            else:
                st.markdown("""
                <div class='risk-low'>
                <div class = 'text'>            
                    <h3>LOW RISK DETECTED</h3>
                    <p><strong>Continue Good Practices:</strong></p>
                    <ul>
                        <li>Maintain regular prenatal checkups</li>
                        <li>Continue healthy lifestyle habits</li>
                        <li>Stay hydrated and eat nutritious food</li>
                        <li>Light exercise as recommended by doctor</li>
                    </ul>
                </div>            
                </div>
                """, unsafe_allow_html=True)
            
            st.subheader("Risk Probability Distribution")
            
        
            low_risk_prob = 0
            for key, val in prob_values.items():
                if 'low' in key.lower():
                    low_risk_prob = val
                    break
            
        
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=low_risk_prob,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Low Risk Probability (%)", 'font': {'size': 24}},
                gauge={
                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                    'bar': {'color': "darkblue"},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "gray",
                    'steps': [
                        {'range': [0, 33], 'color': '#FFE5E5'},
                        {'range': [33, 66], 'color': '#FFF4E5'},
                        {'range': [66, 100], 'color': '#E5FFE5'}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 50
                    }
                }
            ))
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
      
            st.subheader(" Detailed Probability Breakdown")
            
            
            prob_df = pd.DataFrame({
                'Risk Level': list(prob_values.keys()),
                'Probability (%)': list(prob_values.values())
            }).sort_values('Probability (%)', ascending=False)
            
   
            colors = []
            for risk in prob_df['Risk Level']:
                if 'low' in risk.lower():
                    colors.append('#00C851')
                elif 'mid' in risk.lower():
                    colors.append('#FFA500')
                elif 'high' in risk.lower():
                    colors.append('#FF4B4B')
                else:
                    colors.append('#888888')
            
            fig2 = go.Figure(data=[
                go.Bar(
                    x=prob_df['Risk Level'],
                    y=prob_df['Probability (%)'],
                    text=prob_df['Probability (%)'].round(2),
                    textposition='auto',
                    marker_color=colors
                )
            ])
            
            fig2.update_layout(
                title="Probability for Each Risk Level",
                xaxis_title="Risk Level",
                yaxis_title="Probability (%)",
                height=400
            )
            
            st.plotly_chart(fig2, use_container_width=True)
            
  
            st.subheader("Probability Table")
            prob_table = pd.DataFrame({
                'Risk Level': list(probabilities_dict.keys()),
                'Probability': list(probabilities_dict.values())
            })
            st.table(prob_table)
            
           
            st.subheader(" Input Summary")
            input_summary = pd.DataFrame({
                'Parameter': ['Age', 'Systolic BP', 'Diastolic BP', 'Blood Sugar', 'Body Temperature', 'Heart Rate'],
                'Value': [age_val, systolic_val, diastolic_val, bs_val, temp_val, hr_val],
                'Unit': ['years', 'mmHg', 'mmHg', 'mmol/L', '°F', 'bpm']
            })
            st.table(input_summary)
    
    except ValueError:
        st.error("**Invalid Input!** Please enter valid numbers in all fields.")
        st.info("**Example values:**\n- Age: 25\n- Systolic BP: 120\n- Diastolic BP: 80\n- Blood Sugar: 7.0\n- Body Temperature: 98.0\n- Heart Rate: 75")
    
    except Exception as e:
        st.error(f" **Error occurred:** {str(e)}")
        st.info("Please check your inputs and try again.")


if dashboard_button:
    try:
      
        age_val = float(age)
        systolic_val = float(systolic_bp)
        diastolic_val = float(diastolic_bp)
        bs_val = float(blood_sugar)
        temp_val = float(body_temp)
        hr_val = float(heart_rate)
        
        
        errors = []
        
        if not (10 <= age_val <= 70):
            errors.append("Age must be between 10 and 70 years")
        if not (70 <= systolic_val <= 200):
            errors.append("Systolic BP must be between 70 and 200 mmHg")
        if not (40 <= diastolic_val <= 120):
            errors.append("Diastolic BP must be between 40 and 120 mmHg")
        if not (5.0 <= bs_val <= 20.0):
            errors.append("Blood Sugar must be between 5.0 and 20.0 mmol/L")
        if not (96.0 <= temp_val <= 104.0):
            errors.append("Body Temperature must be between 96.0 and 104.0 °F")
        if not (60 <= hr_val <= 120):
            errors.append("Heart Rate must be between 60 and 120 bpm")
        
        if errors:
            st.error(" **Validation Errors:**")
            for error in errors:
                st.error(f"• {error}")
        else:
           
            create_health_dashboard(age_val, systolic_val, diastolic_val, bs_val, temp_val, hr_val)
    
    except ValueError:
        st.error("**Invalid Input!** Please enter valid numbers in all fields before viewing dashboard.")
        st.info("**Example values:**\n- Age: 25\n- Systolic BP: 120\n- Diastolic BP: 80\n- Blood Sugar: 7.0\n- Body Temperature: 98.0\n- Heart Rate: 75")
    
    except Exception as e:
        st.error(f" **Error occurred:** {str(e)}")
    
FEEDBACK_FORM_URL = "https://forms.gle/UEoUWFHfLZ3HxbX96"

if st.button("Give Feedback"):
    st.markdown(f"[Click here to open feedback form]({FEEDBACK_FORM_URL})")



st.markdown("---")
st.markdown("""
<div style='text-align: center; color: black;'>
    <p> <strong>Disclaimer:</strong> This tool is for educational and informational purposes only. 
    It is NOT a substitute for professional medical advice, diagnosis, or treatment.</p>
    <p>Always seek the advice of your physician or other qualified health provider with any questions 
    regarding your medical condition.</p>
    <p>Made by Clinexi , with love , for Maternal Health Awareness | © 2026 | Author : Tirthesh Rudrakar </p>
</div>
""", unsafe_allow_html=True)
