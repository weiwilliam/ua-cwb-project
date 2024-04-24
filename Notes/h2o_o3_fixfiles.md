# Apr 22, 2024
FV3 ATM at [GFS v16](https://github.com/NOAA-EMC/fv3atm/tree/production/GFS.v16) was checked out on FX1000.

# Apr 3, 2024
Please go to outside HPC and find my cloned ufs-weather-model repository at
`/nwpr/gfs/xa30/Git/ufs-weather-model`

1. global-workflow links h2o and o3 files as below,
   ```
   - [$(FIXgfs)/am/ozprdlos_2015_new_sbuvO3_tclm15_nuchem.f77,    $(DATA)/global_o3prdlos.f77]
   - [$(FIXgfs)/am/global_h2o_pltc.f77,                           $(DATA)/global_h2oprdlos.f77]
   ```
2. The reading modules are under
   Ozone: `FV3/ccpp/physics/physics/photochem/module_ozphys.F90`
   The function call is at line 5574-5591 of `FV3/ccpp/data/GFS_typedef.F90`
   H2O: `FV3/ccpp/physics/physics/photochem/h2ointerp.f90`
   The subroutine call is at line 227 of `FV3/ccpp/physics/physics/Interstitials/UFS_SCM_NEPTUNE/GFS_phys_time_vary.fv3.F90`

3. The ozone data is read at the beginning (in `GFS_typedef.F90`) and interpolated (`ozphys%setup_o3prog`) and updated (`ozphys%update_o3prog`) for every time step in `GFS_rad_time_vary.fv3.F90`.
4. H2O data is read (`call read_h2odata`) and setup (`call setindxh2o` and `call h2ointerpol`) at each time step in `GFS_phys_time_vary.fv3.F90`.
* I don't fully understand the difference between the subroutine `GFS_phys_time_vary_init` and `GFS_phys_time_vary_timestep_init`
