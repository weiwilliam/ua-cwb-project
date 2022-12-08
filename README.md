# UAlbany-CWB-Project
This repo contains the python scripts and the virtual environment yaml file. \
Following is the instruction to install python and create virtual environment based on the swei's env as of Dec 7, 2022 
## 1. Environment setup 
  After log on h6dm23, check you have HTTPS_PROXY and HTTP_PROXY set up as below. \
  export HTTPS_PROXY=proxy-s1.cwb.gov.tw:8888 \
  export http_proxy=proxy-s1.cwb.gov.tw:8888 \
  With these two environment variables, you can access the public domain outside of CWB firewall.
## 2. Download or Copy the conda install script
  Copy /nwpr/gfs/xa30/libs/Anaconda3-2022.05-Linux-x86_64.sh \
  or download (via wget) the latest anaconda or miniconda installing script at \
  https://www.anaconda.com/products/distribution#Downloads \
  It is https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh as of Dec 7, 2022. \
  For miniconda, check https://docs.conda.io/en/latest/miniconda.html and download the latest script via command below \
  ```wget the https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh``` \
  Install conda by execute the shell script.
## 3. Create virtual environment
  
