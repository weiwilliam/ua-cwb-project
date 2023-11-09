# UAlbany-CWB-Project
This repo contains the python scripts and the virtual environment yaml file. \
Following is the instruction to install python and create virtual environment based on the swei's env as of Dec 7, 2022 
## Prepare your environment
### 1. Environment setup 
  After log on h6dm23, check you have HTTPS_PROXY and HTTP_PROXY set up as below. \
  export HTTPS_PROXY=proxy-s1.cwb.gov.tw:8888 \
  export http_proxy=proxy-s1.cwb.gov.tw:8888 \
  With these two environment variables, you can access the public domain outside of CWB firewall. \
  **Note: as of Nov 8, 2023, it can't reach public domain through the proxy sever**
### 2. Download or Copy the conda install script
  Copy /nwpr/gfs/xa30/libs/Anaconda3-2022.05-Linux-x86_64.sh \
  or download (via wget) the latest anaconda or miniconda installing script at \
  https://www.anaconda.com/products/distribution#Downloads \
  It is https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh as of Dec 7, 2022. \
  \
  For miniconda, check https://docs.conda.io/en/latest/miniconda.html \
  and download the latest script via command below \
  ```wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh``` \
  Install conda by execute the shell script.
  See https://conda.io/projects/conda/en/latest/user-guide/install/linux.html#installing-on-linux for more information.
### 3. Clone this repo
  ```
  git clone --recursive https://github.com/weiwilliam/ua-cwb-project.git <dirname>
  ```
  or 
  ```
  git clone --recursive https://github.com/weiwilliam/ua-cwb-project.git <dirname>
  cd <dirname>
  git submodule update --init --recursive
  ```
### 4. Create virtual environment
  Create a virtual environment through
  ```
  conda create -n <envname> -f envs/swei_env.yaml
  ```
  You can call your virtual environment by any name you prefer.
  It will create the environment based on my installed package.
  
### 5. Activate/deactivate your virtual environment
  ```
  conda activate <envname>
  conda deactivate
  ```
## Use the python scripts
It will be ideal to create your local branch first based on master branch.
  ```
  git checkout -b <branch_name>
  ```

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
Replace the "/path/to/pylibs" with your absolute path of pylibs under the repo. \
Then it should be able to use all the functions I defined in pylibs after ```source .bash_profile```.

### Sync the dmsdb from inside HPC to outside HPC
Modify the paths in scripts/sync_dmsdb.sh to your environment
```
mydmsdb=/nwpr/gfs/xa30/data/dmsdb
# Target inside dmsdb path
inside_dmsdb=/nwpr/gfs/xa30/data/dmsdb
inside_ufsnm=TCo383L72
outside_ufsnm=TCo383L72
inside_dmsfd=EFFR22080100GIMG
```
Run it to copy it to outside HPC for plotting.

### Check comments in the script to learn how to run it.
Check pyscripts/plot_2dmap.py \
Changes to these lines may be needed \
https://github.com/weiwilliam/ua-cwb-project/blob/1f5ce19e160e711f528d5621b87b551007a0ec05/pyscripts/plot_2dmap.py#L34-L67

