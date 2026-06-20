FROM jenkins/jenkins:lts

USER root

RUN apt-get update && \
    apt-get install -y \
    docker.io \
    curl \
    unzip \
    python3 \
    python3-pip && \
    apt-get clean

# Match Docker Desktop's docker group GID
RUN groupadd -g 1001 docker-host || true && \
    usermod -aG 1001 jenkins

USER jenkins