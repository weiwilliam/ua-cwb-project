#!/usr/bin/env python3
#
# @author: Shih-Wei Wei
#
import sys, os, platform
from pathlib import Path
import numpy as np
import pandas as pd
import xarray as xa
from datetime import datetime, timedelta
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as mpcrs
import cartopy.crs as ccrs
import cartopy.feature as cft

from utils import setup_cmap, get_dates, find_cnlvs
from plot_utils import setupax_2dmap,set_size
from TCo_latlon_def import define_latlon
from lib_dms import read_dms, find_dms_longname
import setuparea as setarea

# Plotting setup
txsize=12
mpl.rc('axes',titlesize=12,labelsize=12)
mpl.rc('xtick',labelsize=12)
mpl.rc('ytick',labelsize=12)
mpl.rc('legend',fontsize='large')
axe_w=6; axe_h=6
quality=300
minussign=u'\u2212'

# Setup the path of dmsdb and output sub-folder name
rootdms='/nwpr/gfs/xa30/data/dmsdb'
savedir='ualb_oldnew_fix'

# Default folder is "images" in repo, modify it accordingly
imagesdir=str((Path(__file__).parent/'..').resolve())
outputpath=imagesdir+'/images/2dmap/'+savedir
if ( not os.path.exists(outputpath) ):
    os.makedirs(outputpath)

# Setup the experiment .ufs folder
expufs=['TCo383L72.ufs','TCo383L72.ufs']
# Setup the 4-digit tag of the DMS
expdms=['ALB1','ALB2']
# Setup the jcap for lat/lon definition
expjcap=[383,383]
# Setup the label name using in figures
exp_nm=['OldFix','NewFix']

# Setup the plotting variable, it will find the longname definition in pylibs
pltvar='100'
dmstag='GIMG'
if dmstag=='GIMG':
    if 'M' == pltvar[0]:
        keytag=dmstag
    else:
        keytag='GI0G'
    grdtag='H1191936'

levlist = [ 10,  20,  30,  50,  70,
           100, 150, 200, 250, 300,
           400, 500, 700, 850, 925]
   
sdate=2022110100
edate=2022110100
cycint=6
fhmin=0
fhmax=120
fhint=6

cblb=find_dms_longname(pltvar)
print('Plotting '+cblb)
area='Glb'
pltave=0 # 0: single cycle only; 1: time average
pltfhrave=1 # 0: separate fhr only; 1: average over fhr
tkfreq=2

fhrlist=list(np.arange(fhmin,fhmax+.1,fhint))
   
#cnlvs=np.array((0., 0.05, 0.1, 0.15, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.5, 2.5))

# Constant configuration
proj=ccrs.PlateCarree()
grav=9.80665e+0

# Setup plotting area
minlon, maxlon, minlat, maxlat, crosszero, cyclic=setarea.setarea(area)
print(minlat,maxlat,minlon,maxlon,crosszero,cyclic)
if (area=='Glb'):
   minlon=-180. ; maxlon=180.
else:
   minlon=(minlon+180)%360-180
   maxlon=(maxlon+180)%360-180
cornerll=[minlat,maxlat,minlon,maxlon]

dates = get_dates(sdate,edate,cycint)

# Define lat/lon of the Gaussian grid based on jcap number
lat,lon=define_latlon(jcap=383)
lon=(lon+180)%360-180

dates_count=0
for cdate in dates:
    yy=cdate.strftime('%Y')
    mm=cdate.strftime('%m')
    dd=cdate.strftime('%d')
    hh=cdate.strftime('%H')
    dtg=cdate.strftime('%y%m%d%H')
    cdt=cdate.strftime('%Y%m%d%H')

    for eidx,(ufsn,dmsn) in enumerate(zip(expufs,expdms)):
        dtgdir=dmsn+dtg+dmstag
        inputpath=os.path.join(rootdms,ufsn,dtgdir)
        for fidx,fhr in enumerate(fhrlist):
            fhrdir='%s%.6i' %(cdt,fhr)
            for lvidx, lev in enumerate(levlist):
                 keyfile='%.3i%s%s%s' %(lev,pltvar,keytag,grdtag)
                 indmskey=os.path.join(inputpath,fhrdir,keyfile)
                 print('Processing on: '+indmskey, flush=1)
                 tmp=read_dms(indmskey).reshape(lat.size,lon.size)
                 tmpds=xa.Dataset({'pltvar':(['lat','lon'],tmp)},coords={'lat':lat,'lon':lon})
                 tmpds=tmpds.sortby('lon')
                 if lvidx==0:
                     levds=tmpds
                 else:
                     levds=xa.concat((levds,tmpds),dim='lev')
            if fidx==0:
               fhrds=levds
            else:
               fhrds=xa.concat((fhrds,levds),dim='fhr')
        if eidx==0:
           expds=fhrds
        else:
           expds=xa.concat((expds,fhrds),dim='exp')
    if dates_count==0:
       allds=expds
    else:
       allds=xa.concat((allds,expds),dim='time')
    dates_count+=1

