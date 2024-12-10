import requests
import time
import json
import os


# Environments Variables
ENTITY_ID = os.getenv("ENTITY_ID")
BROKER_URL = os.getenv("BROKER_URL")
DEFAULT_DEGRADATION_RATE = float(os.getenv("DEFAULT_DEGRADATION_RATE", 0.5))
RUN_DURATION = int(os.getenv("RUN_DURATION", 120))

def get_entity_data(entity_id):
    """Fetch the entity data from the Context Broker."""
    response = requests.get(f"{BROKER_URL}{entity_id}", headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching entity data: {response.status_code} {response.text}")
        return None

def calculate_degradation_factor(charging_behavior, discharging_behavior, temperature, cycle_count):
    """Calculate the degradation factor based on charging, discharging, temperature, and cycle count."""
    
    # Constants
    OPTIMAL_BEHAVIOR = 10
    RATED_CYCLES = 120  # One cycle per second of simulation
    
    # Behavior impact (non-linear, with charging weighted more)
    charging_impact = ((charging_behavior - OPTIMAL_BEHAVIOR) ** 2) * 0.001
    discharging_impact = ((discharging_behavior - OPTIMAL_BEHAVIOR) ** 2) * 0.0005
    behavior_factor = charging_impact + discharging_impact

    # Temperature impact
    if temperature < 0:
        temperature_factor = abs(temperature) * 0.01
    elif temperature > 40:
        temperature_factor = (temperature - 40) * 0.01
    else:
        temperature_factor = 0

    # Cycle count impact
    cycle_factor = (cycle_count / RATED_CYCLES) * 0.1

    # Total degradation factor calculation
    total_degradation_factor = DEFAULT_DEGRADATION_RATE + behavior_factor + temperature_factor + cycle_factor
    
    return max(0, min(total_degradation_factor, 1.0))

def update_entity(entity_id, soh_percentage, soh_state, time_to_critical):
    data = {
        "sohPercentage": {
            "type": "Property",
            "value": soh_percentage
        },
        "sohCurrentState": {
            "type": "Property",
            "value": soh_state
        },
        "sohTimeToCritical": {
            "type": "Property",
            "value": time_to_critical
        }
    }
    
    response = requests.post(f"{BROKER_URL}{entity_id}/attrs?options=append", json=data, headers={"Content-Type": "application/json"})
    if response.status_code in [200, 204]:
        print("Entity updated successfully.")
    else:
        print(f"Error updating entity: {response.status_code} {response.text}")

def main():
    start_time = time.time()
    soh_percentage = 100.0  # Initial SoH at 100%
    cycle_count = 0         # Initialize cycle counter

    while time.time() - start_time < RUN_DURATION:
        cycle_count += 1
        
        # Step 1: Query the Context Broker
        entity_data = get_entity_data(ENTITY_ID)
        if entity_data is None:
            break

        # Step 2: Extract relevant attributes
        charging_behavior = entity_data.get("chargingBehaviour", {}).get("value", 10)
        discharging_behavior = entity_data.get("dischargingBehaviour", {}).get("value", 10)
        temperature = entity_data.get("temperature", {}).get("value", 25)

        # Step 3: Calculate degradation factor
        degradation_factor = calculate_degradation_factor(
            charging_behavior, 
            discharging_behavior, 
            temperature,
            cycle_count
        )

        # Step 4: Update SoH for the next iteration
        soh_percentage -= degradation_factor
        soh_percentage = max(soh_percentage, 0)  # Prevent negative SoH

        # Step 5: Determine SoH state
        if soh_percentage >= 80:
            soh_state = "Very Good"
        elif soh_percentage >= 40:
            soh_state = "Good"
        elif soh_percentage >= 15:
            soh_state = "Weak"
        else:
            soh_state = "Critical"

        # Step 6: Calculate time to critical
        time_to_critical = soh_percentage / degradation_factor if degradation_factor > 0 else float('inf')

        # Step 7: Update the entity with new SoH values
        update_entity(ENTITY_ID, soh_percentage, soh_state, time_to_critical)

        # Wait for a second before the next iteration
        time.sleep(1)

if __name__ == "__main__":
    main()
