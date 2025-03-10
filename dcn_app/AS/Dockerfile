FROM python:3.8

# Set working directory
WORKDIR /app

# Copy application files
COPY run.py dns_records.json requirements.txt ./

# Install dependencies
RUN pip install -r requirements.txt

# Expose UDP port 53533
EXPOSE 53533/udp

# Run the DNS server
CMD ["python", "run.py"]