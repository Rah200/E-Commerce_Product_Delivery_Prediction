# Import Libraries
import streamlit as st
from helper import predict

# Set the title
st.set_page_config(page_title="E-Commerce Delivery Prediction", layout="centered")
st.title("📦 Product Delivery Predictor")
st.write("Check whether a product will be delivered on time or delayed.")

# Create three rows of three columns each
row1 = st.columns(3)
row2 = st.columns(3)
row3 = st.columns(3)

# Input Fields
with row1[0]:
    weight = st.number_input("Weight (KG)", min_value=0.1, value=1.0, step=0.1, format="%.1f")
with row1[1]:
    cost = st.number_input("Cost of Product", step=10, min_value=1, value=250)
with row1[2]:
    discount = st.number_input("Discount Offered (%)", min_value=0, value=1)

with row2[0]:
    warehouse = st.selectbox("Warehouse Block", ["A","B","C","D","F"])
with row2[1]:
    shipment = st.selectbox("Mode of Shipment", ["Flight","Road","Ship"])
with row2[2]:
    importance = st.selectbox("Product Importance", ["low","medium","high"])

with row3[0]:
    customer_rating = st.number_input("Customer Rating", min_value=1, max_value=5, value=1)
with row3[1]:
    prior_purchase = st.number_input("Prior Purchases", min_value=0, value=1)
with row3[2]:
    customer_care_calls = st.number_input("Customer Care Calls", min_value=0, max_value=10, value=1)

# Convert Inputs
input_dict = {
    "Customer_care_calls": customer_care_calls,
    "Customer_rating": customer_rating,
    "Cost_of_the_Product": cost,
    "Prior_purchases": prior_purchase,
    "Discount_offered": discount,
    "Weight_in_gms": weight * 1000,

    "warehouse": warehouse,
    "shipment": shipment,
    "importance": importance
}

# Button to make prediction
if st.button("Check"):

    prediction, probability = predict(input_dict)

    if prediction == 1:
        st.error("❌ Product Delivery will be Delayed")
    else:
        st.success("✅ Product will be Delivered On Time")

    st.write("### Prediction Confidence")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("On-Time Delivery", f"{probability[0]*100:.2f}%")

    with col2:
        st.metric("Delayed Delivery", f"{probability[1]*100:.2f}%")