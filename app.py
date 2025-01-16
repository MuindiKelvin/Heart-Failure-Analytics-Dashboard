import streamlit as st
import numpy as np
import pickle as pkl
import time

# Load the model
with open("model.pkl", 'rb') as f:
    model = pkl.load(f)

def dicti_vals(dicti):
    x = list(dicti.values())
    x = np.array([x])
    return x

def get_binary_input(prompt):
    user_input = st.radio(prompt, ('Yes', 'No'), horizontal=True)
    return 1 if user_input == 'Yes' else 0

def determine_lifestyle_changes(predict_type, new_person):
    lifestyle_changes = []

    if predict_type > 0:
        if 'Smoking' in new_person and new_person['Smoking'] == 1:
            lifestyle_changes.append('quit smoking 🚭')
        if 'BMI' in new_person and new_person['BMI'] < 18.5:
            lifestyle_changes.append('gain weight 🍔')
        elif 'BMI' in new_person and new_person['BMI'] > 25:
            lifestyle_changes.append('lose weight 🏋️‍♂️')
        if 'Exercise Hours Per Week' in new_person and new_person['Exercise Hours Per Week'] < 1.25:
            lifestyle_changes.append('do more exercise 🏃‍♀️')
        if 'Diet' in new_person and new_person['Diet'] == 0:
            lifestyle_changes.append('eat healthy food 🥗')
        if 'Alcohol Consumption' in new_person and new_person['Alcohol Consumption'] == 1:
            lifestyle_changes.append('try reducing alcohol 🍷')

        result_str = "Heart attack risk: {:.2%}".format(predict_type)
        for i in lifestyle_changes:
            result_str += f"\n• {i}"
        result_str += "\nThese changes can reduce your heart failure risk. ❤️"
        return result_str

    return ""

# Set page config
st.set_page_config(layout="wide", page_title="Heart Failure Classification App")

# Streamlit app
st.title("🏥 Heart Attack Risk Analytics Dashboard 📊🩺")

# Theme selection
theme = st.sidebar.selectbox("Choose theme", ["Light", "Blue"])
if theme == "Blue":
    st.markdown("""
    <style>
    .stApp {
        background-color: #E6F2FF;
        color: #000000;
    }
    </style>
    """, unsafe_allow_html=True)
    result_background = "#E6F2FF"
else:
    result_background = "#FFFFFF"

# Create two main columns
input_col, result_col = st.columns([2, 1])

with input_col:
    st.header("📝 Fill in the Required Information 📋")
    
    # Create four columns for input fields
    col1, col2, col3, col4 = st.columns(4)

    # Distribute the input fields across the four columns
    input_keys = [
        'Age', 'Cholesterol', 'BP_systolic', 'BP_diastolic', 'Heart Rate',
        'Diabetes', 'Family History', 'Smoking', 'Obesity',
        'Alcohol Consumption', 'Exercise Hours Per Week', 'Previous Heart Problems', 'Medication Use',
        'BMI', 'Triglycerides', 'Sleep Hours Per Day',
        'Sex', 'Diet'
    ]

    user_input = {}
    for i, key in enumerate(input_keys):
        with col1 if i % 4 == 0 else col2 if i % 4 == 1 else col3 if i % 4 == 2 else col4:
            if key in ['Diabetes', 'Family History', 'Smoking', 'Obesity', 'Alcohol Consumption', 'Previous Heart Problems', 'Medication Use', 'Diet']:
                user_input[key] = get_binary_input(key)
            elif key == 'Sex':
                sex_input = st.radio("Sex", ('Male', 'Female'), horizontal=True)
                user_input[key] = 1 if sex_input == 'Female' else 0
            else:
                user_input[key] = st.number_input(key, value=0, step=1)

    # Correlation Suggestions
    if 'Smoking' in user_input and 'Diet' in user_input and user_input['Smoking'] == 1 and user_input['Diet'] == 0:
        st.warning("Note: Smoking and an unhealthy diet are correlated with higher heart attack risk.")

    # Prediction button with blue style
    button_html = f"""
        <style>
            .stButton button {{
                background-color: #18dc50;
                color: white;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 4px;
                width: 200px;
            }}
        </style>
    """
    st.markdown(button_html, unsafe_allow_html=True)

    if st.button("Assess Risk🚀", key="predict_button"):
        with result_col:
            st.header("Prediction Results")
            if user_input['Age'] == 0:
                st.warning("Age cannot be 0. Please enter a valid age to proceed with the prediction.")
            else:
                progress_bar = st.progress(0)
                status_text = st.empty()
                for i in range(100):
                    progress_bar.progress(i + 1)
                    status_text.text(f"Processing: {i+1}%")
                    time.sleep(0.10)  # Simulating some processing time

                x = dicti_vals(user_input)
                predict_type = model.predict_proba(x)[:, 1][0]

                status_text.text("Processing: Complete!")
                time.sleep(0.10)  # Pausing briefly before showing results
                status_text.empty()  # Clearing the status text
                progress_bar.empty()  # Removing the progress bar
                
                st.markdown(f"""
                    <div style="background-color:{result_background}; padding: 20px; border-radius: 5px; box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);">
                        <h3>Heart attack risk: {predict_type:.2%}</h3>
                        {determine_lifestyle_changes(predict_type, user_input)}
                    </div>
                """, unsafe_allow_html=True)

                if predict_type > 0.75:
                    st.warning("You should consult a doctor immediately. 🚑")

                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown("""
                    <div style="text-align: center; font-size: 16px; color: gray;">
                        © 2025 Kelvin Muindi: Healthcare Analytics Dashboard. All rights reserved.
                    </div>
                """, unsafe_allow_html=True)
