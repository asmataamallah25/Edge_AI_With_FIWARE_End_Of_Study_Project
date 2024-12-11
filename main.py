import os
from datetime import timedelta
import pandas as pd

from simulator import simulate_battery_data
from config import OUTPUT_DIR, SCENARIOS, INITIAL_SOH


def main():
    end_date = pd.Timestamp.now().date()
    start_date = end_date - timedelta(days=4*365)

    for usage_frequency, charging_behavior in SCENARIOS:
        scenario_name = f"{usage_frequency}_{charging_behavior}"
        print(f"Starting scenario: {scenario_name}")
        try:
            df = simulate_battery_data(start_date, end_date, INITIAL_SOH, usage_frequency, charging_behavior)
            print(f"Data generated for scenario: {scenario_name}")
            
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            filename = f'{usage_frequency}_usage_{charging_behavior}_charging_battery_data.csv'
            filepath = os.path.join(OUTPUT_DIR, filename)
            df.to_csv(filepath, index=False)
            print(f"Data saved to {filepath}")
        except Exception as e:
            print(f"Error in scenario {scenario_name}: {str(e)}")

if __name__ == "__main__":
    main()
