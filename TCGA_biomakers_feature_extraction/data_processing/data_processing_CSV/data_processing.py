import csv
import pandas as pd
import  pathlib, re, os

"""
Path to the data folder where cancer types are located. Main file is TCGA with subfolders of clinical and- 
gene expression data for each cancer type.
"""


directory =  'D:/XGBoost_Survival_Analysis/venv/dataset_preprocessed'


"""
Recursive iteration through the directory to find all the gene expression files. Once the file is found-,
it is opened, transposed and saved as a csv file. The data is trasposed to make the genes concatenate with-
clinical data. (patient case as a row and gene as a column).
"""

def transpose_data(_dir):
    path = pathlib.Path(_dir)
    for file in path.rglob('*.csv'):
        if bool(re.search(pattern='exp_fpkm_', string=str(file))) == True:
            string_name = str((os.path.dirname(os.path.abspath(file))) + '/transposed_' + file.name)
            data = pd.read_csv(file)
            data.transpose().to_csv(string_name, encoding = 'utf-8')
"""
add gene data and add clinical data creates a dictionary of datasets to find:

1. if all dataset share the same genes (same dataframe size and same features)
2. to find the intersection of clinical data. (what clinical data is shared among-
    all cancer types).

"""

def add_gene_data(_dir):
    path = pathlib.Path(_dir)
    data_frames_gene = {}
    for data in path.rglob('*.csv'):
        if bool(re.search(pattern='transposed', string=str(data))) == True:
            data_frames_gene["string{0}".format(data.name)] = pd.read_csv(data,skiprows = [0])
    print(data_frames_gene)
    return data_frames_gene


def add_clinical_data(_dir):
    path = pathlib.Path(_dir)
    data_frames_clinical = {}
    for data in path.rglob('*.csv'):
        if bool(re.search(pattern='patient', string=str(data))) == True:
            data_frames_clinical["string{0}".format(data.name)] = pd.read_csv(data,skiprows = [0])
    print(data_frames_clinical)
    return data_frames_clinical

"""
calling the function to find intersection of clinical & gene data
"""
general_features_clinical = set(TCGA_clinical_dictionary['ACC_patient.csv'].columns.values).intersection\
    (*[TCGA_clinical_dictionary[data_headers].columns.values for data_headers in TCGA_clinical_dictionary])


general_features_gene = set(TCGA_gene_dictionary['transposed_ACC_exp_fpkm_pancan_data_log2plus1.csv'].columns.values)\
    .intersection(*[TCGA_gene_dictionary[data_headers].columns.values for data_headers in TCGA_gene_dictionary])

"""
these clinical features are the same for all cancer types.

['bcr_patient_barcode','stage_event_pathologic_stage','has_drugs_information','days_to_death','days_to_birth',
'race_list','other_dx','gender','project','has_radiations_information','vital_status','history_of_neoadjuvant_treatment',
'ethnicity']

Function used to iterate over all clinical data files to open csv file only with the columns defined in 
"general features". Once opened, the columns are reindexed for order consistency across all cancer types.
"""

def clinical_data_processed(_dir,general_features_clinical):
    path = pathlib.Path(_dir)
    for file in path.rglob('*.csv'):
        if bool(re.search(pattern='_clinical', string=str(file))) == True:
            file.name = pd.read_csv(file, usecols=general_features_clinical)
            file.name = file.format.reindex(columns=general_features_clinical)
            file.name.to_csv(file.name, index = false, encoding = 'utf-8')
    return ('clinical data processed')

"""
after data clinical data and gene is processed, data merger script will combine datasets
"""


