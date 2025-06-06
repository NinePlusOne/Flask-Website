# Use a slim Python base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose the default Hugging Face Spaces port
EXPOSE 7860

# Run the app
CMD ["python", "app.py"]
