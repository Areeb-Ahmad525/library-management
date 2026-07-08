#!/bin/bash
set -e

# 8. Debug Information
echo "--- Debug Information ---"
pwd
whoami
hostname
ls -la
echo "-------------------------"

echo "Starting Continuous Deployment script on EC2..."

# 2. Project Directory
echo "Determining project root and navigating to it..."
PROJECT_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$PROJECT_ROOT"
echo "Project root is: $PROJECT_ROOT"

# 1. Check whether Docker is installed
echo "Checking Docker installation..."
if ! command -v docker &> /dev/null; then
  echo "Docker is not installed. Installing Docker..."
  curl -fsSL https://get.docker.com -o get-docker.sh
  sudo sh get-docker.sh
  rm get-docker.sh
  
  echo "Adding current user to the docker group..."
  sudo usermod -aG docker $USER
  
  # Flag to use sudo for docker commands since the group change requires a new shell session to propagate
  export NEED_SUDO_DOCKER=1
else
  echo "Docker is already installed."
  export NEED_SUDO_DOCKER=0
fi

# 3. Docker Service
echo "Enabling and starting Docker service (always run for safety)..."
sudo systemctl enable docker
sudo systemctl start docker

# Helper function to run docker commands safely if group propagation hasn't occurred
run_docker() {
  if [ "$NEED_SUDO_DOCKER" = "1" ] || ! docker ps &> /dev/null; then
    sudo docker "$@"
  else
    docker "$@"
  fi
}

# 6. Check whether Docker Compose is installed
echo "Checking Docker Compose installation..."
if ! run_docker compose version &> /dev/null; then
  echo "Docker Compose is missing. Installing docker-compose-plugin..."
  # 7. apt Package Cache
  sudo apt-get update -y
  sudo apt-get install -y docker-compose-plugin
else
  echo "Docker Compose is already installed."
fi

# Stop currently running containers if they exist
echo "Stopping currently running containers..."
run_docker compose down || true

# Build and start the application
echo "Building and starting containers in detached mode..."
run_docker compose up -d --build


# Verify deployment
echo "Verifying deployment..."
echo "--- Docker Process List ---"
run_docker ps
echo "--- Docker Compose Process List ---"
run_docker compose ps

# Remove unused Docker images
echo "Removing unused/dangling Docker images to free up space..."
run_docker image prune -f

echo "Deployment script completed successfully!"
