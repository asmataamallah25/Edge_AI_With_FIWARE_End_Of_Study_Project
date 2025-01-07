# Edge AI With FIWARE - Generate custom recommendation for the Battery State of Health 
# Edge AI With FIWARE End Of Study Project

## Project Overview
This project focuses on integrating Edge AI capabilities with FIWARE, implementing recommendation systems in the edge AI solution using the Phi-3.5 model with Unsloth optimization.

## Features
- Custom recommendations based on State of Health (SOH)
- Edge computing integration with FIWARE
- Optimized inference using Unsloth

## Technical Requirements
- Python 3.x
- Dependencies:
  - PyTorch 2.4.0+
  - Transformers 4.46+
  - Unsloth 2024.12.4
  - Datasets 3.2.0
  - XFormers 0.0.28
  - Triton 3.1.0

## Model Architecture
- Base Model: unsloth/Phi-3.5-mini-instruct
- Maximum sequence length: 2048 tokens
- 4-bit quantization enabled
- Optimized for GPU acceleration

## Training Configuration
**PEFT Settings**
- LoRA adaptation (rank 16)
- Target modules: attention and FFN layers
- Training parameters:
  - Batch size: 2
  - Gradient accumulation: 4 steps
  - Learning rate: 2e-4
  - Training steps: 60

## Contributing
Feel free to contribute to this project by forking the repository, creating your own branch and submitting a pull request with your improvements. We welcome all contributions that enhance the functionality or performance of the system.



