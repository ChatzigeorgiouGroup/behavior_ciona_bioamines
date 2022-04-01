import h5py
import numpy as np

class TierpsySkeleton:
    
    def __init__(self, file_path):
        self.orig_filepath = file_path
        self.skel_array = self.read_skeleton_as_array()
        self.neck_coords = self.get_neck_points()
        self.quality = self.calc_quality()
        
        
    def read_skeleton_as_array(self,skel_array=None):
        """
        Read the skeleton database from hdf5 file and returns it as an array
        Keyword arguments:
            file_path -- full path to the skeleton file in hdf5 format
        Returns :
            skeletons : 3D array of shape (number of frames,number of skeleton points,2)
        """
        try:
            skeletons_store = h5py.File(file_path, 'r')
            skeletons = np.array(skeletons_store['coordinates']['skeletons'])
        except IOError:
            print("Unable to read the file : check if the file exists")
        except KeyError:
            skeletons = np.array(skeletons_store['skeleton'])
        return skeletons


    def get_skel_length(self,file_path):
        try:
            skeletons_store = h5py.File(file_path, 'r')
            skel_length = np.array(skeletons_store['skeleton_length'])
        except IOError:
            print("Unable to read the file : check if the file exists")
        except KeyError:
            print('KeyError')
        return skel_length

    def get_neck_points(self,from_array=True):
        try:
            skeletons_store = h5py.File(file_path, 'r')
            cont_widths = np.array(skeletons_store['contour_width'])
            print(np.shape(cont_widths),np.shape(np.diff(cont_widths)))
            diff_contour = np.nanmean(np.diff(cont_widths), axis=0)
            print(diff_contour.shape)
            diff_contour = diff_contour[3:26]
            neck_point = np.argmin(diff_contour)+4
        except IOError:
            print("Unable to read the file : check if the file exists")
        except KeyError:
            print('KeyError')
        return neck_point


    def calc_quality(self, skel_array):
        """
        Computes the quality of a give skeleton array
        Keyword arguments:
        skel_array -- 3D skeleton array
        Returns :
        quality : Percentage of rows (frames) in the skeleton array (experiment) which are not all NaNs
        """
        n_notnan_rows = np.sum(np.sum(np.isnan(skel_array[:,:,0]) & np.isnan(skel_array[:,:,1]),axis=1) < skel_array.shape[1])
        quality = (n_notnan_rows/skel_array.shape[0])*100
        return quality

    def del_nan_rows(self,skel_array):
        """
        Deletes the rows (frames) in the skeleton array( experiment) which are all NaNs
        Keyword arguments:
        skel_array -- 3D skeleton array
        Returns :
        a :  3D array 
        """
        a = skel_array[~np.isnan(skel_array[:,:,0]).all(axis=1)]
        return a