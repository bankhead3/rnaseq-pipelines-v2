# rnaseq-pipelines-v2 README

The code in this repository represents a collection of bash, python, and R scripts for processing RNA-Seq data on a slurm cluster.
I am polishing coding and putting it into a publically available repository for others to view and hopefully use--especially in the University of Michigan Rogel Comprehensive Cancer Center, Cancer Data Sciences shared resource.

##### YMMV!

## Pipeline Overview:
1. 01--build-fastq-catalog: create a table mapping sample names to fastq files
2. 02--process: using a cluster, perform in parallel for each sample alignment, quantification
3. 03--post-process: gather quantifications into a single file
4. 04--diffex: perform differential expression using deseq2
5. 05--david: perform gene set enrichment using DAVID 
6. 06--gsea: perform gene set enrichment using GSEA
7. 10--visuals: generate basic visualizations to describe data

## Expected module requirements: 
1. STAR
2. Stringtie

Instructions for starting out:
Step 1: Create a project directory to contain your analysis.  
Step 2: Change into your project directory and download this respository
Step 3: Copy 01--build-fastq-catalog from the repository directory to the project directory
Step 4: Change into the 01--build-fastq-catalog directory

## 01--build-fastq-catalog

