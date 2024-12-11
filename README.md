# Battery State of Health Estimator

This Python script provides an advanced simulation of battery State of Health (SoH) estimation through integration with a FIWARE Context Broker. The program implements a sophisticated degradation model that accounts for multiple real-world factors affecting battery health, including cycle count, non-linear charging behaviors, and environmental conditions.

### Main features

#### Advanced Degradation Modeling:
- Non-linear degradation calculations based on charging and discharging patterns
- Weighted impact factors with charging behavior given higher significance
- Cycle count tracking for cumulative stress assessment
- Temperature-based degradation with optimized ranges

#### Smart Health Assessment:
- Real-time SoH percentage calculation
- Dynamic health state classification (Very Good, Good, Weak, Critical)
- Predictive time-to-critical estimation, that determines how long it will take for a battery to reach a critical SOH based on its current degradation patterns. 

### Specifications

#### Key parameters:
- Default simulation duration: 120 seconds
- Degradation rate: 0.5% (configurable)
- Optimal temperature range: 0-40°C
- Total ccle count: 120 cycles
- Maximum degradation factor: 1.0

#### Environmental Variables:
- ENTITY_ID: Target battery entity identifier
- BROKER_URL: FIWARE Context Broker endpoint
- DEFAULT_DEGRADATION_RATE: Base rate of degradation
- RUN_DURATION: Total simulation time

### Main functionalities
- Queries Context Broker for current battery parameters
-Calculates degradation using:
    - Quadratic charging behavior impact (0.001 weight)
    - Quadratic discharging behavior impact (0.0005 weight)
    - Temperature deviation effects
    - Cycle count influence

- Updates the Context Broker with new SoH values
- Runs for the specified duration, updating SoH at regular intervals.
