import pybamm
# Battery simulation scenarios
#(usage frequency, charging behaviour)
#simulate various battery usage patterns
SCENARIOS = [
   #('usage', 'frequency')
    ('low', 'optimal'),
    ('normal', 'optimal'),
    ('normal', 'full'),
    ('normal', 'frequent_top_ups'),
    ('normal', 'deep_discharge'),
    ('high', 'optimal')
]

# Degradation rates of the State of Health(SOH) for each scenario
#(usage frequency, charging behaviour): (min_degradation, max_degradation)
DEGRADATION_RATES = {
    ('low', 'optimal'): (0.05, 0.10),
    ('normal', 'optimal'): (0.10, 0.15),
    ('normal', 'full'): (0.15, 0.20),
    ('normal', 'frequent_top_ups'): (0.12, 0.18),
    ('normal', 'deep_discharge'): (0.18, 0.25),
    ('high', 'optimal'): (0.18, 0.25)
}

# Battery charging patterns 
CHARGING_BEHAVIORS = {
    'optimal': (20, 80),
    'full': (10, 100),
    'frequent_top_ups': (60, 80),
    'deep_discharge': (5, 95)
}

# SOH configuration parameters
INITIAL_SOH = 100
MINIMUM_SOH = 70

# Battery model
def pybamm_model():
    model = pybamm.lithium_ion.SPM()
    param = model.default_parameter_values
    return model, param

# Folder name in which the synthtic data is saved
OUTPUT_DIR = "synthetic_datasets"