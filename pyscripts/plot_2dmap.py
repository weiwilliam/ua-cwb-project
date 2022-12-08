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

from utils import setup_cmap, ndate, find_cnlvs
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
axe_w=6; axe_h=4
quality=300
minussign=u'\u2212'

# Setup the path of dmsdb and output sub-folder name
rootdms='/nwpr/gfs/xa30/data/dmsdb'
savedir='debug'

# Default folder is "images" in repo, modify it accordingly
imagesdir=str((Path(__file__).parent/'..').resolve())
outputpath=imagesdir+'/images/2dmap/'+savedir
if ( not os.path.exists(outputpath) ):
    os.makedirs(outputpath)

# Setup the experiment .ufs folder
expufs=['TCo383L72.ufs','TCo383L72DG.ufs']
expdms=['NAER','NAER']
exp_nm=['Ctrl','TestDG']
expjcap=[383,383]

dmstag='GIMG'
if dmstag=='GIMG':
   keytag='GI0G'
   grdtag='H1191936'
   
sdate=2022050100
edate=2022050100
cycint=6
fhmax=24
fhint=6

# Setup the plotting variable, it will find the longname definition in pylibs
pltvar='S00310'
cblb=find_dms_longname(pltvar)
area='Glb'
pltave=0 # 0: single cycle only 1: time average
tkfreq=1

fhrlist=list(np.arange(0,fhmax+.1,fhint))
if pltvar[:3]=='S00':
   cnlvs=np.array((0,100,200,300,400,500,600,700,800,900,1000,1100))
   
#cnlvs=np.array((0., 0.05, 0.1, 0.15, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.5, 2.5))
clridx=np.array((0,2,4,7,8,9,10,12,14,15,16,17,18))
clrmap=setup_cmap('precip3_16lev',clridx)
clrnorm = mpcrs.BoundaryNorm(cnlvs,len(clridx),extend='both')

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

date1=pd.to_datetime(sdate,format="%Y%m%d%H")
date2=pd.to_datetime(edate,format="%Y%m%d%H")
delta = timedelta(hours=cycint)
dates = pd.date_range(start=date1, end=date2, freq=delta)

# Define lat/lon of the Gaussian grid based on jcap number
lat,lon=define_latlon(jcap=383)
lon=(lon+180)%360-180

tnum=0
dlist=[]
cdate=sdate
while (cdate<=edate):
    dlist.append(str(cdate))
    tnum=tnum+1
    cdate=ndate(cycint,cdate)

dates_count=0
for date in dlist:
    yy=date[:4] ; mm=date[4:6] ; dd=date[6:8] ; hh=date[8:10]
    dtg=date[2:10]

    for eidx,(ufsn,dmsn) in enumerate(zip(expufs,expdms)):
        dtgdir=dmsn+dtg+dmstag
        inputpath=os.path.join(rootdms,ufsn,dtgdir)
        for fidx,fhr in enumerate(fhrlist):
            fhrdir='%s%.6i' %(date,fhr)
            keyfile='%s%s%s' %(pltvar,keytag,grdtag)
            indmskey=os.path.join(inputpath,fhrdir,keyfile)
            print('Processing on: '+indmskey, flush=1)
            tmp=read_dms(indmskey).reshape(lat.size,lon.size)
            tmpds=xa.Dataset({'pltvar':(['lat','lon'],tmp)},coords={'lat':lat,'lon':lon})
            tmpds=tmpds.sortby('lon')
            if fidx==0:
               fhrds=tmpds
            else:
               fhrds=xa.concat((fhrds,tmpds),dim='fhr')
        if eidx==0:
           expds=fhrds
        else:
           expds=xa.concat((expds,fhrds),dim='exp')
    if dates_count==0:
       allds=expds
    else:
       allds=xa.concat((allds,expds),dim='time')
    dates_count+=1

allds=allds.assign_coords({'exp':exp_nm,'fhr':fhrlist,'time':dlist})
if area!='Glb':
   tmpds=allds.sel(lon=slice(minlon,maxlon),lat=slice(minlat,maxlat))

