import csv
import pandas as pd
import numpy as np
import  pathlib, re, os


"""
the previous saved csv is loaded to continue processing. To keep numbers range closer to the gene count
the days will be transformed to years. Some patients had more than one diagnosis of the same cancer. 
For simplicity, the first diagnosis will be used. Having the same person with two diagnosis could bias the results.
"""
TCGA = pd.read_csv('D:/XGBoost_Survival_Analysis/venv/TCGA-Merge.csv')

TCGA.rename({'days_to_death': 'years_to_death', 'days_to_birth': 'years_to_birth'}, axis=1, inplace=True)

TCGA['years_to_death'] = TCGA['years_to_death'].mul(0.002738)
TCGA['years_to_birth'] = TCGA['years_to_birth'].mul(-0.002738)

TCGA = TCGA.drop_duplicates(subset=['bcr_patient_barcode'])

"""
The following data must be converted to categorical one hot encoding to remove "string" data that the model cannot 
understand. Once the data is converted to categorical using "dummies", the columns before conversion are dropped.
"""

OHE_race = pd.get_dummies(TCGA['race_list'])
OHE_eth = pd.get_dummies(TCGA['ethnicity'])
OHE_neo = pd.get_dummies(TCGA['history_of_neoadjuvant_treatment'])
OHE_dx = pd.get_dummies(TCGA['other_dx'])


TCGA_data_OHE = pd.merge(left=OHE_race,right=TCGA,left_index=True,right_index=True)
TCGA_data_ETH = pd.merge(left=OHE_eth,right=TCGA_data_OHE,left_index=True,right_index=True)
TCGA_data_NEO = pd.merge(left=OHE_neo,right=TCGA_data_ETH,left_index=True,right_index=True)
TCGA_data_DX = pd.merge(left=OHE_dx,right=TCGA_data_NEO,left_index=True,right_index=True)


TCGA_data_DX.rename(columns={'No_x': 'no history of malignancy', 'Yes_x': 'yes history of malignancy',
                             'Yes, History of Prior Malignancy': 'history of prior malignancy',
                             'Yes, History of Synchronous/Bilateral Malignancy':'synchrnous/bilateral malignancy',
                             'No_y': 'no radiation','Yes_y' : 'yes radiation',
                             'Yes, Radiation Prior to Resection':'radiation prior to resection',
                             'Yes, Pharmaceutical Treatment Prior to Resection': 'pharmaceutical treatment prior resection'},
                    inplace=True)

TCGA_data_A_encoded = TCGA_data_DX.drop(['race_list','other_dx','ethnicity','history_of_neoadjuvant_treatment'],axis=1)


"""
We also have categorical binary data that must  be remapped to 0 and 1. After it is remapped, data is shuffled with a-
ratio of keeping 100% of the data.
"""
TCGA_data_A_encoded['gender'] = TCGA_data_A_encoded['gender'].map({'MALE': 0,'FEMALE': 1})
TCGA_data_A_encoded['has_radiations_information'] = TCGA_data_A_encoded['has_radiations_information'].map({'NO': 0,'YES': 1})
TCGA_data_A_encoded['vital_status'] = TCGA_data_A_encoded['vital_status'].map({'Alive': 0,'Dead': 1})
TCGA_data_A_encoded['has_drugs_information'] = TCGA_data_A_encoded['has_drugs_information'].map({'NO': 0,'YES': 1})


