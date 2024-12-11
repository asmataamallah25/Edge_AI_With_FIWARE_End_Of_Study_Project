import random
import pandas as pd
import math
import pybamm
#from config import DEGRADATION_RATES, CHARGING_BEHAVIORS, MINIMUM_SOH
from config import DEGRADATION_RATES, CHARGING_BEHAVIORS, MINIMUM_SOH, pybamm_model

def simulate_battery_data(start_date, end_date, initial_soh=100, usage_frequency='normal', charging_behavior='optimal'):
    """
    Simulate battery data over a specified time period.

    This function generates synthetic battery data based on various parameters such as
    usage frequency, charging behavior, and temperature. It simulates daily
    battery usage and calculates State of Health (SOH) degradation over time.

    Parameters:
    -----------
    start_date : str or datetime
        The start date of the simulation period.
    end_date : str or datetime
        The end date of the simulation period.
    initial_soh : float, optional (default=100)
        The initial State of Health of the battery (percentage).
    usage_frequency : str, optional (default='normal')
        The frequency of battery usage. Can be 'low', 'normal', or 'high'.
    charging_behavior : str, optional (default='optimal')
        The charging behavior pattern. Can be 'optimal', 'full', 'frequent_top_ups', or 'deep_discharge'.

    Returns:
    --------
    pandas.DataFrame
        A DataFrame containing daily battery data including date, temperature, charging details,
        cycle information, and State of Health (SOH).

    Notes:
    ------
    - The function uses predefined degradation rates and charging behaviors from a config file.
    - Temperature effects and cycling effects are considered in SOH degradation calculations.
    - The minimum SOH is capped at 70%.
    - Extreme temperature events are simulated with a 10% probability.
    """

    start_date = pd.Timestamp(start_date)
    end_date = pd.Timestamp(end_date)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    data = []
    soh = initial_soh
    total_cycles = 0

    # PyBaMM model
    model, param = pybamm_model()
    
    # Get the target degradation range for this scenario
    min_degradation, max_degradation = DEGRADATION_RATES[(usage_frequency, charging_behavior)]
    
    # Calculate daily degradation rate
    total_days = (end_date - start_date).days
    daily_degradation_min = min_degradation / total_days
    daily_degradation_max = max_degradation / total_days
    

    for date in date_range:
        # Temperature simulation with occasional extreme events
        season = (date.month % 12 + 3) // 3
        if season == 1:  # Winter
            temp = random.uniform(-10, 10)
        elif season == 2:  # Spring
            temp = random.uniform(5, 25)
        elif season == 3:  # Summer
            temp = random.uniform(15, 35)
        else:  # Autumn
            temp = random.uniform(0, 20)
        
        # Extreme temperature introduction 
        if random.random() < 0.10:  # 10% chance of an extreme temperature event
            temp = random.choice([random.uniform(-20, -10), random.uniform(40, 50)])
        
        # Charging behavior
        charge_start, charge_end = CHARGING_BEHAVIORS[charging_behavior]

        # Occasional full charge for 'optimal' and 'frequent_top_ups'
        if charging_behavior in ['optimal', 'frequent_top_ups'] and random.random() < 0.1:
            charge_end = 100
        
        # Daily cycles calculation (low, normal & high usage)
        if usage_frequency == 'low':
            daily_cycles = random.uniform(0.2, 0.5)
        elif usage_frequency == 'normal':
            daily_cycles = random.uniform(0.5, 1)
        else:  # high usage
            daily_cycles = random.uniform(1, 2)
        
        # Total cycles are calculated on a daily basis
        total_cycles += daily_cycles
        
        # Create PyBaMM experiment for this day
        experiment = create_daily_experiment(charging_behavior, daily_cycles)

        # Create a new simulation object for each iteration
        sim = pybamm.Simulation(model, parameter_values=param, experiment=experiment)

        # Solve PyBaMM simulation for this day
        solution = sim.solve()

        # Calculate SOH degradation
        # Degradation rates claculation based on the input parameters depending on the scenarios of usage and charge (in config file) 
        base_degradation = random.uniform(daily_degradation_min, daily_degradation_max) * 100  # Amplify the effect 
        
        # Temperature effect
        # Assuming that the ideal temp ranges of a battery are between 15 and 35, degradation of lower and higher temp is refelected
        if temp > 35:
            temp_factor = 1 + 0.15 * ((temp - 35) / 10)
        elif temp < 15:
            temp_factor = 1 - 0.10 * ((15 - temp) / 10)
        else:
            temp_factor = 1
        
        # Simplified cycle effect
        cycle_factor = 1 + 0.1 * math.sqrt(total_cycles / (365 * 4))  # Assuming max cycles over 3 years

        capacity = solution["Discharge capacity [A.h]"].data[-1]
        initial_capacity = param["Nominal cell capacity [A.h]"]
        capacity_loss = (1 - capacity / initial_capacity) * 100
        
        soh_degradation = (base_degradation* (1 + capacity_loss / 100)) * temp_factor * cycle_factor
        
        soh -= soh_degradation
        soh = max(soh, MINIMUM_SOH)  # Assuming minimum SOH of 70%
        
        # Generated Dataset 
        # The dataset will have the following features and the target/label is SOH (in a supervised learning context)
        data.append({
            'Date': date,
            'Temperature': temp,
            'Charge_Start': charge_start,
            'Charge_End': charge_end,
            'Daily_Cycles': daily_cycles,
            'Total_Cycles': total_cycles,
            'SOH': soh
        })
    
    return pd.DataFrame(data)

def create_daily_experiment(charging_behavior, daily_cycles):
    charge_start, charge_end = CHARGING_BEHAVIORS[charging_behavior]
    
    # Convert SOC percentages to approximate voltage values
    # Assuming 3.0V at 0% SOC and 4.2V at 100% SOC
    voltage_low = 3.0 + (charge_start / 100) * 1.2 
    voltage_high = 3.0 + (charge_end / 100) * 1.2

    return pybamm.Experiment([
        (f"Discharge at {daily_cycles}C until {voltage_low}V",
         f"Charge at {daily_cycles}C until {voltage_high}V")
    ])