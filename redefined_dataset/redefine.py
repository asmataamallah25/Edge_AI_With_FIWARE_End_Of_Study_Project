import os 
import pandas as pd 

def generate_recommendation(soh):
    if soh >= 98:
        return "Exceptional condition. Battery is performing at peak efficiency. Maintain current usage and charging patterns."
    elif 95 <= soh < 98:
        return "Excellent condition. Battery health is optimal. Continue current practices and avoid extreme temperatures."
    elif 92 <= soh < 95:
        return "Very good condition. Minor degradation detected. Optimize charging by keeping battery between 20-80% when possible."
    elif 89 <= soh < 92:
        return "Good condition. Slight performance decrease may be noticeable. Avoid frequent full discharges and minimize exposure to high temperatures."
    elif 86 <= soh < 89:
        return "Above average condition. Consider adjusting usage patterns. Limit fast charging and avoid leaving the battery at 100% for extended periods."
    elif 83 <= soh < 86:
        return "Average condition. Performance decline may be evident. Implement battery-saving measures like reducing screen brightness and background app usage."
    elif 80 <= soh < 83:
        return "Fair condition. Battery life noticeably shorter. Optimize device settings, avoid extreme temperatures, and consider reducing heavy usage."
    elif 77 <= soh < 80:
        return "Below average condition. Significant capacity loss. Use power-saving mode frequently and avoid demanding applications when possible."
    elif 74 <= soh < 77:
        return "Poor condition. Battery degradation is advanced. Plan for replacement within the next few months and avoid complete discharges."
    elif 71 <= soh < 74:
        return "Very poor condition. Battery performance is severely compromised. Prepare for imminent replacement and keep charger readily available."
    elif 70 <= soh < 71:
        return "Critical condition. Battery has reached end-of-life. Replace as soon as possible to avoid unexpected shutdowns and potential data loss."
    else:
        return "Battery failure imminent. Replace immediately to prevent device malfunction and potential safety issues."

def process_dataset(data_dir, reformulated_dataset_dir):
    all_data = []
    # Get a list of all csv files
    csv_files = os.listdir(data_dir)
    print(f"The csv files: {csv_files}")
    for csv_file in csv_files:
        if csv_file.endswith('.csv'):
            print(csv_file)
            # Join the directory path with the filename
            full_path = os.path.join(data_dir, csv_file)
            df = pd.read_csv(full_path)
            # Extract SOH values and generate recommendations
            soh_values = df['SOH']
            recommendation = [generate_recommendation(soh) for soh in soh_values]
            
            # Combine SOH and recommendations
            all_data.extend(zip(soh_values, recommendation))

    # Create a new DataFrame with the processed data
    new_df = pd.DataFrame(all_data, columns=['SOH', 'recommendation'])
    
    # Create the output directory if it doesn't exist
    if not os.path.exists(reformulated_dataset_dir):
        os.makedirs(reformulated_dataset_dir)
    
    output_file = os.path.join(reformulated_dataset_dir, 'soh_recommendation_dataset.csv')
    # Shuffle all the raws of the dataframe
    shuffled_df = new_df.sample(frac=1).reset_index(drop=True)
    
    # Save the new DataFrame to a CSV file
    shuffled_df.to_csv(output_file, index=True)
    print(f"New dataset saved to {output_file}")

# Execute the functions
data_dir = '../battery_simulation/synthetic_datasets'
reformulated_dataset_dir = 'reformulated_dataset'

process_dataset(data_dir, reformulated_dataset_dir)