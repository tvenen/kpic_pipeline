from glob import glob
import os
import kpicdrp.background as background
from kpicdrp.data import Dataset, DetectorFrame
from kpicdrp.caldb import DetectorCalDB


maindir = "/scr3/jruffio/data/kpic" # main data directory for raw files 
all_bkgd_dir = glob(os.path.join(maindir,"*_backgrounds")) # each directory name's filepath of raw files

det_caldb = DetectorCalDB(filepath="/scr3/kpic/KPIC_Campaign/calibs/DetectorCalDB") #cal db
calibdir = "/scr3/kpic/KPIC_Campaign/calibs" # main directory for directories of calibrated files to save to


# for loop for all directories with *_backgrounds
for dir in all_bkgd_dir:
    bkgd_dir_name = os.path.basename(dir) # 20200928_backgrounds
    bkgd_date = os.path.basename(dir).split("_")[0] # 20200928
    bkgddir = os.path.join(maindir, bkgd_dir_name) # /scr3/jruffio/data/kpic/20191013_backgrounds
    save_loc = os.path.join(calibdir, bkgd_date, "bkgd_bpmap") #"/scr3/kpic/KPIC_Campaign/calibs/20200928/bkgd_bpmap" to save all calibrated files
    
    # Create output directory if it does not exist.
    if not os.path.exists(os.path.join(calibdir, bkgd_date, "bkgd_bpmap")):
        os.makedirs(os.path.join(calibdir, bkgd_date, "bkgd_bpmap"))
    
    # make a list of the input raw data
    raw_filelist = glob(os.path.join(bkgddir,"raw","*.fits"))

    # read in the raw dataset  
    raw_dataset = Dataset(filelist=raw_filelist, dtype=DetectorFrame)

    master_bkgds, badpixmaps, unique_tint, unique_coadds = background.process_backgrounds(raw_dataset, save_loc=save_loc, fileprefix=bkgd_date, caldb_save_loc=det_caldb)
    # stop after first iteration