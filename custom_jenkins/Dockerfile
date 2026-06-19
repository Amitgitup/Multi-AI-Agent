# Use the Jenkins image as the base image
FROM jenkins/jenkins:lts

# Switch to root user
USER root

# Install utilities commonly needed later
RUN apt-get update && \
    apt-get install -y \
    docker.io \
    curl \
    unzip \
    python3 \
    python3-pip && \
    apt-get clean

RUN groupadd -f docker && \
    usermod -aG docker jenkins

# Switch back to Jenkins user
USER jenkins