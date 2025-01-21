FROM python:3.9-slim

# Install dependencies
WORKDIR /app
RUN pip install --no-cache-dir selenium==4.28.0

# Copy the Selenium script
COPY check_enrollment.py /app/

# Default command to run the script
CMD ["python", "check_enrollment.py"]
