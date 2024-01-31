FROM python:3.11

# Copy the application to the container
COPY . /app

# Set the working directory
WORKDIR /app

# Install dependencies
RUN pip install -r requirements.txt

# Expose port 80
EXPOSE 80

# Configure Streamlit
RUN mkdir ~/.streamlit
RUN cp .streamlit/config.toml ~/.streamlit/config.toml
RUN cp .streamlit/credentials.toml ~/.streamlit/credentials.toml

# Set the working directory again
WORKDIR /app

# Cron job to run scraper/run_scrapers.py at 23:00 every day
RUN echo "0 23 * * * cd /app && python scraper/run_scrapers.py >> /var/log/scrapers.log 2>&1" > /etc/cron.d/scrapers

# Cron job to run src/utils/rag.py at 23:30 on Monday, Wednesday and Friday
RUN echo "30 23 * * 1,3,5 cd /app && python src/utils/rag.py >> /var/log/rag.log 2>&1" > /etc/cron.d/rag

# Provide execute permissions for cron scripts
RUN chmod 0644 /etc/cron.d/scrapers
RUN chmod 0644 /etc/cron.d/rag

# Start the application with Streamlit
ENTRYPOINT ["streamlit", "run"]

# Default command
CMD ["main.py"]
