# Add graphics drivers PPA and install nvidia driver 570
sudo add-apt-repository ppa:graphics-drivers/ppa -y && \
sudo apt update && \
sudo apt install -y nvidia-driver-570 && \

echo "Installed NVIDIA driver 570. Reboot your system to apply changes. Then 'bash 2-install-nvidia-cuda.sh' to install CUDA toolkit and cuDNN."
