# Use the official Python image from Docker Hub
# This images includes a complete Python installation on a Debian-based system
FROM python:3.11

# Set the working directory in the container 
# All subsequent operations will be performed under ../app
WORKDIR /app

# Copy the requirements file into the container
COPY ../requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Command to run your application
CMD ["python", "soh_estimator.py"]
