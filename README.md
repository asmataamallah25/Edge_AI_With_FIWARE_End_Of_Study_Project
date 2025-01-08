# Edge AI With FIWARE - Battery SOH Dataset Generation

## Overview
This branch contains the dataset generation module for battery State of Health (SOH) prediction using PyBaMM simulation. The generated dataset is optimized for edge processing and includes critical operational parameters affecting battery degradation.

## Features
- Physics-based battery simulation
- Customizable degradation scenarios
- Environmental condition modeling
- Multiple charging patterns
- Usage frequency variations
- Exploratory data analysis tools

## Installation

1. Clone the repository and switch to data_generation branch:
```
git clone https://github.com/asmataamallah25/Edge_AI_With_FIWARE_End_Of_Study_Project.git
cd Edge_AI_With_FIWARE_End_Of_Study_Project
git checkout data_generation
```

2. Create and activate virtual environment:
```
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

3. Install dependencies:
```
pip install -r requirements.txt
```

## Dataset Parameters
The generated dataset includes:
- Daily temperature readings
- Charging cycle information
- Usage patterns
- Cumulative cycles
- State of Health (SOH)

## Exploratory Analysis
Launch Jupyter notebook:
```
jupyter notebook notebooks/exploratory_analysis.ipynb
```

## Contributing
Feel free to contribute to this project by forking the repository, creating your own branch and submitting a pull request with your improvements. We welcome all contributions that enhance the functionality or performance of the solution.

## Author
Asma Taamallah
