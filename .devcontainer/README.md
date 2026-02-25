# Simple Agents Platform - Dev Container Configuration

This directory contains the configuration for VS Code Dev Containers.

## What's Included

- **devcontainer.json**: Main configuration file for the dev container
- **Dockerfile.devcontainer**: Custom Docker image for development

## Features

- Python 3.14 pre-installed
- `uv` package manager for fast dependency management
- Automatic dependency installation on container creation
- VS Code extensions pre-configured (Python, Pylance, Ruff)
- Port forwarding for API server (8000)
- Config volume mounted for easy access

## Usage

1. Open the project in VS Code
2. When prompted, click "Reopen in Container"
3. Wait for the container to build and dependencies to install
4. Start coding!

## Customization

You can modify `.devcontainer/devcontainer.json` to:

- Add additional VS Code extensions
- Change Python version
- Add environment variables
- Configure additional port forwarding
- Install additional system packages
