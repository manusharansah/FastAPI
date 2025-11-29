import streamlit as st
import requests

API_URL = 'http://127.0.0.1:8000/predict'

st.title('Insurance Premium Category Prediction Model')
st.markdown('Enter your details below')

age = st.number_input('Age')
weight = st.number_input('Weight in kilograms(kg)')
height = st.number_input('Height in meters(m)')
income_lpa = st.number_input('Annual income in Lakhs')
smoker = st.selectbox('Are you a smoker?',options=['Yes','No'])
city = st.text_input('Residing City')
occupation = st.selectbox('Work for living',options=['retired', 'freelancer', 'student', 'government_job','business_owner', 'unemployed', 'private_job'])

if st.button('Predict Premium Type'):
    data = {
        'age':int(age),
        'weight':weight,
        'height':height,
        'income_lpa':income_lpa,
        'smoker': True if smoker == 'Yes' else False,
        'city': city,
        'occupation': occupation
    }

    try:
        response = requests.post(API_URL,json=data)
        result = response.json()
        
        # st.write(result)
        # st.write(response)


        if response.status_code == 200:
            prediction = result["predicted_insurance_premium_category"]
            st.success(f"Predicted Insurance Premium Type: {prediction}")
        else:
            st.error(f'API Error: {response.status_code}')
            st.write(result)
    except requests.exceptions.ConnectionError:
        st.error("Couldn't connect to API")
