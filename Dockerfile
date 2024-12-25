# Use Python slim image
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libssl-dev libffi-dev libxml2-dev libxslt1-dev zlib1g-dev curl git

# Set the working directory in the container
WORKDIR /app

# Copy only requirements.txt first (to leverage Docker caching)
COPY requirements.txt requirements.txt

# Install Python dependencies (use PIP cache if available)
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Set the default command to run Scrapy spider
CMD ["scrapy", "crawl", "splash_spider"]
