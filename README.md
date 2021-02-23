# rnaseq-pipelines-v2 README

The code in this repository represents a collection of bash, python, and R scripts for processing RNA-Seq data on a slurm cluster.
I am polishing coding and putting it into a publically available repository for others to view and hopefully use--especially in the University of Michigan Rogel Comprehensive Cancer Center, Cancer Data Sciences shared resource.

##### ymmv

## Pipeline Overview:
1. 01--build-fastq-catalog: create a table mapping sample names to fastq files
2. 02--process: using a cluster, perform in parallel for each sample alignment, quantification
3. 03--post-process: gather quantifications into a single file
4. 04--diffex: perform differential expression using deseq2
5. 05--david: perform gene set enrichment using DAVID 
6. 06--gsea: perform gene set enrichment using GSEA
7. 10--visuals: generate basic visualizations to describe data

## Module requirements: 
* star/2.5.2a
* stringtie/2.1.1
* subread/1.6.1
* R/3.5.0
* fastqc/0.11.5
* samtools/1.5

## Instructions for starting out:
Step 1: Create a project directory to contain your analysis    
Step 2: Change into your project directory and download this respository  
Step 3: Copy 01--build-fastq-catalog from the repository directory to the project directory  
Step 4: Change into the 01--build-fastq-catalog directory  

## 01--build-fastq-catalog
Step 1: Create experimentalDesign.txt table (look in input directory for example)  
Step 2: Update 01-pull-data.sh to fastq data directory and experimentalDesign.txt file  
Step 3: Run process.sh to execute 01-pull-data.sh, 02-build-fq2sample.sh, 03-map-to-samples.py, and create fastqCatalog in output directory  

Next: Copy 02--process from rnaseq-pipelines-v2 directory  
## 02--process
Step 1: Update 01-pull-data.sh to point to fastqCatalog  
Step 2: Run process.sh to execute 01-pull-data.sh, 02-build-fastq-catalog.py, 03-build-sample-replicate-catalog.sh  
Step 3: Update and run pipeline-setup.py and pipeline-execute.py  
Step 4: Run ./04-gather-counts.sh and 05-pivot-counts.sh and copy 05.txt to output as fragmentCounts file (see process.sh)  


