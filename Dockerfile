# Use official Python image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Set environment variable for Flask
ENV FLASK_APP=app.py

ENV PYTHONPATH="${PYTHONPATH}:/app"

ENV PYTHONUNBUFFERED=1

# Run the app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
