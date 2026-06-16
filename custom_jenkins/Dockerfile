# Use the Jenkins image as the base image
FROM jenkins/jenkins:lts

# Switch to root user
USER root

# Install utilities commonly needed later
RUN apt-get update && \
    apt-get install -y \
    curl \
    unzip \
    python3 \
    python3-pip && \
    apt-get clean

# Switch back to Jenkins user
USER jenkins