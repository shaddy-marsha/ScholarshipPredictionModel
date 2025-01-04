import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
import os

# Load the model
model_path = os.path.join(os.path.dirname(__file__), '../Models/scholarship_award_decision.h5')
model = load_model(model_path)

# Streamlit UI to input data for prediction
st.title("Scholarship Predictor")

# Create input fields (adjust according to your model's input features)
education_qualification = st.selectbox("Education Qualification", ["Undergraduate", "Postgraduate", "Doctorate"])
annual_percentage = st.number_input("Annual Percentage", min_value=0.0, max_value=100.0)
income = st.number_input("Income", min_value=0.0)
gender = st.selectbox("Gender", ["Male", "Female"])
community = st.selectbox("Community", ["Minority", "OBC", "SC/ST", "General"])
disability = st.selectbox("Disability", ["No", "Yes"])
sports = st.selectbox("Sports", ["No", "Yes"])
india = st.selectbox("India", ["In", "Out"])

# Apply preprocessing (Ordinal encoding for Education Qualification and one-hot encoding for others)
# Ordinal encode education qualification
education_categories = ["Undergraduate", "Postgraduate", "Doctorate"]
education_encoded = education_categories.index(education_qualification)

# One-hot encoding for gender
gender_male = 1 if gender == "Male" else 0

# One-hot encoding for community (excluding "General" as the reference category)
community_minority = 1 if community == "Minority" else 0
community_obc = 1 if community == "OBC" else 0
community_sc_st = 1 if community == "SC/ST" else 0

# One-hot encoding for disability
disability_yes = 1 if disability == "Yes" else 0

# One-hot encoding for sports
sports_yes = 1 if sports == "Yes" else 0

# One-hot encoding for India
india_in = 1 if india == "In" else 0

# Construct the input array for prediction (ensure it has 10 features)
input_data = np.array([[
    education_encoded, annual_percentage, income,
    gender_male, community_minority, community_obc, community_sc_st,
    disability_yes, sports_yes, india_in
]])

# Make prediction when the user submits
if st.button("Predict"):
    prediction = model.predict(input_data)
    if prediction[0] > 0.5:
        st.write("The student is likely to receive a scholarship.")
    else:
        st.write("The student is unlikely to receive a scholarship.")
