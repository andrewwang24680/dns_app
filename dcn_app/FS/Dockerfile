FROM python:3.8

# Set working directory
WORKDIR /app

# Copy application files
COPY run.py requirements.txt ./

# Install dependencies
RUN pip install -r requirements.txt

# Set the Flask app environment variable
ENV FLASK_APP=run.py

# Expose port 9090
EXPOSE 9090

# Run the application
CMD ["python", "run.py"]
