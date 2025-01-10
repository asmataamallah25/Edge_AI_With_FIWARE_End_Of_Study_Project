FROM python:3.9-slim

WORKDIR /app
COPY arima_model.pkl .
COPY predict.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "predict:app", "--host", "0.0.0.0", "--port", "8000"]

