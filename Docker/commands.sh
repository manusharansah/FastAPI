#!/bin/sh

uvicorn insurance_premium_prediction_project.insurance_api:app --reload &
streamlit run insurance_premium_prediction_project/frontend/insurance_frontend.py
