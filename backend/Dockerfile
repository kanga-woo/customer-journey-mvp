FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Upgrade pip to avoid compatibility issues
RUN pip install --upgrade pip

# Install Redis first to avoid potential conflicts
RUN pip install redis==6.0.0

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose necessary ports or run your application
EXPOSE 8000
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
