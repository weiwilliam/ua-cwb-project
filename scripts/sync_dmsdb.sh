#!/bin/ksh
# 
# Sync the inside dmskeys to outside CWBHPC
#

# Outisde dmsdb path
mydmsdb=/nwpr/gfs/xa30/data/dmsdb
# Target inside dmsdb path
inside_dmsdb=/nwpr/gfs/xb173/data/dmsdb
inside_ufsnm=TCo383L72
outside_ufsnm=TCo383L72DG
inside_dmsfd=NAER22050100GIMG

if [ ! -d ${mydmsdb}/${outside_ufsnm}.ufs ]; then
   mkdir -p ${mydmsdb}/${outside_ufsnm}.ufs
fi
cd ${mydmsdb}/${outside_ufsnm}.ufs
rsync -r ${USER}@h6dm15:${inside_dmsdb}/${inside_ufsnm}.ufs/${inside_dmsfd} .
