# -*- coding: utf-8 -*-
import sys
from watertools.Collect.GPM.DataAccess import DownloadData


def main(Dir, Startdate='', Enddate='', latlim=[-90, 90], lonlim=[-180, 180], cores=False, Waitbar = 1):
    """
    This function downloads GPM (daily) data

    Keyword arguments:
    Dir -- 'C:/file/to/path/'
    Startdate -- 'yyyy-mm-dd'
    Enddate -- 'yyyy-mm-dd'S
    latlim -- [ymin, ymax] (values must be between -50 and 50)
    lonlim -- [xmin, xmax] (values must be between -180 and 180)
    cores -- The number of cores used to run the routine.
             It can be 'False' to avoid using parallel computing
             routines.
    Waitbar -- 1 (Default) will print a waitbar
    """
     # Download data
    print('\nDownload daily GPM precipitation data for period %s till %s' %(Startdate, Enddate))
    DownloadData(Dir, Startdate, Enddate, latlim, lonlim, Waitbar, cores, TimeCase='daily')

if __name__ == '__main__':
    main(sys.argv)
