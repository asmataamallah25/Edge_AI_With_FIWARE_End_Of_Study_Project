import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

# Set the directory path
data_dir = '../battery_simulation/synthetic_datasets'

# Initialize an empty list to store dataframes
dataframes = []

# Iterate through CSV files in the directory
for csv_file in os.listdir(data_dir):
    if csv_file.endswith('.csv'):
        # Extract scenario name from the filename
        scenario = csv_file.replace('_battery_data.csv', '')
        
        # Construct full file path
        full_path = os.path.join(data_dir, csv_file)
        
        # Read the CSV file
        df = pd.read_csv(full_path, parse_dates=['Date'])
        
        # Add a scenario column
        df['scenario'] = scenario
        
        # Append the dataframe to the list
        dataframes.append(df)

# Concatenate all dataframes
combined_dataset = pd.concat(dataframes, ignore_index=True)

# Convert datetime to numerical features
combined_dataset['Date'] = combined_dataset['Date'].astype(int) / 10**9

# Label encode the scenario column
label_encoder = LabelEncoder()
combined_dataset['scenario'] = label_encoder.fit_transform(combined_dataset['scenario'])

# Separate features and target
features = combined_dataset.drop('SOH', axis=1)
target = combined_dataset['SOH']

# Scale numerical features
scaler = MinMaxScaler()
features_scaled = scaler.fit_transform(features)

# Convert to DataFrame
features_scaled_df = pd.DataFrame(features_scaled, columns=features.columns)

# Concatenate the scaled features with the target
final_dataset = pd.concat([features_scaled_df, target], axis=1)

# Save the final preprocessed dataset
final_output_file = 'preprocessed_battery_data.csv'
final_dataset.to_csv(final_output_file, index=False)

print(f"Preprocessed data saved to {final_output_file}")
print(final_dataset.columns)
print(final_dataset.head())