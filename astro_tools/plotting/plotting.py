# utils/plotting.py
import matplotlib.pyplot as plt
from astropy.visualization import ZScaleInterval, ImageNormalize
import numpy as np

def plot_cutout(cutout, title=None, figsize=(8, 8), show_grid=True):
    """
    Plot cutout with WCS projection
    
    Parameters:
    -----------
    cutout : Cutout2D object
    title : str, optional
    figsize : tuple
    show_grid : bool
    """
    norm = ImageNormalize(cutout.data, interval=ZScaleInterval())
    
    fig, ax = plt.subplots(figsize=figsize, subplot_kw={'projection': cutout.wcs})
    
    im = ax.imshow(cutout.data, origin='lower', norm=norm, cmap='gray')
    
    ax.set_xlabel('RA')
    ax.set_ylabel('Dec')
    
    if title:
        ax.set_title(title)
    
    if show_grid:
        ax.grid(color='white', ls=':', alpha=0.5)
    
    plt.colorbar(im, ax=ax, label='Flux')
    
    return fig, ax