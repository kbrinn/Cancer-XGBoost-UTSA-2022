# Title     : TODO
# Objective : The demo code for downloading TCGA data, Chris Chiu, GCCRI/UTHSCSA, April 2018
# Created by: CSBL 6095, Analaysis and Visualization of Genomic Data, Jan 2018, UTHSCSA
# Created on: 2022-02-19

setwd("../../TCGA_survival_analysis")

#first time use devtools, you have to install
#install.packages("devtools")

# install the TCGAbiolinks package from Github (the Bioconductor version of TCGAbiolinks seems to have some unfixed bugs)
# if you don't have devtools, run install.packages(devtools) first
#devtools::install_github(repo = "BioinformaticsFMRP/TCGAbiolinks")

# install SummarizedExperiment package if you haven't done it earlier this semester
#source("https://bioconductor.org/biocLite.R")
#biocLite("SummarizedExperiment")

# read the website for an overview/tutorial of TCGAbiolinks: https://bioconductor.org/packages/release/bioc/vignettes/TCGAbiolinks/inst/doc/download_prepare.html
library(TCGAbiolinks)
library(SummarizedExperiment)

# overview of the cancer type of your interest
#TCGAbiolinks:::getProjectSummary("TCGA-BRCA") # ACC is one of the smallest cancer type and used as an example here
# visit this website for a list of cancer types: https://bioconductor.org/packages/release/bioc/vignettes/TCGAbiolinks/inst/doc/query.html#project_options

# download raw HTSeq counts of all AML samples



query <- GDCquery(project = c('TCGA-UVM'),
                  #sample.type = "Primary solid Tumor", # visit this website for a list of sample.type (including normal controls): https://bioconductor.org/packages/release/bioc/vignettes/TCGAbiolinks/inst/doc/query.html#sampletype_options
                  data.category = "Transcriptome Profiling",
                  data.type = "Gene Expression Quantification",
                  workflow.type = "HTSeq - FPKM", # or 'HTSeq - FPKM'
                  legacy = FALSE)

query <- GDCquery(project = c(
                             'TCGA-ACC','TCGA-BLCA','TCGA-BRCA','TCGA-CESC','TCGA-CHOL','TCGA-COAD','TCGA-DLBC',
                             'TCGA-ESCA','TCGA-GBM','TCGA-HNSC','TCGA-KICH','TCGA-KIRC','TCGA-KIRP','TCGA-LGG',
                             'TCGA-LIHC','TCGA-LUAD','TCGA-LUSC','TCGA-MESO','TCGA-OV','TCGA-PAAD','TCGA-PCPG',
                             'TCGA-PRAD','TCGA-READ','TCGA-SARC','TCGA-SKCM','TCGA-STAD','TCGA-TGCT','TCGA-THCA',
                             'TCGA-THYM','TCGA-UCEC','TCGA-UCS','TCGA-UVM','TCGA-LAML'),
                 #sample.type = "Primary solid Tumor", # visit this website for a list of sample.type (including normal controls): https://bioconductor.org/packages/release/bioc/vignettes/TCGAbiolinks/inst/doc/query.html#sampletype_options
                 data.category = "Transcriptome Profiling",
                 data.type = "Gene Expression Quantification",
                 file.type = "normalized_results",
                 workflow.type = "HTSeq - FPKM", # or 'HTSeq - FPKM'
                 legacy = FALSE)

# data.category, data.type, workflow.type, and legacy can be changed if you want any other data than RNA-Seq
# in this case, please visit the following websites for choices:
# table of legacy (most NGS) datasets: https://bioconductor.org/packages/release/bioc/vignettes/TCGAbiolinks/inst/doc/query.html#harmonized_data_options_(legacy_=_false)
# table of non-legacy (most microarrays) datasets: https://bioconductor.org/packages/release/bioc/vignettes/TCGAbiolinks/inst/doc/query.html#legacy_archive_data_options_(legacy_=_true)

GDCdownload(query) # download the data, this step can take some time depending on internet bandwidth
data <- GDCprepare(query)
#data <- GDCprepare(query,save = TRUE ,save.filename, directory = "GDCdata", summarizedExperiment = TRUE, remove.files.prepared = FALSE)
data_num <- assay(data) # extract numeric data; cols are samples and rows are genes
data_clin <- colData(data) # extract indexed clinical data and subtype information from marker TCGA papers
data_feat <- rowRanges(data) # extract feature matrix information (gene information)
gene_annot <- as.data.frame(data_feat@elementMetadata@listData) # ENSG gene IDs and gene symbols

data_num <- log2(data_num+1)

write.table(file = "exp_fpkm_pancan_data_log2plus1.xml", x = data_num, quote = FALSE, sep = "\t", eol = "\n", row.names  = T, col.names = T)
write.table(file = "exp_fpkm_pancan_clinical.txt", x = data_clin, quote = FALSE, sep = "\t", eol = "\n", row.names  = T, col.names = T)
write.table(file = "exp_fpkm_pancan_geneannot.txt", x = gene_annot, quote = FALSE, sep = "\t", eol = "\n", row.names  = T, col.names = T)

# download clinical data

a = c('UVM')

a = c('ACC','BLCA','BRCA','CESC','CHOL','COAD','DLBC',
     'ESCA','GBM','HNSC','KICH','KIRC','KIRP','LGG',
     'LIHC','LUAD','LUSC','MESO','OV','PAAD','PCPG',
     'PRAD','READ','SARC','SKCM','STAD','TGCT','THCA',
     'THYM','UCEC','UCS','UVM','LAML')

for( i in 1:length(a)) {
  cancer_type = a[i]
  print(cancer_type)
  query <- GDCquery(project = paste0('TCGA-',cancer_type), data.category = "Clinical", file.type = "xml")
  GDCdownload(query)

  clinical.drug <- GDCprepare_clinic(query, clinical.info = "patient")
  write.table(file = paste0(cancer_type, "_patient.txt"), x = clinical.drug, quote = FALSE, sep = "\t", eol = "\n", row.names  = F, col.names = T)
  clinical.drug <- GDCprepare_clinic(query, clinical.info = "drug")
  write.table(file = paste0(cancer_type, "_drug.txt"), x = clinical.drug, quote = FALSE, sep = "\t", eol = "\n", row.names  = F, col.names = T)
  clinical.drug <- GDCprepare_clinic(query, clinical.info = "follow_up")
  write.table(file = paste0(cancer_type, "_followup.txt"), x = clinical.drug, quote = FALSE, sep = "\t", eol = "\n", row.names  = F, col.names = T)
  clinical.drug <- GDCprepare_clinic(query, clinical.info = "radiation")
  write.table(file = paste0(cancer_type, "_radiation.txt"), x = clinical.drug, quote = FALSE, sep = "\t", eol = "\n", row.names  = F, col.names = T)
  clinical.drug <- GDCprepare_clinic(query, clinical.info = "stage_event")
  write.table(file = paste0(cancer_type, "_stage_event.txt"), x = clinical.drug, quote = FALSE, sep = "\t", eol = "\n", row.names  = F, col.names = T)
  clinical.drug <- GDCprepare_clinic(query, clinical.info = "new_tumor_event")
  write.table(file = paste0(cancer_type, "_new_tumor_event.txt"), x = clinical.drug, quote = FALSE, sep = "\t", eol = "\n", row.names  = F, col.names = T)
  }