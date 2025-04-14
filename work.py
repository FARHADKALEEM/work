
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import streamlit as st
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc

# Title for the app
st.title("Fraud Detection Model")

# File uploaders to upload training and testing data
train_file = "C:/Users/Hussian computer/Downloads/fraudTrain.csv"
test_file = "C:/Users/Hussian computer/Downloads/fraudTest.csv"

# Check if both files are uploaded
if train_file is not None and test_file is not None:
    # Load the datasets directly from the uploaded files
    train = pd.read_csv(train_file)
    test = pd.read_csv(test_file)
    
    # Combine both datasets
    df = pd.concat([train, test], ignore_index=True)
    
    
    # Display the combined dataframe
    st.write("Combined Data:")
    st.dataframe(df)
    
    # Check for missing values
    if df.isnull().sum().any():
        st.warning("There are missing values in the dataset.")
        df.fillna(0, inplace=True)  # Optionally fill missing values
    else:
        st.success("No missing values found.")
    
    # Drop 'Unnamed: 0' if it exists
    if 'Unnamed: 0' in df.columns:
        df = df.drop('Unnamed: 0', axis=1)
    
    # Initialize LabelEncoder
    le = LabelEncoder()
    
    # Apply LabelEncoder only to categorical columns
    for column in df.columns:
        if df[column].dtype == 'object':
            df[column] = le.fit_transform(df[column])

    # Prepare features (x) and target (y)
    x = df.drop('is_fraud', axis=1)
    y = df['is_fraud']
    df_combined = pd.concat([x, y], axis=1)

# Select a random sample of 1000 rows
    df_sampled = df_combined.sample(n=1000, random_state=42)  # random_state ensures reproducibility

# Separate the features and target back after sampling
    x_sampled = df_sampled.drop('is_fraud', axis=1)  # Features
    y_sampled = df_sampled['is_fraud'] 
    # Split the data into training and test sets
    x_train, x_test, y_train, y_test = train_test_split(x_sampled, y_sampled, test_size=0.2, random_state=42)

    # Train the model
    model = svm.SVC()
    model.fit(x_train, y_train)

    # Make predictions
    y_predict = model.predict(x_test)
    
    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_predict)

    # Display accuracy
    st.write(f"Model Accuracy: {accuracy * 100:.2f}%")
    
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc

# Example true labels and predicted probabilities
y_true = [0, 1, 1, 0, 1]  # True labels
y_pred_prob = [0.1, 0.7, 0.8, 0.4, 0.9]  # Predicted probabilities for the positive class

# Compute ROC curve and ROC AUC
fpr, tpr, thresholds = roc_curve(y_true, y_pred_prob)
roc_auc = auc(fpr, tpr)
st .dataframe(df.head(10))
st.dataframe(df.info())
# Plot ROC curve
plt.figure()
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic')
plt.legend(loc='lower right')

# Display the plot in Streamlit
st.pyplot(plt)
import streamlit as st
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_curve

# Example true labels and predicted probabilities
y_true = [0, 1, 1, 0, 1]  # True labels
y_pred_prob = [0.1, 0.7, 0.8, 0.4, 0.9]  # Predicted probabilities for the positive class

# Compute precision and recall
precision, recall, thresholds = precision_recall_curve(y_true, y_pred_prob)

# Plot Precision-Recall curve
plt.figure()
plt.plot(recall, precision, color='blue', lw=2)
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve')

# Display the plot in Streamlit
st.pyplot(plt)

import pandas as pd
import streamlit as st
from sklearn import svm

# Load your trained model here (assuming you have trained it previously)
# from joblib import load
# model = load('your_model.joblib')

# For demonstration, let's assume you have a trained model variable
model = svm.SVC(probability=True)  # Replace this with your actual trained model

# Title for the app
st.title("Fraud Detection Model")

# User input for all required features
trans_date_trans_time = st.text_input("Transaction Date and Time (YYYY-MM-DD HH:MM:SS):")
cc_num = st.number_input("Credit Card Number:", min_value=0, format="%d")
merchant = st.text_input("Merchant Name:")
category = st.text_input("Category:")
amt = st.number_input("Transaction Amount:", min_value=0.0)
first = st.text_input("First Name:")
last = st.text_input("Last Name:")
gender = st.selectbox("Gender:", ["Male", "Female", "Other"])
street = st.text_input("Street Address:")
city = st.text_input("City:")
state = st.text_input("State:")
zip_code = st.number_input("ZIP Code:", min_value=0)
lat = st.number_input("Latitude:", format="%.6f")
long = st.number_input("Longitude:", format="%.6f")
city_pop = st.number_input("City Population:", min_value=0)
job = st.text_input("Job Title:")
dob = st.text_input("Date of Birth (YYYY-MM-DD):")
trans_num = st.text_input("Transaction Number:")
unix_time = st.number_input("Unix Time:", min_value=0)
merch_long = st.number_input("Merchant Longitude:", format="%.6f")

# Button to submit the input
if st.button('Check Fraud'):
    # Call the fraud detection function
    result = (
        trans_date_trans_time, cc_num, merchant, category, amt,
        first, last, gender, street, city, state, zip_code,
        lat, long, city_pop, job, dob, trans_num, unix_time, merch_long
    )
    st.write('Transaction is:', 'Fraudulent' if result == 1 else 'Legitimate')

# Function to detect fraud
def detect_fraud(trans_date_trans_time, cc_num, merchant, category, amt,
                 first, last, gender, street, city, state, zip_code,
                 lat, long, city_pop, job, dob, trans_num, unix_time, merch_long):
    # Preprocess the input data
    gender_encoded = 1 if gender == 'Male' else (2 if gender == 'Female' else 0)  # Example encoding

    # Create a DataFrame for the input with the same feature names as the training data
    input_data = pd.DataFrame({
        'trans_date_trans_time': [trans_date_trans_time],
        'cc_num': [cc_num],
        'merchant': [merchant],
        'category': [category],
        'amt': [amt],
        'first': [first],
        'last': [last],
        'gender': [gender_encoded],
        'street': [street],
        'city': [city],
        'state': [state],
        'zip': [zip_code],
        'lat': [lat],
        'long': [long],
        'city_pop': [city_pop],
        'job': [job],
        'dob': [dob],
        'trans_num': [trans_num],
        'unix_time': [unix_time],
        'merch_long': [merch_long]
    })

    # Make predictions
    prediction = model.predict(input_data)
    return prediction[0]  # Return the prediction (0 for legitimate, 1 for fraudulent)
