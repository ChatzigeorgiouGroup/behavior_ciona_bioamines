import os
import sys
import re
import difflib
import numpy as np


def correct_drugnames(data_folder):
    
    # True (standardized) drug names taken from Jerneja's plot diagrams
    drug_names = ['AA', 'Dopamine','Fluoxetine','Methiothepin', 'None', 'Octopamine', 'Serotonin',
                   'Tyramine', 'Alphamethyl', 'Chlorpromazine', 'Clomipramine','Imipramine',  
                   'Mianserin','Paroxetine', 'Phentolamine', 'Quinpirole', 'Raclopride']

    # according to the file naming convention, the position of drug name is after the 5th underscore
    drug_pos = 4

   
    # get all filenames from the data_folder
    (_,_, skel_fnames) = next(os.walk(data_folder))

    for fname in skel_fnames:

        if fname.endswith('.hdf5'):
            old_path = os.path.join(data_folder,fname)
            # get only the alpha (name and not conc) part of the drug label
            drug_conc = re.findall(r"[^\W\d_]+|\d+", fname.split('_')[drug_pos])
            # QUICKFIX : 'ascorbicacid vs AA'
            drug = fname.split('_')[drug_pos]
            # find the closest match of the drug name from the list "drug_names"         
            true_drug_name = difflib.get_close_matches(drug, drug_names, n = 1, cutoff= 0.6)
            # replace the old spelling with the closest match 
            try:
                fname_new = fname.replace(drug_conc[0],true_drug_name[0])
            except IndexError :
                fname_new = fname.replace(drug_conc[0],'AA')
            finally:
                new_path = os.path.join(data_folder, str(fname_new))
                # rename the file
                os.rename(old_path, new_path)

def check_mispelled(data_folder):
    
    drug_names = ['AA', 'Dopamine','Fluoxetine','Methiothepin', 'None', 'Octopamine', 'Serotonin',
               'Tyramine', 'Alphamethyl', 'Chlorpromazine', 'Clomipramine','Imipramine',  
               'Mianserin','Paroxetine', 'Phentolamine', 'Quinpirole', 'Raclopride']
    
    drug_pos = 4

    (_,_, skel_feat_fnames) = next(os.walk(data_folder))
    
    list_paths_mis = []
    n_mis = 0

    for filename in skel_feat_fnames:

        # only applied to (JDA) feature files : read note above  
        #if filename.endswith('features_JDA.pickle'):
        if filename.endswith('.hdf5'):

            # get only the alpha and numeric part of the drug label
            drug_conc = re.findall(r"[^\W\d_]+|\d+", filename.split('_')[drug_pos])


            # if drug name (wxclusing the conc) is not one in the list "drug_names"
            #if (difflib.get_close_matches(drug_conc[0], drug_names, n= 1, cutoff= 1)) == None:
            if drug_conc[0] not in drug_names:
                n_mis += 1
                list_paths_mis.append(os.path.join(data_folder,filename))
                
    return n_mis, list_paths_mis

def list_meta_drugs(data_folder):
    
    drug_list = []
    drug_name_conc_list = []

    drug_pos = 4
    
    (_,_, skel_feat_fnames) = next(os.walk(data_folder))
    
    for feat_fname in skel_feat_fnames:

        #if feat_fname.endswith('features_JDA.pickle'):
        if feat_fname.endswith('.hdf5'):

            drug = feat_fname.split('_')[drug_pos]
            drug_name_conc = re.findall(r"[^\W\d_]+|\d+", drug)
            
            if drug not in drug_list:
                drug_list.append(drug)
                drug_name_conc_list.append(drug_name_conc)              

    drug_list = (sorted(drug_list))
    drug_name_conc_list = sorted(drug_name_conc_list)
    
    return drug_list,drug_name_conc_list