

nvidia-smi && \
# Check if NVIDIA driver is installed
if [ $? -eq 0 ]; then
    echo "NVIDIA driver is already installed."
else
    echo "NVIDIA driver is not installed. Please install it first by running 1-install-nvidia-drivers.sh."
    exit 1
fi

# Download CUDA 12.1 repo package
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-ubuntu2204.pin && \
sudo mv cuda-ubuntu2204.pin /etc/apt/preferences.d/cuda-repository-pin-600 && \

# Add NVIDIA CUDA 12.1 repo
wget https://developer.download.nvidia.com/compute/cuda/12.1.0/local_installers/cuda-repo-ubuntu2204-12-1-local_12.1.0-530.30.02-1_amd64.deb && \
sudo dpkg -i cuda-repo-ubuntu2204-12-1-local_12.1*.deb && \
sudo cp /var/cuda-repo-ubuntu2204-12-1-local/cuda-*-keyring.gpg /usr/share/keyrings/ && \
sudo apt update && \
sudo apt install -y cuda-toolkit-12-1 && \
# sudo apt install libcudnn9 libcudnn9-dev -y && \
echo "Installed CUDA toolkit 12.1.105. Installing cuDNN 9.8." && \
 

wget https://developer.download.nvidia.com/compute/cudnn/9.8.0/local_installers/cudnn-local-repo-ubuntu2204-9.8.0_1.0-1_amd64.deb && \
sudo dpkg -i cudnn-local-repo-ubuntu2204-9.8.0_1.0-1_amd64.deb && \
sudo cp /var/cudnn-local-repo-ubuntu2204-9.8.0/cudnn-*-keyring.gpg /usr/share/keyrings/ && \
sudo apt update && \
sudo apt install -y cudnn-cuda-12 && \
export PATH=/usr/local/cuda-12.1/bin:$PATH && \
export LD_LIBRARY_PATH=/usr/local/cuda-12.1/lib64:$LD_LIBRARY_PATH && \
source ~/.bashrc  && \
echo "Installed cuDNN 9.8. Reboot your system to apply changes. Check using nvcc -V and nvidia-smi commands after reboot."
