from fastapi import FastAPI, HTTPException
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from datetime import datetime

app = FastAPI()

# Load ARIMA model and scalers
try:
    model = joblib.load('arima_model.pkl')
    feature_scaler = MinMaxScaler(feature_range=(-1, 1))
    target_scaler = MinMaxScaler(feature_range=(-1, 1))
except:
    model = None

# Define scenarios and patterns
SCENARIOS = [
    ('low', 'optimal'),
    ('normal', 'optimal'),
    ('normal', 'full'),
    ('normal', 'frequent_top_ups'),
    ('normal', 'deep_discharge'),
    ('high', 'optimal')
]

# Initialize label encoder for scenarios
label_encoder = LabelEncoder()
scenario_labels = [f"{usage}_{freq}" for usage, freq in SCENARIOS]
label_encoder.fit(scenario_labels)

def determine_scenario(charging_rate, discharging_rate, charging_cycles):
    """Determine usage frequency and charging behavior based on input parameters"""
    if charging_cycles < 50:
        usage = 'low'
    elif charging_cycles > 150:
        usage = 'high'
    else:
        usage = 'normal'
    
    if 0.2 <= charging_rate <= 0.8 and 0.2 <= discharging_rate <= 0.8:
        behavior = 'optimal'
    elif charging_rate > 0.8 or discharging_rate > 0.8:
        behavior = 'full'
    elif charging_rate < 0.2:
        behavior = 'deep_discharge'
    elif 0.6 <= charging_rate <= 0.8:
        behavior = 'frequent_top_ups'
    else:
        behavior = 'optimal'
    
    return f"{usage}_{behavior}"

def manual_soh_calculation(charging_cycles, temperature, charging_rate, discharging_rate):
    """Calculate SOH using enhanced degradation factors"""
    # Constants
    OPTIMAL_BEHAVIOR = 10
    INITIAL_SOH = 100.0
    DEFAULT_DEGRADATION_RATE = 1.0
    MIN_SOH = 70.0
    
    # Temperature impact (capped)
    if temperature < 0:
        temperature_factor = min(abs(temperature) * 0.15, 2.0)
    elif temperature > 40:
        temperature_factor = min((temperature - 40) * 0.15, 2.0)
    else:
        temperature_factor = 0
    
    # Behavior impact
    if discharging_rate < 0.2:
        behavior_factor = 0.5
    else:
        charging_behavior = charging_rate * 20
        discharging_behavior = discharging_rate * 20
        charging_impact = ((charging_behavior - OPTIMAL_BEHAVIOR) ** 2) * 0.002
        discharging_impact = ((discharging_behavior - OPTIMAL_BEHAVIOR) ** 2) * 0.001
        behavior_factor = charging_impact + discharging_impact
    
    # Cycle impact (capped) - adjusted for daily data
    cycle_factor = min((charging_cycles / 365) * 0.4, 2.0)  # Using 365 days as reference
    
    # Calculate total degradation with scaling factor
    scaling_factor = min(charging_cycles / 3650, 4.0)  # Cap at 10 years worth of cycles
    total_degradation = (DEFAULT_DEGRADATION_RATE + behavior_factor + temperature_factor + cycle_factor) * scaling_factor
    
    soh = INITIAL_SOH - total_degradation
    return max(MIN_SOH, min(soh, INITIAL_SOH)), "Critical" if soh <= 75 else "Fair"





@app.post("/predict")
async def predict(data: dict):
    try:
        input_data = data.get('data', {})
        charging_cycles = input_data.get('charging_cycles', 100)
        temperature = input_data.get('temperature', 25)
        charging_rate = input_data.get('charging_rate', 0.8)
        discharging_rate = input_data.get('discharging_rate', 0.6)
        
        # Determine scenario and get current timestamp
        scenario = determine_scenario(charging_rate, discharging_rate, charging_cycles)
        current_date = pd.Timestamp.now()
        
        # Try ARIMA prediction first
        if model:
            try:
                features = pd.DataFrame([{
                    'Date': current_date.timestamp(),
                    'scenario': label_encoder.transform([scenario])[0],
                    'charging_cycles': charging_cycles,
                    'temperature': temperature,
                    'charging_rate': charging_rate,
                    'discharging_rate': discharging_rate
                }])
                
                X = feature_scaler.fit_transform(features)
                results = model.fit()
                prediction = results.forecast(steps=1, exog=X)
                soh_prediction = target_scaler.inverse_transform(prediction.reshape(-1, 1))
                
                return {
                    "soh_prediction": float(soh_prediction[0][0]),
                    "date": current_date.isoformat(),
                    "scenario": scenario,
                    "method": "arima"
                }
            except Exception as e:
                pass
        
        # Fallback to manual calculation
        soh, soh_state = manual_soh_calculation(
            charging_cycles,
            temperature,
            charging_rate,
            discharging_rate
        )
        
        return {
            "soh_prediction": float(soh),
            "date": current_date.isoformat(),
            "scenario": scenario,
            "soh_state": soh_state,
            "method": "manual"
        }
        
    except Exception as e:
        current_date = pd.Timestamp.now()
        return {
            "soh_prediction": 95.0,
            "date": current_date.isoformat(),
            "scenario": "normal_optimal",
            "soh_state": "Very Good",
            "method": "default"
        }
