FROM mcr.microsoft.com/devcontainers/python:3.12-bullseye

# hadolint ignore=DL3008
RUN apt-get update && apt-get install -y --no-install-recommends \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg \
        jq \
        lsb-release \
        shellcheck \
        unzip \
        vim \
    && rm -rf /var/lib/apt/lists/*

# # Install Azure CLI latest (2.51.0)
# RUN curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash && echo "az --version"

# # Install bicep
# RUN az bicep install

# Helpful aliases
# hadolint ignore=SC2016
RUN echo 'alias ll='"'"'ls $LS_OPTIONS -al'"'"'' >> /etc/bash.bashrc

# Install Python requirements
# hadolint ignore=DL3013
RUN python -m pip install --no-cache-dir --upgrade pip
COPY ./requirements.txt .
COPY ./requirements_dev.txt .
RUN python -m pip install --no-cache-dir -r ./requirements_dev.txt
