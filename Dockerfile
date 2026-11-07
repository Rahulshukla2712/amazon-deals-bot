FROM python:3.9-slim

WORKDIR /app

# System dependencies setup
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Run the bot script (making sure the filename matches your actual script)
CMD ["python", "deals_bot.py"]
