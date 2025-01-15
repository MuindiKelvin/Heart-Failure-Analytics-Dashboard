import streamlit as st
import numpy as np
import pickle as pkl

# Load the model
with open("model.pkl", 'rb') as f:
    model = pkl.load(f)

def dicti_vals(dicti):
    x = list(dicti.values())
    x = np.array([x])
    return x

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
            result_str += f"\nPlease {i},"
        result_str += "\nThis can reduce your heart rate risk. ❤️"
        st.success(result_str)
        
    if predict_type > 0.75:
        st.warning("You should consult a doctor immediately. 🚑")
        st.write("Heart attack risk: {:.2%}".format(predict_type))

# Streamlit app
st.title("Heart Failure Classification App 🩺")

# User Input section
st.header("User Input 🛠️")

# Centering user inputs in columns
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
for i in range(4):
    with col1 if i == 0 else col2 if i == 1 else col3 if i == 2 else col4:
        for j in range(i, len(input_keys), 4):
            user_input[input_keys[j]] = st.number_input(input_keys[j], value=0)

# Prediction button with green style
button_html = f"""
    <style>
        .stButton button {{
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 4px;
        }}
    </style>
"""
st.markdown(button_html, unsafe_allow_html=True)
if st.button("Predict Heart Failure 🚀", key="predict_button"):
    x = dicti_vals(user_input)
    predict_type = model.predict_proba(x)[:, 1]
    determine_lifestyle_changes(predict_type[0], user_input)
