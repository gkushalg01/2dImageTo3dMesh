# Use CUDA 12.1 with development libraries (needed for compiling torchmcubes)
FROM nvidia/cuda:12.1.1-devel-ubuntu22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install OS dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    python3-setuptools \
    build-essential \
    cmake \
    ninja-build \
    git \
    curl \
    wget \
    unzip \
    libopenmpi-dev \
    libomp-dev \
    libgl1-mesa-glx \
    libegl1-mesa \
    libosmesa6 \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install PyTorch with CUDA 12.1 support
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Install torchmcubes with GPU (CUDA) support
RUN pip install git+https://github.com/tatsy/torchmcubes.git

# Copy the rest of your codebase
COPY . .

# Set default workdir and shell
WORKDIR /workspace
CMD ["/bin/bash"]
