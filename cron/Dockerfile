FROM ubuntu:latest

RUN apt-get update && apt-get -y install cron curl

# Copy hello-cron file to the cron.d directory
COPY cron_jobs /etc/cron.d/cron_jobs
 
# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/cron_jobs

# Apply cron job
RUN crontab /etc/cron.d/cron_jobs
 
# Create the log file to be able to run tail
RUN touch /var/log/cron.log
 
# Run the command on container startup
CMD cron && tail -f /var/log/cron.log
