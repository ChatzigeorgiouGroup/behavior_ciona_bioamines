import numpy as np
from scipy.signal import savgol_filter


def get_curv_savgol(skel_array, wl=15, order=2):
    
    """ Function to calculate curvatures of a ciona skeleton 
        The derivates are calcuated using savitzky-golay filters
        
        Keyword arguments:
        skel_array -- 3D array of shape (N,n,2)
            N ------- Number of frames 
            n ------- Number of skeleton points

        wl -- The length of the filter window (i.e. the number of coefficients). wl must be a positive odd integer.
        order -- The order of the polynomial used to fit the samples. It must be less than wl.
               
    """

    # first and second derivatives computed using savgol filters
    dx = savgol_filter(skel_array[:,:,0],window_length=wl,polyorder=order,deriv=1,mode='nearest')
    dy = savgol_filter(skel_array[:,:,1],window_length=wl,polyorder=order,deriv=1,mode='nearest')
    ddx = savgol_filter(skel_array[:,:,0],window_length=wl,polyorder=order,deriv=2,mode='nearest')
    ddy = savgol_filter(skel_array[:,:,1],window_length=wl,polyorder=order,deriv=2,mode='nearest')

    # curvature formula adapted from Tierpsy paper 
    #curvatures = np.abs(dx*ddy - dy*ddx)/(dx**2+dy**2)**1.5
    curvatures = (dx*ddy - dy*ddx)/(dx**2+dy**2)**1.5
    
    return curvatures


def get_tan_angles(skel_array, uni_lat=True, center = False, filt = False, mean_center = True):
    
    """Function that returns the tangent angles for a given skeleton array with respect to the horizontal axis
    Keyword arguments:
    
    skel_array -- 3D array of shape (N,n,2)
        N ------- Number of frames 
        n ------- Number of skeleton points
    """
    if filt:
        skel_array = savgol_skeleton(skel_array)
        
    tan_angles = np.arctan2(np.diff(skel_array[:,:,1]),np.diff(skel_array[:,:,0]))
    
    if center:
        tan_angles -= tan_angles[:,0].reshape(-1,1)
        
    if mean_center:
        tan_angles -= np.mean(tan_angles, axis=1, keepdims=True )
    
    if uni_lat:
        tan_angles[tan_angles<0] += 2*np.pi
        
    
    return tan_angles

def savgol_skeleton(skel_array, wl=15):
    
    """Function that smoothens a given skeleton array using a savitzky golay filter
    Keyword arguments:
    
    skel_array -- 3D array of shape (N,n,2)
        N ------- Number of frames 
        n ------- Number of skeleton points
    """
    skel_array_filt = savgol_filter(skel_array, window_length=wl, polyorder=2, mode='nearest', axis=1)
    
    return skel_array_filt