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
