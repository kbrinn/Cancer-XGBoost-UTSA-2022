'''
Title     : functions_file
Objective : Functions to process and transform TCGA data from https://portal.gdc.cancer.gov/ with R
Created by: Kevin Brinneman for UTSA Electrical & Computer Engineering
Created on: 2022-01-23

This script will recursively iterate over all folder to decompress GZ files.Once decompressed, all RNA_seq files are
opened as .COUNTS format and processed as JSON files. JSON format is preferible over .TXT files to prevent data
corruption.
'''

'''
Directory tree only showing three samples. The same architecture continues for the list showed below.
Directory originally in Data_processing/preprocessed_data/GDC. Files too large to share.

----TCGA
    |----GDC_Data
    |    |----TCGA-ACC
              |----harmonized
                   |----Transcriptome_Profiling
                        |----Gene_Expression_Quantification
                            |----[folders with txt files]
                   |----Clinical
                        |----Clinical_Supplement
                            |----[folders with txt files]
    |    |----TCGA-BLCA
              |----harmonized
                   |----Transcriptome_Profiling
                        |----Gene_Expression_Quantification
                            |----[folders with txt files]
                   |----Clinical
                        |----Clinical_Supplement
                            |----[folders with txt files]
    |    |----TCGA-BRCA
              |----harmonized
                   |----Transcriptome_Profiling
                        |----Gene_Expression_Quantification
                            |----[folders with txt files]
                   |----Clinical
                        |----Clinical_Supplement
                            |----[folders with txt files]
                            
    .
    .
    .
    
    [           ...          ...        ... TCGA-CESC,TCGA-CHOL,TCGA-COAD,
    TCGA-DLBC, TCGA-ESCA,TCGA-GBM,TCGA-HNSC,TCGA-KICH,TCGA-KIRC,TCGA-KIRP,
    TCGA-LGG, TCGA-LIHC,TCGA-LUAD,TCGA-LUSC,TCGA-MESO,TCGA-OV,TCGA-PAAD,
    TCGA-PCPG, TCGA-PRAD,TCGA-READ,TCGA-SARC,TCGA-SKCM,TCGA-STAD,TCGA-TGCT,
    TCGA-THCA,TCGA-THYM,TCGA-UCEC,TCGA-UCS,TCGA-UVM,TCGA-LAML]
'''


#import libraries
import gzip, pathlib, shutil, json, re

#Where the directory is located
base_dir = "D:/GDCdata"

#Function to open .COUNTS files, proccess them as JSON, and deletion of processed files.

def unpack_all_in_dir(_dir):
    path = pathlib.Path(_dir)
    for gzfilepath in path.rglob('*.gz'):
        with gzip.open(gzfilepath) as f, gzfilepath.with_suffix('').open('wb') as fw:
            shutil.copyfileobj(f, fw)
        os.remove(gzfilepath)

unpack_all_in_dir(base_dir)

#Function used to find clinical-to-rna match. Creates two dictionaries of clinical and rna data
# and is compared to find a match between samples with same ID alphanumeric string

def merge_data_files(_dir):
    path = pathlib.Path(_dir)
    tcga_type = [item for item in path.iterdir() if item.is_dir()] #make the folder a mutable object list
    GDC_data = {}
    for tcga in tcga_type:
        GDC_data[tcga.name] = {}
        for clinical in tcga.glob('Clinical_Supplement'):
            Clinical_Supplement = {}
            for case in clinical.iterdir():
                Clinical_Supplement[case.name] = case
        for rna_cases in tcga.glob('Gene_Expression_Quantification'):
            Gene_Expression_Quantification = {}
            for sample in rna_cases.iterdir():
                Gene_Expression_Quantification[sample.name] = sample
        ({f for f in Clinical_Supplement} & {f for f in Gene_Expression_Quantification})
    print(GDC_data)

#Function to iterate over all folders to save samples as JSON files and convert each .COUNT file
#to JSON format. Each JSON formart file is processed as a dictionary.

def header_check_df (_dir):
    path = pathlib.Path(_dir)
    for headers in path.rglob('*.htseq.counts'):
        object_gene= {}
        feature_rna_string = {}
        with open(headers) as f:
            for line in f:
                gene, count = line.strip().split(None,1)
                feature_rna_string.update({gene: int(count)})
            object_gene[str(re.sub(r'.htseq.counts', '', headers.name))] = feature_rna_string
        file_regexd = re.sub(r'.htseq.counts','',headers.name) + '.json'
        out_file = open(headers.parent.joinpath(file_regexd), 'w')
        json.dump(object_gene, out_file, indent = 4, sort_keys= False)
        out_file.close()

header_check_df(base_dir)