for date in dlist:
    for fhr in fhrlist:
        pltdata=allds.sel(time=date,fhr=fhr)
        for explb in exp_nm:
            plttmp=pltdata.sel(exp=explb)
            tistr='%s %s_f%.3i' %(explb,date,fhr) 
            outname='%s/%s_%s.%s_f%.3i.png' %(outputpath,explb,pltvar,date,fhr)

            fig,ax,gl=setupax_2dmap(cornerll,area,proj,lbsize=txsize)
            set_size(axe_w,axe_h,b=0.13,l=0.1,r=0.95,t=0.95)
            cn=ax.contourf(plttmp.lon,plttmp.lat,plttmp.pltvar.data,levels=cnlvs,norm=clrnorm,cmap=clrmap,extend='both')
            ax.set_title(tistr,loc='left')
            plt.colorbar(cn,ax=ax,orientation='horizontal',ticks=cnlvs[::tkfreq],
                         fraction=0.045,aspect=40,pad=0.08,label=cblb)
            if (area=='NAmer'):
               ax.add_feature(cft.STATES,zorder=2)
            print(outname,flush=1)
            fig.savefig(outname,dpi=quality)
            plt.close()

diff=allds.diff(dim='exp').sel(exp=exp_nm[1])
difflvs=find_cnlvs(diff.pltvar.data,ntcks=21,eqside=1)
clridx=[]
for idx in np.linspace(2,254,difflvs.size):
    clridx.append(int(idx))
diffcmap=setup_cmap('BlueYellowRed',clridx)
diffnorm = mpcrs.BoundaryNorm(difflvs,len(clridx)+1,extend='both')

for date in dlist:
    for fhr in fhrlist:
        plttmp=diff.sel(time=date,fhr=fhr)
        tistr='%s%s%s %s_f%.3i' %(exp_nm[1],minussign,exp_nm[0],date,fhr) 
        outname='%s/Diff_%s-%s_%s.%s_f%.3i.png' %(outputpath,exp_nm[1],exp_nm[0],pltvar,date,fhr)

        fig,ax,gl=setupax_2dmap(cornerll,area,proj,lbsize=txsize)
        set_size(axe_w,axe_h,b=0.13,l=0.1,r=0.95,t=0.95)
        cn=ax.contourf(plttmp.lon,plttmp.lat,plttmp.pltvar.data,levels=difflvs,norm=diffnorm,cmap=diffcmap,extend='both')
        ax.set_title(tistr,loc='left')
        plt.colorbar(cn,ax=ax,orientation='horizontal',ticks=difflvs[::2],
                     fraction=0.045,aspect=40,pad=0.08,label=cblb)
        if (area=='NAmer'):
           ax.add_feature(cft.STATES,zorder=2)
        print(outname,flush=1)
        fig.savefig(outname,dpi=quality)
        plt.close()
#
#    if (pltave):
#       if (dates_count==0):
#          var=tmpvar
#       else:
#          var=xa.concat((var,tmpvar),dim='time')
#
#       if (date==str(edate)):
#          outname='%s/%s_%s.mean.%s_%s.png' %(outputpath,area,pltvar,sdate,edate)
#          title_str='%s-%s'%(sdate,edate)
#
#          pltdata=var.mean(dim='time')
#          fig,ax,gl=setupax_2dmap(cornerll,area,proj,lbsize=txsize)
#          set_size(axe_w,axe_h,b=0.13,l=0.05,r=0.95,t=0.95)
#          cn=ax.contourf(pltdata.lon,pltdata.lat,pltdata,levels=cnlvs,cmap=clrmap,norm=aer_norm,extend='both')
#          ax.set_title(title_str,loc='left')
#          plt.colorbar(cn,ax=ax,orientation='horizontal',ticks=cnlvs[::tkfreq],
#                       fraction=0.045,aspect=40,pad=0.08,label=cblb)
#          if (area=='NAmer'):
#             ax.add_feature(cft.STATES,zorder=2)
#          print(outname)
#          fig.savefig(outname,dpi=quality)
#          plt.close()
 
