import asyncio
import streamlit as st

# Fix the "RuntimeError: This event loop is already running" issue
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())


import streamlit as st
import pandas as pd
import numpy as np
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding
from tensorflow.keras.models import load_model  # Example import
# from sklearn.model_selection import train_test_split
import numpy as np
import os

# Define expected columns
expected_columns = [
    'm1_height', 'm1_weight', 'm2_height', 'm2_weight',
    'm3_height', 'm3_weight', 'm4_height', 'm4_weight',
    'm5_height', 'm5_weight', 'm6_height', 'm6_weight',
    'm7_height', 'm7_weight', 'm8_height', 'm8_weight',
    'm9_height', 'm9_weight', 'm10_height', 'm10_weight',
    'm11_height', 'm11_weight', 'm12_height', 'm12_weight'
]

def main():
    st.title("Smart Interventions: ML-Powered Child Nutrition Predictions for CINI")
    df = pd.DataFrame(columns=expected_columns)

    with st.sidebar:
        st.header("Data Input Method")
        input_method = st.radio("Choose input method:", 
                              ("Manual Entry", "File Upload"))

        if input_method == "Manual Entry":
            st.subheader("Manual Data Entry")
            input_data = {}

            # Create number inputs for each month
            for month in range(1, 13):
                st.markdown(f"**Month {month}**")
                col1, col2 = st.columns(2)
                with col1:
                    input_data[f'm{month}_height'] = st.number_input(
                        f"Height (cm)", 
                        key=f"h{month}", 
                        value=0.0
                    )
                with col2:
                    input_data[f'm{month}_weight'] = st.number_input(
                        f"Weight (kg)", 
                        key=f"w{month}", 
                        value=0.0
                    )

            # Create DataFrame from manual input
            df = pd.DataFrame([input_data])

        else:
            st.subheader("File Upload")
            uploaded_file = st.file_uploader(
                "Upload CSV or Excel file",
                type=["csv", "xlsx"],
                accept_multiple_files=False
            )

            if uploaded_file is not None:
                # Read file based on extension
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)

                # Add missing columns with 0.0 values
                for col in expected_columns:
                    if col not in df.columns:
                        df[col] = 0.0

                # Select only expected columns in correct order
                df = df[expected_columns]

    # Display resulting dataframe
    st.subheader("Input Data Preview")
    st.write(df)
    
    # Add your code here to use the dataframe with your model
    if st.button("Predict"):
        model_path = os.path.join("..", "model", "my_model.h5")
        model = keras.models.load_model(model_path)

        # Get raw probability predictions
        prediction_probs = model.predict(df)  

        # Define class labels
        label_mapping = {
            0: "stunting",
            1: "under-nourishment",
            2: "healthy"
        }

        # Convert probabilities into a readable format
        results = []
        for probs in prediction_probs:  
            formatted_probs = {label_mapping[i]: f"{probs[i] * 100:.2f}%" for i in range(len(probs))}
            results.append(formatted_probs)

        # Display results
        for idx, res in enumerate(results):
            st.subheader(f"Prediction for Sample {idx+1}")
            for label, prob in res.items():
                st.write(f"{label}: {prob}")



if __name__ == "__main__":
    main()