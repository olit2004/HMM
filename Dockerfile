FROM python:3.11-slim

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY server/requirements.txt /app/server/
RUN pip install --no-cache-dir -r /app/server/requirements.txt

# Copy the rest of the application code
COPY server /app/server
COPY client /app/client

WORKDIR /app/server

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
