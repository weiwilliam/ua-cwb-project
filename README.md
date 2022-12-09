# UAlbany-CWB-Project
This repo contains the python scripts and the virtual environment yaml file. \
Following is the instruction to install python and create virtual environment based on the swei's env as of Dec 7, 2022 
## Prepare your environment
### 1. Environment setup 
  After log on h6dm23, check you have HTTPS_PROXY and HTTP_PROXY set up as below. \
  export HTTPS_PROXY=proxy-s1.cwb.gov.tw:8888 \
  export http_proxy=proxy-s1.cwb.gov.tw:8888 \
  With these two environment variables, you can access the public domain outside of CWB firewall.
### 2. Download or Copy the conda install script
  Copy /nwpr/gfs/xa30/libs/Anaconda3-2022.05-Linux-x86_64.sh \
  or download (via wget) the latest anaconda or miniconda installing script at \
  https://www.anaconda.com/products/distribution#Downloads \
  It is https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh as of Dec 7, 2022. \
  For miniconda, check https://docs.conda.io/en/latest/miniconda.html and download the latest script via command below \
  ```wget the https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh``` \
  Install conda by execute the shell script.
  See https://conda.io/projects/conda/en/latest/user-guide/install/linux.html#installing-on-linux for more information.
### 3. Clone this repo
  ```
  git clone --recursive https://github.com/weiwilliam/ua-cwb-project.git name
  ```
  or 
  ```
  git clone --recursive https://github.com/weiwilliam/ua-cwb-project.git name
  cd name
  git submodule update --init --recursive
  ```
  Replace 'name' with your preferred folder name
### 4. Create virtual environment
  Create a virtual environment through
  ```
  conda env create -n name -f envs/swei_env.yaml
  ```
  Replace 'name' with your preferred env name.
### 5. Activate/deactivate your virtual environment
  ```
  conda activate name
  conda deactivate
  ```
## Use the python scripts
It will be ideal to create your local branch first.
  ```
  git checkout -b name
  ```
Replace 'name' with you preference.
### Update pylibs as needed
Update the pylibs when you need or when there are new features in master branch of pylibs you would like to use
  ```
  cd /path/to/repo_ua-cwb-project
  git fetch --recurse-submodules
  git submodule update --remote --merge
  git add pylibs
  git commit -m'messages'
  git push
  ```
You can omit the last 3 steps if you don't want to push it back to your remote branch
### Update whole repo with latest commit
Updating your local master branch regularly is recommended.
  ```
  cd /path/to/repo_ua-cwb-project
  git checkout master
  git fetch --recurse-submodules
  git pull --recurse-submodules
  ```

### Make it accessible for python
Add the full path of pylibs into PYTHONPATH in .bash_profile for BASH shell.
  ```
  export PYTHONPATH=$PYTHONPATH:/path/to/pylibs
  ```
Then it should be able to use all the functions I defined in pylibs after ```source .bash_profile```.

### Check comments in the script to learn how to run it.

