sudo apt-get --purge remove '*cublas*' '*cufft*' '*curand*' '*cusolver*' '*cusparse*' \
'*npp*' '*nvjpeg*' '*cuda*' '*nsight*' 'libcudnn*' 'libnv*' 'nvidia-*' -y && \
sudo apt-get autoremove -y && \
sudo apt-get autoclean -y && \
sudo rm -rf /usr/local/cuda* && echo "NVIDIA drivers and CUDA have been uninstalled."
