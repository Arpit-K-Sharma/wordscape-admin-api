# Using Python Image
FROM --platform=linux/amd64 python:3.12.3-slim

# Setting the working directory in the app
WORKDIR /app

# Copying the requirements.txt into the container
COPY requirements.txt .

# Installing the dependencies with requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copying the rest of the application code
COPY . .

EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