allds=allds.assign_coords({'exp':exp_nm,'fhr':fhrlist,'time':dates,'lev':levlist})
if area!='Glb':
    tmpds=allds.sel(lon=slice(minlon,maxlon),lat=slice(minlat,maxlat))
else:
    tmpds=allds

diff=tmpds.diff(dim='exp').sel(exp=exp_nm[1])
difflvs=find_cnlvs(diff.pltvar.data,ntcks=21,eqside=1)
clridx=[]
for idx in np.linspace(2,254,difflvs.size):
    clridx.append(int(idx))
diffcmap=setup_cmap('BlueYellowRed',clridx)
diffnorm = mpcrs.BoundaryNorm(difflvs,len(clridx)+1,extend='both')

for cdate in dates:
    cdt=cdate.strftime('%Y%m%d%H')
    plttmp=diff.sel(time=cdate).mean(dim=['lat','lon'])

    tmplvs=find_cnlvs(plttmp.pltvar.data,ntcks=21,eqside=1)
    clridx=[]
    for idx in np.linspace(2,254,tmplvs.size):
        clridx.append(int(idx))
    tmpcmap=setup_cmap('BlueYellowRed',clridx)
    tmpnorm = mpcrs.BoundaryNorm(tmplvs,len(clridx)+1,extend='both')

    tistr='%s%s%s %s' %(exp_nm[1],minussign,exp_nm[0],cdt) 
    outname='%s/Diff_Crossec_%s-%s_%s.%s.png' %(outputpath,exp_nm[1],exp_nm[0],pltvar,cdt)

    fig, ax = plt.subplots()
    set_size(axe_w,axe_h,b=0.15,l=0.15,r=0.95,t=0.95)
    pm = ax.pcolormesh(plttmp.fhr,plttmp.lev,plttmp.pltvar.data.swapaxes(0,1),cmap=tmpcmap,norm=tmpnorm)
    ax.set_title(tistr,loc='left')
    plt.colorbar(pm,ax=ax,orientation='horizontal',ticks=difflvs[::tkfreq],
                 fraction=0.045,aspect=40,pad=0.08,label=cblb)
    print(outname,flush=1)
    fig.savefig(outname,dpi=quality)
    plt.close()
#
#    if (pltfhrave):
#        plttmp=diff.sel(time=cdate).mean(dim='fhr')
#        tistr='%s%s%s %s fhr ave.' %(exp_nm[1],minussign,exp_nm[0],cdt) 
#        outname='%s/DiffAve_%s-%s_%s.%s.png' %(outputpath,exp_nm[1],exp_nm[0],pltvar,cdt)
#
#        tmplvs=find_cnlvs(plttmp.pltvar.data,ntcks=21,eqside=1)
#        clridx=[]
#        for idx in np.linspace(2,254,tmplvs.size):
#            clridx.append(int(idx))
#        tmpcmap=setup_cmap('BlueYellowRed',clridx)
#        tmpnorm = mpcrs.BoundaryNorm(tmplvs,len(clridx)+1,extend='both')
#
#        fig,ax,gl=setupax_2dmap(cornerll,area,proj,lbsize=txsize)
#        set_size(axe_w,axe_h,b=0.13,l=0.05,r=0.95,t=0.95)
#        cn=ax.contourf(plttmp.lon,plttmp.lat,plttmp.pltvar.data,levels=tmplvs,cmap=tmpcmap,norm=tmpnorm,extend='both')
#        ax.set_title(tistr,loc='left')
#        plt.colorbar(cn,ax=ax,orientation='horizontal',ticks=tmplvs[::tkfreq],
#                     fraction=0.045,aspect=40,pad=0.08,label=cblb)
#        if (area=='NAmer'):
#           ax.add_feature(cft.STATES,zorder=2)
#        print(outname)
#        fig.savefig(outname,dpi=quality)
#        plt.close()
 
