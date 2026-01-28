# uu_framework Build Environment
# Docker image for building the static site

FROM node:20-alpine

# Install Python 3 and PyYAML for preprocessing scripts
RUN apk add --no-cache \
    python3 \
    py3-pip \
    py3-yaml

# Set working directory
WORKDIR /app

# Copy package files first for better layer caching
COPY uu_framework/eleventy/package*.json ./

# Install Node.js dependencies
RUN npm install

# Copy framework files
COPY uu_framework/ ./uu_framework/

# Create output directory
RUN mkdir -p _site

# Default command runs the full build pipeline
CMD ["sh", "-c", "python3 uu_framework/scripts/preprocess.py && npx @11ty/eleventy"]
