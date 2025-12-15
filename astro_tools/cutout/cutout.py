from astropy.nddata import Cutout2D
from astropy.wcs import WCS
from astropy.io import fits
from astropy.coordinates import SkyCoord
import numpy as np

def make_cutout(fits_path, ra, dec, size, mode='partial', extension=0):
    """
    Create cutout from FITS file
    
    Parameters:
    -----------
    fits_path : str
        Path to FITS file
    ra, dec : float
        Coordinates in degrees
    size : int
        Cutout size in pixels
    mode : str
        'partial', 'trim', or 'strict'
    
    Returns:
    --------
    cutout : Cutout2D object
    """
    if not (np.isfinite(ra) and np.isfinite(dec)):
        raise ValueError(f"Invalid coordinates: RA={ra}, DEC={dec}")
    
    coord = SkyCoord(ra, dec, unit='deg')
    
    with fits.open(fits_path) as hdul:
        data = hdul[extension].data
        wcs = WCS(hdul[extension].header)
        cutout = Cutout2D(data, coord, size, wcs=wcs, mode=mode)
    
    return cutout


def check_coord_inside_fits(fits_path, ra, dec, extension=0):
    """
    Check if coordinates are inside FITS file
    
    Parameters:
    -----------
    fits_path : str
        Path to FITS file
    ra, dec : float
        Coordinates in degrees
    extension : int
        HDU extension (default: 0)
    
    Returns:
    --------
    bool : True if coordinates are inside file, False otherwise
    """
    try:
        make_cutout(fits_path, ra, dec, size=1, mode='strict', extension=extension)
        return True
    except FileNotFoundError:
        raise FileNotFoundError(f"FITS file not found: {fits_path}")
    except Exception:
        return False