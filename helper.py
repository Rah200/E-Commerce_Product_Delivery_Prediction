import pandas as pd
import joblib

model = joblib.load("artifacts/model_rf.joblib")

def preprocess_input(input_dict):
    expected_columns = [
        'Customer_care_calls', 'Customer_rating', 'Cost_of_the_Product', 'Prior_purchases',
        'Discount_offered', 'Weight_in_gms',
        'Warehouse_block_B', 'Warehouse_block_C', 'Warehouse_block_D', 'Warehouse_block_F',
        'Mode_of_Shipment_Road', 'Mode_of_Shipment_Ship',
        'Product_importance_low', 'Product_importance_medium'
    ]

    df = pd.DataFrame(0, columns=expected_columns, index=[0])

    df["Customer_care_calls"] = input_dict["Customer_care_calls"]
    df["Customer_rating"] = input_dict["Customer_rating"]
    df["Cost_of_the_Product"] = input_dict["Cost_of_the_Product"]
    df["Prior_purchases"] = input_dict["Prior_purchases"]
    df["Discount_offered"] = input_dict["Discount_offered"]
    df["Weight_in_gms"] = input_dict["Weight_in_gms"]

    # One-hot encoding
    warehouse = input_dict["warehouse"]
    shipment = input_dict["shipment"]
    importance = input_dict["importance"]

    if warehouse == "B":
        df["Warehouse_block_B"] = 1
    elif warehouse == "C":
        df["Warehouse_block_C"] = 1
    elif warehouse == "D":
        df["Warehouse_block_D"] = 1
    elif warehouse == "F":
        df["Warehouse_block_F"] = 1

    if shipment == "Road":
        df["Mode_of_Shipment_Road"] = 1
    elif shipment == "Ship":
        df["Mode_of_Shipment_Ship"] = 1

    if importance == "low":
        df["Product_importance_low"] = 1
    elif importance == "medium":
        df["Product_importance_medium"] = 1

    return df

def predict(input_dict):
    input_df = preprocess_input(input_dict)
    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0]

    return prediction, probability